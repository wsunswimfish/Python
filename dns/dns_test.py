# 用于进行域名解析的压力测试
import random
import time

import dns.resolver  # pip install dnspython

st = time.perf_counter()
i = 1
n = 30
re = dns.resolver.Resolver()
re.nameservers = ["127.0.0.1"]
name = ["www.baidu.com", "www.qq.com", "www.126.com", "www.163.com",
        "www.cctv.com", "www.sgcc.com.cn", "11.11.cn", "1.1cn", "2.2cn", "3.3cn"]

while i <= n:
    domain = name[random.randint(0, len(name)-1)]
    try:
        answer = re.resolve(domain, "A", raise_on_no_answer=False, lifetime=6)
    except:
        print("{:<10}   NAME:{:<20}    查询无结果".format(i, domain))
    else:
        for ipval in answer:
            print("{:<10}   NAME:{:<20}    IP:{}".format(
                i, answer.qname.to_text(), ipval.to_text()))
    finally:
        i += 1
        time.sleep(0.01)

et = time.perf_counter()
print("共耗时{}秒".format(et-st))
