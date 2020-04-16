import pyttsx3

# voices
# 25  name:Mei-Jia     languages:['zh_TW']  age:35  gender:VoiceGenderFemale
# 36  name:Sin-ji      languages:['zh_HK']  age:35  gender:VoiceGenderFemale
# 39  name:Ting-Ting   languages:['zh_CN']  age:35  gender:VoiceGenderFemale

def say_init(voice=25, rate=200, volume=100):
    # 初始化引擎
    engine = pyttsx3.init()
    # rate = engine.getProperty("rate")
    # volume = engine.getProperty("volume")
    engine.setProperty("rate", rate)
    engine.setProperty("voice", engine.getProperty("voices")[voice].id)
    print("阅读语速设置：{}  阅读音量设置：{}".format(rate, volume))
    return (engine)


def say(engine, text="info.txt"):
    # 阅读文本
    try:
        with open(text, "r", encoding="utf8") as f:
            # f_info = f.readlines()
            f_info = f.read()
            f_info = f_info.split("。")
            for i in f_info:
                engine.say(i)
                print(i)
                engine.runAndWait()
    except KeyboardInterrupt:
        engine.say("阅读异常中断！")
        engine.runAndWait()
    else:
        engine.say("全部文本阅读完毕！")
        engine.runAndWait()
    finally:
        pyttsx3.speak("本次阅读结束！")


if __name__ == "__main__":
    engine = say_init(rate=150)
    say(engine, "info.txt")

