import time

from snmp_cmds import snmpwalk,snmpget



hosts = ["192.168.100.103","192.168.100.40"] # REPLACE these IPs with real IPs
oids = ["1.3.6.1.2.1.2.2.1.2",  #网络接口信息描述
        "1.3.6.1.2.1.2.2.1.5",  # 网络接口带宽bps
        "1.3.6.1.2.1.2.2.1.10",  #网络接口输入字节数
        "1.3.6.1.2.1.2.2.1.16"]   #网络接口输出字节数
ifids=["4228057","4228065","4228473","4228481"]

community = "xxww"

while 1:
    start = time.time()
    for host in hosts:
        print("Host:{}".format(host))
        for ifid in ifids:
            t1=",".join((host,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())))
            # print(t1)
            try:
                for oid in oids:
                    t1=",".join((t1,snmpwalk(host,".".join((oid,ifid)),community)[0][1]))
                with  open("ifconfig.text", "a", encoding="utf8") as fo:
                    fo.write(t1 + "\n")
                print(t1)
            except:
                print("ERROR !")


    end = time.time()
    print("本次轮询{}台设备、{}个接口，耗时 {} 秒".format(len(hosts),len(hosts)*len(ifids),end - start))
    time.sleep(300)

