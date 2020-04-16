#

import time

import RPi.GPIO as GPIO


def gpio_setup(channels, mode=GPIO.BOARD, channels_mode=GPIO.OUT):
    if GPIO.getmode() is None:
        GPIO.setmode(mode)
    for pin in channels:
        GPIO.setup(pin, channels_mode)


def led_breath(channels, frequency=2000):
    for pin in channels:
        pwm["pwm" + str(pin)] = GPIO.PWM(pin, frequency)
        pwm["pwm" + str(pin)].start(1)
    dutycycle_list = [abs(x ** 3) * 100 / 20 ** 3 +
                      0.16 for x in range(-19, 20)]
    while True:
        for i in dutycycle_list:
            for pin in pins:
                pwm["pwm" + str(pin)].ChangeDutyCycle(i)
            #                time.sleep(0.1)
            time.sleep(0.16)


if __name__ == "__main__":
    pins = [33, 35, 37]
    gpio_setup(pins, GPIO.BOARD, GPIO.OUT)

    try:
        pwm = globals()
        led_breath(pins)
    except KeyboardInterrupt:
        for pin in pins:
            pwm["pwm" + str(pin)].stop()
        GPIO.cleanup()

pwm = locals()

# for pin  in pins:
#    pwm["pwm"+str(pin)]=GPIO.PWM(pin,1000)
#    pwm["pwm"+str(pin)].start(1)
#
# try:
#    while 1:
#        for i in range(1,100,5):
#            for pin in pins:
#                pwm["pwm"+str(pin)].ChangeDutyCycle(i)
#            time.sleep(0.05)
#        for i in range(100,0,-5):
#            for pin in pins:
#                pwm["pwm"+str(pin)].ChangeDutyCycle(i)
#            time.sleep(0.05)
# except KeyboardInterrupt:
#    for pin in pins:
#        pwm["pwm"+str(pin)].stop()
#    GPIO.cleanup()
