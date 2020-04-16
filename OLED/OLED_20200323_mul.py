# 控制树莓派OLED显示
import os
import time
from threading import Thread
# import schedule

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import requests
from PIL import Image, ImageDraw, ImageFont


def printc(text, front="white", back="black", mode="default"):
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

    color = {"black": [30, 40], "red": [31, 41], "green": [32, 42], "yellow": [33, 43], "blue": [34, 44],
             "magenta": [35, 45], "cyan": [36, 46], "white": [37, 47]}

    display_mode = {"default": 0, "bold": 1, "underscore": 4, "blink": 5, "reverse": 7, "concealed": 8}

    print("\033[{};{};{}m{}\033[0m".format(display_mode[mode], color[front][0], color[back][1], text))


def get_weather(city="101120601"):
    try:
        # r = requests.get('http://wthrcdn.etouch.cn/weather_mini?city={}'.format(city))
        # data = r.json()
        # weather=data['data']['forecast'][0]
        # weather["fengli"]=weather["fengli"][weather["fengli"].find("CDATA")+6:-3]
        # weather["nowtmp"]=data["data"]["wendu"]+"℃"
        # weather_info="{date}, 天气{type}, {fengxiang}{fengli}, {high}, {low}, 当前温度{nowtmp}".format(**weather)
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(
            "http://api.help.bj.cn/apis/weather/?id={}".format(city),
            headers=headers)
        weather = r.json()

        weather_dic = {"优": [0, 35], "良": [35, 75], "轻度污染": [75, 115], "中度污染": [115, 150], "重度污染": [150, 250],
                       "严重污染": [250, 1000]}

        for key, value in weather_dic.items():
            if int(weather["pm25"]) in range(value[0], value[-1]):
                weather["pm25_info"] = key
                break

        weather_info = "{today},{city},{weather},{wd}{wdforce}," \
                       "当前温度{temp}℃,湿度{humidity},气压{stp}百帕,能见度{wisib}," \
                       "PM2.5指数{pm25}μg/m³,空气质量{pm25_info}".format(**weather)

        return (weather_info)
    except BaseException:
        printc("天气参数获取失败!","red","black","flash")
        return ("天气参数获取失败!")


def get_oil_price():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("http://api.help.bj.cn/apis/youjia", headers=headers)
        oil_price = r.json()
        oil_price_info = "{} {}, 92号汽油{}元, 95号汽油{}元, 98号汽油{}元, 0号柴油{}元".format(
            oil_price["update"], *oil_price["data"][15])
        return (oil_price_info)
    except BaseException:
        printc("油价参数获取失败!","red","black","flash")
        return ("油价参数获取失败!")


def get_datetime():
    return (time.strftime("%Y-%m-%d %H:%M %A", time.localtime()))


def get_uptime():
    with os.popen("uptime") as fo:
        uptime = fo.readline()
        uptime_info = uptime[uptime.find("up"):uptime.find(",")]
    return (uptime_info)


def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as fo:
        temp = int(fo.read()) / 1000
    return (temp)
    # return(56.6)


def get_gpu_temp():
    with os.popen("vcgencmd measure_temp") as fo:
        temp = fo.readline().replace("temp=", "")
    return (temp)
    # return(52.7)


def get_memory():  # return [total,used,free]
    with os.popen("free -t --mega") as fo:
        memory = fo.readlines()[3].split()[1:]
    return (memory)
    # return([5218,5316,2107])


def get_image(mode="1", size=(128, 64), color=0):
    image = Image.new(mode, size, color)
    # image=Image.open("image.bmp","r")
    return (image)


def get_draw(image):
    draw = ImageDraw.Draw(image)
    return (draw)


def get_font(font_size=12):
    font = []
    font.append(ImageFont.truetype("calibri.ttf", font_size))
    font.append(ImageFont.truetype("msyhl.ttc", font_size))
    return (font)


def disp_title():
    try:
        while 1:
            text_loop = [
                get_uptime(), "CPU温度:{:.0f}℃, GPU温度:{}".format(
                    get_cpu_temp(), get_gpu_temp()), "内存:{0[0]}, 使用:{0[1]}, 空闲:{0[2]}".format(
                    get_memory()), get_weather(), get_oil_price()]

            with open("info.txt", "r", encoding="utf-8") as f:
                for ltext in f.readlines():
                    text_loop.append(ltext)

            for m in text_loop:
                for n in range(127, -len(m) * 7, -1):
                    dr.rectangle([0, 0, 127, 15], fill=1)
                    dr.text([n, 0], m, font=get_font()[1], fill=0)
                    # ~ im.show()
                    disp.image(im)
                    disp.display()
    except BaseException:
        printc("滚动信息显示错误!","yellow","black")


def disp_content(time_refresh_contenct=60):
    try:
        counters = 15
        while 1:
            if counters == 15:

                counters = 0
                weather_info = get_weather()
                if weather_info != "天气参数获取失败!":
                    dr.rectangle([0, 16, 63, 63], fill=0)
                    dr.text([0, 16], "{:^5}".format(weather_info.split(
                        ",")[2]), font=get_font(23)[1], fill=1)
                    dr.text([0, 52], "{:^10}".format(weather_info.split(
                        ",")[4][4:]), font=get_font(10)[1], fill=1)
                    dr.text([30, 52], "{:^5}".format(weather_info.split(
                        ",")[5][2:]), font=get_font(10)[1], fill=1)
            counters += 1
            dr.rectangle([63, 16, 127, 63], fill=0)
            dr.text([66, 16], "{:^5}".format(
                get_datetime().split()[1]), font=get_font(26)[0], fill=1)
            dr.text([66, 40], "{:^10}".format(
                get_datetime().split()[2]), font=get_font()[0], fill=1)
            dr.text([66, 52], "{:^10}".format(
                get_datetime().split()[0]), font=get_font()[0], fill=1)
            # disp.image(im)
            # disp.display()
            # print("内容刷新")

            time.sleep(time_refresh_contenct)
    except BaseException:
        printc("内容显示错误!","yellow","black")


if __name__ == "__main__":
    # 引脚配置，按照上面的接线来配置
    RST = 17
    DC = 22
    # 因为连的是CE0，这里的PORT和DEVICE也设置为0
    SPI_PORT = 0
    SPI_DEVICE = 0
    #
    # 根据自己的oled型号进行初始化，我的是128X64、SPI的oled，使用SSD1306_128_64初始化
    disp = Adafruit_SSD1306.SSD1306_128_64(
        rst=RST, dc=DC, spi=SPI.SpiDev(
            SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
    #
    disp.begin()
    disp.clear()
    disp.display()  # 清屏

    try:
        printc("\rOLED显示中....CTRL+C退出！","white","teal","highlight")
        im = get_image()
        dr = get_draw(im)

        time_refresh_contenct = 60

        p1 = Thread(target=disp_content, args=(time_refresh_contenct,))
        p2 = Thread(target=disp_title)
        p1.start()
        p2.start()
        p1.join()
        p2.join()

    except KeyboardInterrupt:
        printc("显示被终止！","white","teal","highlight")

    finally:
        disp.clear()
        disp.display()
        del dr
        del im
