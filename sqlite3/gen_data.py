# 数据生成示例：
'''
随机生成姓名、性别、身份证号码、行政区划、省市、市区、区县信息
将生成结果写入sqlite数据库
数据库为当前父目录的DB下test.db
'''

import datetime
import json
import os
import random
import re
import time

import pandas
import sqlalchemy


def gen_name(num=10):  # 生成姓名、性别、身份证号、省市、市区、区县信息

    with open("name.json", "r") as name_file:  # 名字生成文件
        name_base = json.load(name_file)

    with open("xzqh.csv", "r") as xzqh_file:  # 行政区划文件
        xzqh_list = xzqh_file.readlines()
        # print(xzqh_list)

    name_list = []  # 姓名、性别、身份证号、省市、市区、区县
    xing_len = len(name_base["xing"])
    fuxing_len = len(name_base["fuxing"])
    boy_list = "".join(name_base["boy"])
    girl_list = "".join(name_base["girl"])

    for i in range(num):
        name_choose_list = ["00", "01", "10", "11", "00", "01", "00", "01", "00", "01","00","01"]  # 单姓女，单姓男，复姓女，复姓男
        name_choose = name_choose_list[random.randint(0, 3)]

        if name_choose == "00":
            name = name_base["xing"][random.randint(1, xing_len) - 1] + "".join(
                random.sample(girl_list, random.randint(1, 2)))
            sex = "女"
            sfz = gen_sfz(xzqh_list, 0)
        elif name_choose == "01":
            name = name_base["xing"][random.randint(1, xing_len) - 1] + "".join(
                random.sample(boy_list, random.randint(1, 2)))
            sex = "男"
            sfz = gen_sfz(xzqh_list, 1)
        elif name_choose == "10":
            name = name_base["fuxing"][random.randint(1, fuxing_len) - 1] + "".join(
                random.sample(girl_list, random.randint(1, 2)))
            sex = "女"
            sfz = gen_sfz(xzqh_list, 0)
        elif name_choose == "11":
            name = name_base["fuxing"][random.randint(1, fuxing_len) - 1] + "".join(
                random.sample(boy_list, random.randint(1, 2)))
            sex = "男"
            sfz = gen_sfz(xzqh_list, 1)
        else:
            print("姓名、性别生成错误！")

        name_list.append([name, sex] + sfz)

    return (name_list)


def gen_sfz(xzqh_list, sex):  # 生成身份证、省市、市区、区县信息
    rd = random.randint(0, len(xzqh_list) - 1)
    qh = xzqh_list[rd][0:6]

    while 1:

        if re.findall("..0000", qh) or re.findall("...[1-9]00", qh) or re.findall("....01", qh):
            rd = random.randint(0, len(xzqh_list) - 1)
            qh = xzqh_list[rd][0:6]
        else:
            ny = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(
                days=(365 * (random.randint(0, 100)) + 30 * (random.randint(1, 12)) + random.randint(1, 30))), "%Y%m%d")
            dm = str(random.randrange(100, 999, 2 ** sex))
            sfz = sfz_jy(qh + ny + dm)
            ss = xzqh_list[rd].split(",")[1]
            sq = xzqh_list[rd].split(",")[2]
            qx = xzqh_list[rd].split(",")[3][:-1]
            break

    name_sfz = [sfz, qh, ss, sq, qx]

    return (name_sfz)


def sfz_jy(sfz):  # 生成带校验位的身份证号码
    jy_code = "10X98765432"
    jy = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    sfz_list = list(sfz)
    jy = sum(list(map(lambda x, y: x * int(y), jy, sfz_list))) % 11
    sfz += str(jy_code[jy])

    return (sfz)


if __name__ == "__main__":
    num = 1000000
    print("正在生成数据（{}条），请稍后......".format(num))
    name_df = pandas.DataFrame(gen_name(num), columns=("name", "sex", "sfzh", "code", "ss", "sq", "qx"))
    print(name_df)

    par_path = os.path.dirname(os.path.dirname(os.getcwd()))
    db_path = par_path + "/DB/test.db"
    conn = sqlalchemy.create_engine("sqlite:///{}".format(db_path))
    print("数据生成完毕，正在写库...")
    st = time.perf_counter()
    name_df.to_sql("tb1", conn, if_exists="append", index=False)
    print("写库完成（{}条），耗时{:.2f}s。".format(num, time.perf_counter() - st))
