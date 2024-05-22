import time
import jieba, imageio, os, re
import wordcloud as wd
import numpy as np
import pandas as pd
from collections import Counter


def read_stop_word(stop_word_file=[]):  # 从stop_word文件夹读取指定的停止词文件
    # print(stop_word_file_name)
    stop_word_list = []
    for i in stop_word_file:
        with open(os.path.join(os.getcwd(), "stop_word", i), "r", encoding="utf8") as fp:
            stop_word_list.extend(fp.read().split("\n"))
    stop_word_list = list(set(stop_word_list))
    return (stop_word_list)


def read_file(file_name="", stop_word_list=[]):  # 从file文件夹读取需要制作图云的文本文件并进行分词处理，返回词频字典
    # 读取文本内容
    with open(os.path.join(os.getcwd(), "file", file_name), mode="r", encoding="utf8") as fp:  # 读取文本
        print("正在进行文本读取...", end=" ")
        word_text = fp.read()
        print("{}".format(len(word_text)))

    # 去除特殊字符
    print("正在进行特殊字符处理...", end=" ")
    word_text = re.sub("\W", "", word_text)
    print("{}".format(len(word_text)))

    # 文本分词
    print("正在进行文本分词...", end=" ")
    # star_t = time.perf_counter()
    # jieba.enable_parallel()
    word_list = jieba.lcut(word_text)
    # print(time.perf_counter() - star_t, end=" ")
    print("{}".format(len(word_list)))

    # # 分词后续处理-1
    # print("正在进行分词处理...", end=" ")
    # del_list = list(set([i for i in range(len(word_list)) if
    #                      len(word_list[i]) < 2 or word_list[i] in stop_word_list]))  # 构建长度小于2和停止词的删除列表
    # word_list = list(np.delete(np.array(word_list), del_list))  # 去除删除的新词列表
    # word_list.sort()
    # print("{}".format(len(word_list)))

    # # 分词后续处理-2
    # print("正在进行分词处理...", end=" ")
    # star_t=time.perf_counter()
    # word_list_array=np.array(word_list)
    # word_list = [i for i in word_list_array if len(i)>=2 and i not in stop_word_list]  # 去除删除的新词列表
    # word_list.sort()
    # print(time.perf_counter()-star_t, end=" ")
    # print("{}".format(len(word_list)))

    # 分词后续处理-3
    print("正在进行分词处理...", end=" ")
    star_t = time.perf_counter()
    word_pd=pd.DataFrame(word_list,columns=["word"])
    word_pd_new=word_pd[(word_pd["word"].str.len()>=2) & (~word_pd["word"].isin(stop_word_list))]
    word_list=word_pd_new["word"].to_list()
    word_list.sort()
    print(time.perf_counter() - star_t, end=" ")
    print("{}".format(len(word_list)))


    # 分词后词频统计
    print("正在分词统计...", end=" ")
    word_dic = dict(Counter(word_list))
    print(sorted(word_dic.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[:10])

    # return(word_list)
    return (word_dic)


def gen_wordcloud(file_name, mask_file, out_file="out.png", stop_word_file=[], stop_word_list=[], font_file="msyh.ttc"):
    stop_word_list.extend(read_stop_word(stop_word_file))
    # word_list=read_file(file_name,stop_word_list)
    word_dic = read_file(file_name, stop_word_list)
    mask = imageio.imread(os.path.join(os.getcwd(), "mask", mask_file))
    font_file = os.path.join(os.getcwd(), "font", font_file)
    color_func = wd.ImageColorGenerator(mask)
    w = wd.WordCloud(font_path=font_file,
                     # width=1600,
                     # height=800,
                     scale=1,
                     # stopwords=stop_word_list,
                     max_words=2000,
                     background_color=None,
                     mode='RGBA',
                     mask=mask,
                     color_func=color_func,
                     prefer_horizontal=0.9,
                     margin=2,
                     # collocations=False,
                     # contour_width = 0,  # (float)mask轮廓线宽。若mask不为空且此项值大于0，就绘制出mask轮廓 (default=0)
                     # contour_color = 'black'
                     )

    # wl=" ".join(word_list)

    print("正在进行词云生成...")
    w.generate_from_frequencies(word_dic)
    print("正在进行词云输出...")
    w.to_file(os.path.join(os.getcwd(), "out", out_file))
    # im=Image.open(os.path.join(os.getcwd(),"out",out_file))
    # im.show()

    wm = w.to_image()
    wm.show()


if __name__ == "__main__":
    file_name = "笑傲江湖.txt"
    mask_file = "mask1.png"
    out_png = "outpng.png"
    stop_word_file = ["baidu_stop_word.txt", "cn_stop_word.txt", "hit_stop_word.txt", "scu_stop_word.txt"]
    stop_word_list = ["你们", "我们", "他们", "它们", "说道", "一声", "心中"]
    font_file = "msyh.ttc"

    gen_wordcloud(file_name, mask_file, out_png, stop_word_file, stop_word_list, font_file)
