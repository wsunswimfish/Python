import datetime
import random
import time
from time import sleep

from sense_hat import SenseHat


def show_info(sense):
    print("\n{:=^40}".format("SenseHat传感器"))
    print("{:^40}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("温度：{:5.2f}℃   (从湿度传感器：{:5.2f}℃   从气压传感器：{:5.2f}℃)".format(sense.get_temperature(),
                                                                                   sense.get_temperature_from_humidity(),
                                                                                   sense.get_temperature_from_pressure()))
    print("湿度：{:5.2f}％".format(sense.get_humidity()))
    print("气压：{:5.2f}mbar\n".format(sense.get_pressure()))

    print("磁力仪方向：{:5.2f}".format(sense.get_compass()))
    print("重力加速度：X:{x:5.2f} Y:{y:5.2f}  Z:{z:5.2f}\n".format(**sense.get_accelerometer_raw()))

    print("get_orientation   yaw:{yaw:6.2f}  pitch:{pitch:6.2f}  roll:{roll:6.2f}".format(**sense.get_orientation()))
    print("get_accelerometer yaw:{yaw:6.2f}  pitch:{pitch:6.2f}  roll:{roll:6.2f}".format(**sense.get_accelerometer()))
    print("get_gyroscope     yaw:{yaw:6.2f}  pitch:{pitch:6.2f}  roll:{roll:6.2f}".format(**sense.get_gyroscope()))

    accel = sense.get_accelerometer_raw()


def check_time():
    if (time.gmtime().tm_hour < 9 and time.gmtime().tm_hour >= 0) or time.gmtime().tm_hour >= 23:
        return (True)
    else:
        return (False)


def rgb(rgb=["r", "g", "b"]):
    # 无限循环RGB顺序
    yield rgb
    while True:
        rgb.append(rgb.pop(0))
        yield rgb


def jb_rgb_1(sense):
    # 演示RGB循环渐变，R-G-B
    # R降G升 G降B升 B将R升 往复循环

    sense.clear()
    r, g, b = 255, 0, 0
    t = 0.01

    try:

        while 1:
            show_info(sense)

            for r in range(255, 0, -1):
                sense.set_pixels([(r, g, b)] * 64)
                r -= 1
                g += 1
                sleep(t)

            for g in range(255, 0, -1):
                sense.set_pixels([(r, g, b)] * 64)
                g -= 1
                b += 1
                sleep(t)

            for b in range(255, 0, -1):
                sense.set_pixels([(r, g, b)] * 64)
                b -= 1
                r += 1
                sleep(t)

    except KeyboardInterrupt:
        print("程序被终止！")

    finally:
        sense.clear()


def jb_rgb_2(sense):
    # 演示RGB循环渐变，R-G-B
    # R,G,B 初始值(255,0,0)
    # R→,G↗,B→  演变为(255,255,0)
    # R↘,G→,B→  演变为(0,255,0)
    # R→,G→,B↗  演变为(0,255,255)
    # R→,G↘,B→  演变为(0,0,255)
    # R↗,G→,B→  演变为(255,0,255)
    # R→,G→,B↘  演变为(255,0,0)

    t = 0.008
    rgb_s = rgb()

    try:
        for rgb_i in rgb_s:
            show_info(sense)

            exec("{} = 255".format(rgb_i[0]))
            exec("{} ,{}  = 0 ,0".format(rgb_i[1], rgb_i[2]))

            for i in range(0, 255):
                sense.set_pixels([(eval("r"), eval("g"), eval("b"))] * 64)
                exec("{} += 1".format(rgb_i[1]))
                sleep(t)
            for i in range(255, 0, -1):
                sense.set_pixels([(eval("r"), eval("g"), eval("b"))] * 64)
                exec("{} -= 1".format(rgb_i[0]))
                sleep(t)

    except KeyboardInterrupt:
        print("程序被终止！")

    finally:
        sense.clear()


def jb_rgb_3(sense):
    # 演示RGB循环渐变，R-G-B 0-2初始值(255,0,0) 3-4初始值(0,255,0) 5-7初始值(0,0,255)
    # R,G,B 初始值(255,0,0)
    # R→,G↗,B→  演变为(255,255,0)
    # R↘,G→,B→  演变为(0,255,0)
    # R→,G→,B↗  演变为(0,255,255)
    # R→,G↘,B→  演变为(0,0,255)
    # R↗,G→,B→  演变为(255,0,255)
    # R→,G→,B↘  演变为(255,0,0)

    t = 0.003
    rgb_s_1 = rgb(["r", "g", "b"])
    rgb_s_2 = rgb(["g", "b", "r"])
    rgb_s_3 = rgb(["b", "r", "g"])

    try:
        while 1:

            show_info(sense)

            if check_time():
                print(1)
                sense.clear()
                sleep(60)
                continue
            rgb_s_1_i = next(rgb_s_1)
            rgb_s_2_i = next(rgb_s_2)
            rgb_s_3_i = next(rgb_s_3)

            exec("{}_1 = 255".format(rgb_s_1_i[0]))
            exec("{}_1 ,{}_1  = 0 ,0".format(rgb_s_1_i[1], rgb_s_1_i[2]))

            exec("{}_2 = 255".format(rgb_s_2_i[0]))
            exec("{}_2 ,{}_2  = 0 ,0".format(rgb_s_2_i[1], rgb_s_2_i[2]))

            exec("{}_3 = 255".format(rgb_s_3_i[0]))
            exec("{}_3 ,{}_3  = 0 ,0".format(rgb_s_3_i[1], rgb_s_3_i[2]))

            for i in range(0, 255):
                pixels = [(eval("r_1"), eval("g_1"), eval("b_1"))] * 24 + [
                    (eval("r_2"), eval("g_2"), eval("b_2"))] * 16 + [(eval("r_3"), eval("g_3"), eval("b_3"))] * 24
                sense.set_pixels(pixels)
                exec("{}_1 += 1".format(rgb_s_1_i[1]))
                exec("{}_2 += 1".format(rgb_s_2_i[1]))
                exec("{}_3 += 1".format(rgb_s_3_i[1]))
                sleep(t)
            for i in range(255, 0, -1):
                pixels = [(eval("r_1"), eval("g_1"), eval("b_1"))] * 24 + [
                    (eval("r_2"), eval("g_2"), eval("b_2"))] * 16 + [(eval("r_3"), eval("g_3"), eval("b_3"))] * 24
                sense.set_pixels(pixels)
                exec("{}_1 -= 1".format(rgb_s_1_i[0]))
                exec("{}_2 -= 1".format(rgb_s_2_i[0]))
                exec("{}_3 -= 1".format(rgb_s_3_i[0]))
                sleep(t)

    except KeyboardInterrupt:
        print("程序被终止！")

    finally:
        sense.clear()


def jb_rgb_4(sense):
    # 演示彩虹色依次循环
    # 赤橙黄绿青蓝紫
    pixels_list = [[(255, 0, 0)] * 8,
                   [(255, 165, 0)] * 8,
                   [(255, 255, 0)] * 8,
                   [(0, 255, 0)] * 8,
                   [(0, 127, 255)] * 8,
                   [(0, 0, 255)] * 8,
                   [(139, 0, 255)] * 8,
                   [(255, 0, 255)] * 8]

    t = 0.2
    print(len(pixels_list))
    try:
        while 1:

            pixels = []
            for i in pixels_list:
                pixels += i
            sense.set_pixels(pixels)
            pixels_list.append(pixels_list.pop(0))
            sleep(t)
            # sense.set_rotation(90)

    except KeyboardInterrupt:
        print("程序被终止！")

    finally:
        sense.clear()


def jb_rgb_5(sense):
    # 演示整体彩虹色渐变循环
    # 赤橙黄绿青蓝紫
    pixels_list = [(255, 0, 0),
                   (255, 165, 0),
                   (255, 255, 0),
                   (0, 255, 0),
                   (0, 127, 255),
                   (0, 0, 255),
                   (139, 0, 255)]

    t = 0.01
    r, g, b = 255, 0, 0
    try:

        while 1:

            if (r, g, b) == (255, 0, 0):
                # print("\n赤-橙-黄")
                for i in range(0, 255):
                    sense.clear((r, g, b))
                    g += 1
                    sleep(t)
                print(r, g, b)

            elif (r, g, b) == (255, 255, 0):
                # print("\n黄-绿")
                for i in range(0, 255):
                    sense.clear((r, g, b))
                    r -= 1
                    sleep(t)
                print(r, g, b)

            elif (r, g, b) == (0, 255, 0):
                # print("\n绿-青")
                for i in range(0, 128):
                    sense.clear((r, g, b))
                    g -= 1
                    b += 2
                    sleep(t)
                b = 255
                print(r, g, b)
            elif (r, g, b) == (0, 127, 255):
                # print("\n青-兰")
                for i in range(0, 127):
                    sense.clear((r, g, b))
                    g -= 1
                    sleep(t)
                print(r, g, b)

            elif (r, g, b) == (0, 0, 255):
                # print("\n兰-紫")
                for i in range(0, 127):
                    sense.clear((r, g, b))
                    r += 1
                    sleep(t)
                print(r, g, b)

            elif (r, g, b) == (127, 0, 255):
                # print("\n紫-红")
                for i in range(0, 128):
                    sense.clear((r, g, b))
                    r += 1
                    b -= 2
                    sleep(t)
                b = 0
                print(r, g, b)



    except KeyboardInterrupt:
        print("程序被终止！")

    finally:
        sense.clear()

def round_rgb_dot(sense):
    r,g,b = 0,0,0
    x,y = 0 ,0
    sense.clear(r,g,b)
    t=0.01

    while 1:
        r, g, b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
        x,y =random.randint(0,7), random.randint(0,7)
        sense.set_pixel(x, y, r, g, b)
        sleep(t)
        # sense.clear()


if __name__ == "__main__":
    sense = SenseHat()
    sense.low_light=True

    # jb_rgb_1(sense)
    # jb_rgb_2(sense)
    jb_rgb_3(sense)
    # jb_rgb_4(sense)
    # jb_rgb_5(sense)
    # round_rgb_dot(sense)
