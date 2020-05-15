#RaspBerry LED PWM 呼吸灯 示例

import time
import numpy as np
import RPi.GPIO as GPIO


def gpio_setup(channels, mode=GPIO.BOARD, channels_mode=GPIO.OUT):
    #定义GPIO工作模式，针脚定义，针脚工作模式
    if GPIO.getmode() is None:
        GPIO.setmode(mode)
    for pin in channels:
        GPIO.setup(pin, channels_mode)


def led_breath(channels, dutycycle_list):
    #呼吸灯定义
    for pin in channels:
        pwm["pwm" + str(pin)] = GPIO.PWM(pin, frequency)
        pwm["pwm" + str(pin)].start(1)

    while True:
        for i in dutycycle_list:
            for pin in pins:
                pwm["pwm" + str(pin)].ChangeDutyCycle(i)
            #                time.sleep(0.1)
            #time.sleep(0.16)

def breath_list(cycle=3,frequency=50,dutycycle=100,ratio=1/2):
    #根据呼吸函数产生数据序列
    # cycle(周期)  frequency(频率)   dutycycle(占空比) ratio(呼、吸时长比例)
    b_list=[]
    #吸序列生成
    xx_list=np.linspace(-10,0,cycle/(1+1/ratio)*frequency)
    xy_list=(-xx_list**2)+dutycycle
    #呼序列生成
    hx_list=np.linspace(0,10,cycle/(1+ratio)*frequency)
    hy_list=(hx_list-dutycycle*0.5)**2
    #合成呼吸序列
    dutycycle_list=list(xy_list)+list(hy_list)
    return(dutycycle_list)

if __name__ == "__main__":
    pins = [33, 35, 37]
    gpio_setup(pins, GPIO.BOARD, GPIO.OUT)

    try:
        pwm = globals()
        led_breath(pins,breath_list())
    except KeyboardInterrupt:
        for pin in pins:
            pwm["pwm" + str(pin)].stop()
        GPIO.cleanup()

pwm = locals()
