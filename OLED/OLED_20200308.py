
# 控制树莓派OLED显示
from PIL import Image, ImageDraw, ImageFont
import os, time, requests, json
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306


def get_weather(city="101120601"):
    try:
        # r = requests.get('http://wthrcdn.etouch.cn/weather_mini?city={}'.format(city))
        # data = r.json()
        # weather=data['data']['forecast'][0]
        # weather["fengli"]=weather["fengli"][weather["fengli"].find("CDATA")+6:-3]
        # weather["nowtmp"]=data["data"]["wendu"]+"℃"
        # weather_info="{date}, 天气{type}, {fengxiang}{fengli}, {high}, {low}, 当前温度{nowtmp}".format(**weather)

        r = requests.get("http://api.help.bj.cn/apis/weather/?id={}".format(city))
        weather = r.json()

        if int(weather["pm25"]) >= 250:
            weather["pm25_info"] = "严重污染"
        elif int(weather["pm25"]) >= 150:
            weather["pm25_info"] = "重度污染"
        elif int(weather["pm25"]) >= 115:
            weather["pm25_info"] = "中度污染"
        elif int(weather["pm25"]) >= 75:
            weather["pm25_info"] = "轻度污染"
        elif int(weather["pm25"]) >= 35:
            weather["pm25_info"] = "良"
        else :
            weather["pm25_info"] = "优"

        weather_info="{today},{city},{weather},{wd}{wdforce}," \
                     "当前温度{temp}℃,湿度{humidity},气压{stp}百帕,能见度{wisib}," \
                     "PM2.5指数{pm25}μg/m³,空气质量{pm25_info}".format(**weather)

        return (weather_info)
    except:
        print("天气参数获取失败!")
        return("天气参数获取失败!")


def get_oil_price():
    try:
        r = requests.get("http://api.help.bj.cn/apis/youjia")
        oil_price = r.json()
        oil_price_info="{} {}, 92号汽油{}元, 95号汽油{}元, 98号汽油{}元, 0号柴油{}元".format(oil_price["update"],*oil_price["data"][15])
        return (oil_price_info)
    except:
        print("油价参数获取失败!")
        return("油价参数获取失败!")


def get_datetime():
    return (time.strftime("%Y-%m-%d %H:%M %A", time.localtime()))

def get_uptime():
    with os.popen("uptime") as fo:
        uptime = fo.readline()
        uptime_info=uptime[uptime.find("up"):uptime.find(",")]
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


if __name__ == "__main__":
    # 引脚配置，按照上面的接线来配置
    RST = 17
    DC = 22
    # 因为连的是CE0，这里的PORT和DEVICE也设置为0
    SPI_PORT = 0
    SPI_DEVICE = 0
    #
    # 根据自己的oled型号进行初始化，我的是128X64、SPI的oled，使用SSD1306_128_64初始化
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
    #
    disp.begin()
    disp.clear()
    disp.display()  # 清屏

    try:
        print("\rOLED显示中....CTRL+C退出！", end="")
        im = get_image()
        dr = get_draw(im)

        time_time=60
        time_weather=3600
        
        while 1:

            dr.rectangle([0, 15, 127, 63], fill=0)
            #           dr.text([0,48],get_datetime(), font=get_font()[0], fill=1)
            dr.text([66, 16], "{:^5}".format(get_datetime().split()[1]), font=get_font(26)[0], fill=1)
            dr.text([66, 40], "{:^10}".format(get_datetime().split()[2]), font=get_font()[0], fill=1)
            dr.text([66, 52], "{:^10}".format(get_datetime().split()[0]), font=get_font()[0], fill=1)

            text_loop = [get_uptime(),
                     "CPU温度:{:.0f}℃, GPU温度:{}".format(get_cpu_temp(),get_gpu_temp()),
                     "内存:{0[0]}, 使用:{0[1]}, 空闲:{0[2]}".format(get_memory()),
                     get_weather(),
                     get_oil_price()]

            for m in text_loop:
                for n in range(127, -len(m) * 7, -1):
                    dr.rectangle([0, 0, 127, 15], fill=1)
                    dr.text([n, 0], m, font=get_font()[1], fill=0)
                    # ~ im.show()
                    # ~ input()
                    disp.image(im)
                    disp.display()
                    # ~ time.sleep(time_time)

    except KeyboardInterrupt:
        disp.clear()
        disp.display()
        del dr
        del im
