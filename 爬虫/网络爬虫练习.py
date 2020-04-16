import requests

# # 普通网页爬取
# url = "http://www.163.com"
# user_agent = {"User-agent": "Mozilla/5.0"}
#
# try:
#     r = requests.get(url, headers=user_agent)
#     print("网页URL:{}\n网页Headers:{}\n网页头编码:{}\n网页编码:{}".format(r.request.url, \
#                                                              str(r.request.headers), \
#                                                              r.encoding, \
#                                                              r.apparent_encoding))
#     r.raise_for_status()
#     print("网页爬取长度:{}\n网页内容缩略:{} ...".format(len(r.text), r.text[500:1000]))
# except:
#     print("网页爬取失败！")


# 搜索引擎爬取
url = "http://www.sogou.com/web"
keyword = "python"
user_agent = {"User-agent": "Mozilla/5.0"}

try:
    kv = {"query": keyword}
    r = requests.get(url, params= kv, headers= user_agent)
    print("网页URL:{}\n网页Headers:{}\n网页头编码:{}\n网页编码:{}".format(r.request.url, \
                                                             str(r.request.headers), \
                                                             r.encoding, \
                                                             r.apparent_encoding))
    r.raise_for_status()
    print("网页爬取长度:{}\n网页内容缩略:{} ...".format(len(r.text), r.text[500:1000]))
except:
    print("网页爬取失败！")
