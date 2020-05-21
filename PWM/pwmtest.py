# RaspBerry LED PWM 呼吸灯 示例
# 呼吸序列的产生均为一元二次方程产生
# 吸气 y= 占空比 - abs(x**n)
# 呼气 y= abs(x**n)
# n越大吸气和呼气的开始越快
# x取值从(-占空比**(1/n),0)

import time
import numpy as np
import RPi.GPIO as GPIO


def gpio_setup(channels, mode=GPIO.BOARD, channels_mode=GPIO.OUT):
    # 定义GPIO工作模式，针脚定义，针脚工作模式
    if GPIO.getmode() is None:
        GPIO.setmode(mode)
    for pin in channels:
        GPIO.setup(pin, channels_mode)


def led_breath(channels, dutycycle_list, frequency=50):
    # 呼吸灯定义
    for pin in channels:
        pwm["pwm" + str(pin)] = GPIO.PWM(pin, frequency)
        pwm["pwm" + str(pin)].start(1)

    while True:
        for i in dutycycle_list:
            for pin in pins:
                pwm["pwm" + str(pin)].ChangeDutyCycle(i)
            #                time.sleep(0.1)
            time.sleep(1 / frequency)


def breath_list(cycle=3, frequency=50, dutycycle=100, ratio=1 / 2, n=3):
    # 根据呼吸函数产生数据序列
    # cycle(周期)  frequency(频率)   dutycycle(占空比) ratio(呼、吸时长比例) n(n阶函数)
    # 吸序列生成
    xx_list = np.linspace(-dutycycle**(1 / n), 1,
                          int(cycle / (1 + 1 / ratio) * frequency))
    xy_list = np.around(dutycycle - abs(xx_list**n), decimals=1)
    # 呼序列生成
    hx_list = np.linspace(-dutycycle**(1 / n), -1,
                          int(cycle / (1 + ratio) * frequency))
    hy_list = np.around(abs(hx_list**n), decimals=1)
    # 合成呼吸序列
    dutycycle_list = list(xy_list) + list(hy_list)
    # print(dutycycle_list)
    return(dutycycle_list)


if __name__ == "__main__":
    pins = [40]
    gpio_setup(pins, GPIO.BOARD, GPIO.OUT)

    try:
        pwm = globals()
        led_breath(pins, breath_list())
    except KeyboardInterrupt:
        for pin in pins:
            pwm["pwm" + str(pin)].stop()
        GPIO.cleanup()

# pwm = locals()
