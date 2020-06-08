# 根据给定的IP地址段，自动搜索运行的网络设备，获取网络设备IP信息、设备基本信息、设备运行数据，写入MariaDB数据库
# 除运行信息获取外，其它模块一般在初始化时使用

import os
import re
import time

import pymysql
from snmp_cmds import snmpwalk


def get_ip_list(ip_start, ip_end):  # 通过起止ip计算可用地址段列表
    pattern = re.compile(
        "^([1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])")  # ip规范

    if not (re.match(pattern, ip_start) and re.match(pattern, ip_end)):  # ip格式判断
        print("输入的Ip地址格式错误！")
    elif len(list(filter(lambda x: x < 255, [int(i) for i in ip_start.split(".")]))) != 4 or len(
            list(filter(lambda x: x < 255, [int(i) for i in ip_end.split(".")]))) != 4:  # ip每段的取值判断
        print("输入的ip地址范围有误！")
    elif ip_start[:ip_start.rfind(".")] != ip_end[:ip_end.rfind(".")]:  # IP子网判断
        print("输入的ip地址起止子网不一致！")
    else:
        ip_net = ip_start[:ip_start.rfind(".")]
        ip_list = []
        for i in range(int(ip_start[ip_start.rfind(".") + 1:]), int(ip_end[ip_end.rfind(".") + 1:]) + 1):
            ip_list.append("{}.{}".format(ip_net, i))
        return (ip_list)


def get_ip_status(ip_list):  # 判断传入的ip地址列表中ip是否存活
    ip_list_status = []

    for i in ip_list:
        if not os.system("ping -n 1 -w 1 {}".format(i)):
            ip_list_status.append(i)
            print("发现存活ip{}".format(i))

    with open("ip.text", "w", encoding="utf8") as f:  # 写入本地文本
        ip_list_status_text = ",".join(ip_list_status)
        f.writelines(ip_list_status_text)

    return (ip_list_status)


def scan_ip(ip_start, ip_end):  # 调用完成ip计算和ip存活，返回存活列表
    s_t = time.perf_counter()
    # 扫描起止ip地址
    ip_list = get_ip_list(ip_start, ip_end)
    ip_list_status = get_ip_status(ip_list)

    print("\n\n{:=^66}\n{}\n\n扫描耗时{}秒.".format("发现存活ip " + str(len(ip_list_status)) + "个", ip_list_status,
                                               time.perf_counter() - s_t))
    return (ip_list_status)


def get_ip_snmp_info(ip_list_status, snmp_oid_list, community):  # 获取存活ip的snmp详细信息
    ip_snmp = []

    for ip in ip_list_status:
        print("\n正在获取{}的snmp信息...:\n{:=<126}".format(ip, ""))
        ip_snmp_dic = {}
        e = 1
        try:  # 初步测试该ip的snmp是否可用，若可用生成ip列表（zip用）
            ip_list = [ip for i in range(int(snmpwalk(ip, "ifNumber", community)[0][1]))]
        except:
            print("{}snmp不可用！".format(ip))
            continue

        for snmp_oid in snmp_oid_list:  # 循环读取oid信息
            try:
                ip_snmp_dic[snmp_oid] = [i[1] for i in snmpwalk(ip, snmp_oid, community)]
            except:
                print("{}snmp信息获取不完整！".format(ip))
                e = 0
                break
            print(ip_snmp_dic[snmp_oid])
        if e: ip_snmp += list(zip(ip_list, *ip_snmp_dic.values()))
        print(ip_snmp)

    return (ip_snmp)


def wr_db(conn_db_info, table_name, field_name_list, values_list):
    conn = pymysql.connect(**conn_db_info)
    cur = conn.cursor()

    field_name = ",".join(field_name_list)
    values_name = ",".join(["%s" for i in field_name_list])

    sql = "insert into  {}  ({})  values ({})  ".format(table_name, field_name, values_name)
    print(sql)
    cur.executemany(sql, values_list)
    conn.commit()
    print("数据写库完成。")
    cur.close()
    conn.close()


if __name__ == "__main__":
    # 1.定义扫描起止地址等公共参数

    t_start = time.perf_counter()
    ip_start = "192.168.100.1"
    ip_end = "192.168.100.254"
    community = "xxww"
    snmp_oid_dic = {"base": ["sysDescr", "sysUpTime", "sysContact", "sysName", "sysLocation", "ifNumber"],
                    "detial": ["ifIndex", "ifDescr", "ifType", "ifMtu", "ifSpeed", "ifAdminStatus", "ifOperStatus",
                               "ifLastChange"],
                    "running": ["ifIndex", "ifInOctets", "ifInDiscards", "ifInErrors", "ifInUnknownProtos",
                                "ifOutOctets", "ifOutDiscards", "ifOutErrors", "ifOutQLen"]}

    conn_db_info = {"host": "127.0.0.1", "user": "root", "passwd": "mypasswordisroot", "db": "snmp", "port": 3793}

    # 2.获取存活ip地址

    # 2.1重新扫描存活ip

    ip_list_status = scan_ip(ip_start, ip_end)

    # 2.2从本地文本读取ip地址

    # with open("ip.text", "r", encoding="utf8") as f:
    #     ip_list = f.readline()
    #     ip_list_status = ip_list.split(",")

    # 3.获取存活ip基本信息

    ip_snmp = get_ip_snmp_info(ip_list_status, snmp_oid_dic["base"], community)

    # 3.1获取的基本信息写库

    field_name_list = ["ip"] + snmp_oid_dic["base"]
    wr_db(conn_db_info, "dev_ip", field_name_list, ip_snmp)

    # 4.获取存活ip详细信息

    ip_snmp = get_ip_snmp_info(ip_list_status, snmp_oid_dic["detial"], community)

    # 4.1获取的详细信息写库
    field_name_list = ["ip"] + snmp_oid_dic["detial"]
    wr_db(conn_db_info, "dev_detial", field_name_list, ip_snmp)

    # 5.执行结束

    print("\n{:=<126}\n程序执行完毕，耗时{}秒".format("", time.perf_counter() - t_start))

    #
