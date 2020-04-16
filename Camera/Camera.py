import os,time,picamera

from picamera import PiCamera

camera = PiCamera()
camera.resolution = (2592,1944) #picamera的原始尺寸
camera.vflip= True
camera.hflip= True

pho_num = 240
time_sleep = 60
try:
    print("开始拍摄，共拍摄{}张，间隔{}秒，约需{}分钟...\n".format(pho_num,time_sleep,pho_num*time_sleep/60))
    for i in range(pho_num):
        camera.capture("{}.jpg".format(time.strftime("%Y%m%d%H%M%S",time.localtime())))
        print("第{}张照片拍摄完毕。".format(i+1))
        if i != pho_num-1: time.sleep(time_sleep)
except:
    print("拍摄过程异常！")
else:
    print("\n全部照片拍摄完毕！")
finally:
    camera.close()
    print("\n拍摄过程结束！")



