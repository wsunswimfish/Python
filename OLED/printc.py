# 用于在终端输出带颜色的文本信息

'''
Print显示彩色
开头部分： \033[显示方式; 前景色 ; 背景色 m
结尾部分： \033[0m

字体颜色	背景颜色	颜色描述
30	40	白色
31	41	红色
32	42	绿色
33	43	黃色
34	44	蓝色
35	45	紫红色
36	46	青蓝色
37	47	灰色

显示方式	效果
0	终端默认设置
1	高亮显示
4	使用下划线
5	闪烁
7	反白显示
8	不可见
'''


def printc(text, front="black", back="white", mode="default"):
    color = {"black": [30, 40], "red": [31, 41], "green": [32, 42], "yellow": [33, 43], "blue": [34, 44],
             "magenta": [35, 45], "cyan": [36, 46], "white": [37, 47]}

    display_mode = {"default": 0, "bold": 1, "underscore": 4, "blink": 5, "reverse": 7, "concealed": 8}

    # print("",end=" ")   #效果对比展示
    # for key in display_mode.keys():
    #     print("{:-^16}".format(key),end="")
    # print("")
    # for i in range(30,38):
    #     for ii in range(40,48):
    #         text=""
    #         for value in display_mode.values():
    #             text+="\033[{};{};{}m  文字{}  背景{}  \033[0m".format(value,i,ii,i,ii)
    #         print(text)
    # print("")

    print("\033[{};{};{}m{}\033[0m".format(display_mode[mode], color[front][0], color[back][1], text))


if __name__ == "__main__":
    printc("这是一段彩色演示文本", "black", "cyan")
