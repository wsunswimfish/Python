import requests
from bs4 import BeautifulSoup

'''
Print显示彩色
开头部分： \033[显示方式; 前景色 ; 背景色 m
结尾部分： \033[0m

字体颜色	背景颜色	颜色描述
30	40	黑色
31	41	红色
32	42	绿色
33	43	黃色
34	44	蓝色
35	45	紫红色
36	46	青蓝色
37	47	白色

显示方式	效果
0	终端默认设置
1	高亮显示
4	使用下划线
5	闪烁
7	反白显示
8	不可见
'''
def paiming_get(url, year, type="dict"):
    # td结构:排名:学校:地区:总分指标得分:研究生比例(5%):留学生比例(5%):师生比(5%):博士学位授予数(10%)总量:师均:校友获奖(10%)总量	:生均
    headers = {"User-agent": "Mozilla/5.0"}
    r = requests.get(url.format(year), headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")

    if type == "list":
        paiming_list = []  # 返回列表
        for tag in soup.tbody.find_all("tr"):
            tr_list = []
            for tag_c in tag.find_all("td"):
                tr_list.append(tag_c.string)
            paiming_list.append(tr_list)
        return (paiming_list)
    elif type == "dict":
        paiming_dict = {}  # 返回字典
        for tag in soup.tbody.find_all("tr"):
            tr_list = []
            for tag_c in tag.find_all("td"):
                tr_list.append(tag_c.string)
            paiming_dict[tr_list[1]] = tr_list
        return (paiming_dict)
    else:
        print("\033[1;31m输出类型选择错误，请检查！\033[0m")


if __name__ == "__main__":
    years = [2019, 2018, 2017, 2016]
    url = "http://www.zuihaodaxue.com/Greater_China_Ranking{}_0.html"

    for year in years:
        locals()["dict_{}".format(year)] = paiming_get(url, year)

    print(("\033[1;30;43m {:^20}\t" + "{:<10}\t" * len(years)+"\033[0m").format("院校名称", *years))

    for key, value in locals()["dict_{}".format(years[0])].items():
        values = []
        values.append(value[0])
        for year in years[1:]:

            if key in locals()["dict_{}".format(year)].keys():
                values.append(locals()["dict_{}".format(year)][key][0])
            else:
                values.append("-")
        format_values = ""
        for i in range(0, len(years)):
            format_values += "{" + str(i + 2) + ":<10}\t"
        # print(format_values)
        print(("{0:{1}<16}\t" + format_values).format(key, chr(12288), *values))
