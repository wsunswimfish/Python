import pyttsx3
import schedule
import time
from printc import printc


def sch_coffeebreak(text="茶歇时间，请休息一会，站起来活动一下。"):
    printc(text, "black", "cyan")
    # pyttsx3.speak(text)

def job():
    printc("茶歇时间，请休息一会，站起来活动一下。", "black", "cyan")
    # pyttsx3.speak(text)

def main():
    try:
        # schedule.every().day.at("10:00").do(job)

        schedule.every(2).seconds.do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        pass
    finally:
        # schedule.cancel_job()
        pass


# if __name__ == "__main__":
main()
