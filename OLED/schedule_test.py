import time

import pyttsx3
import schedule
from printc import printc


def sch_coffeebreak(text="茶歇时间，请休息一会，站起来活动一下。"):
    printc(text, "black", "cyan")
    # pyttsx3.speak(text)


def job(text="消息提示！"):
    printc(text + "  {}".format(time.strftime("%H:%M:%S", time.localtime())), "black", "cyan")
    pyttsx3.speak(text)


def main():
    shichen_dic = {"name": ['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时'],
                   "name1": ['夜半', '鸡鸣', '平旦', '日出', '食时', '隅中', '日中', '日昳', '晡时', '日入', '黄昏', '人定'],
                   "clock": ['23:00', '01:00', '03:00', '05:00', '07:00', '09:00', '11:00', '13:00', '15:00', '17:00',
                             '19:00', '21:00'],
                   "gengdian": ["三更", "四更", "五更", "", "", "", "", "", "", "", "一更", "二更"],
                   "say":["","","","","","","","","","","",""]}
    shichen = "子丑寅卯辰巳午未申酉戌亥"
    shichen_time = ["{:0>2}:00".format(i * 2 - 1) if i != 0 else "23:00" for i in range(12)]
    try:
        for i in range(12):
            schedule.every().day.at(shichen_dic["clock"][i]).do(job, (
                "{} {} {}".format(shichen_dic["name"][i], shichen_dic["name1"][i], shichen_dic["gengdian"][i])))

        schedule.every().day.at("08:30").do(job, "一天的工作时间开始了！")
        schedule.every().day.at("10:00").do(job, "站起来活动活动，休息一下！")
        schedule.every().day.at("12:00").do(job, "午餐时间到！")
        schedule.every().day.at("12:30").do(job, "中午休息一会吧！")
        schedule.every().day.at("13:30").do(job, "下午工作时间开始了！")
        schedule.every().day.at("15:00").do(job, "休息一下，补充点水分吧！")
        schedule.every().day.at("17:30").do(job, "一天工作时间结束，下班了！")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        printc("程序异常终止!", "red", "white")
    finally:
        schedule.clear()


if __name__ == "__main__":
    main()
