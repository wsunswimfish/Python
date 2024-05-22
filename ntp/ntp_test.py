import ntplib
from time import ctime


ntp_client=ntplib.NTPClient()


n=0

while 1 :
    n+=1
    respones = ntp_client.request("ntp.aliyun.com").tx_time
    print("{:10.0f} return time : {}".format(n,ctime(respones)))