
import jieba,imageio,os
import wordcloud as wd
import numpy as np



def read_stop_word(stop_word_file=[]): #从stop_word文件夹读取指定的停止词文件
    # print(stop_word_file_name)
    stop_word_list=["不是","不能","不过","不好","不会","不知",
                    "他们","咱们","我们","你们","自己",
                    "一个","一声",
                    "知道","甚么","什么","怎么"]
    for i in stop_word_file:
        with open(os.path.join(os.getcwd(),"stop_word",i),"r",encoding="utf8") as fp:
            stop_word_list.extend(fp.read().split("\n"))
    stop_word_list=list(set(stop_word_list))
    return(stop_word_list)

def read_file(file_name=""):    #从file文件夹读取需要制作图云的文本文件并进行分词处理
    ##生成词组列表及相关处理
    print("正在进行文本内容读取...")
    # jieba.enable_parallel(4)

    with open(os.path.join(os.getcwd(),"file",file_name), mode="r", encoding="utf8") as fp:
        print("正在进行文本分词...",end=" ")
        word_list = jieba.lcut(fp.read())
        print("{}".format(len(word_list)))

    print("正在进行分词处理...",end=" ")
    del_list = list(set([i for i in range(len(word_list)) if len(word_list[i])<2]))    #构建长度小于2的删除列表
    word_list = list(np.delete(np.array(word_list), del_list))  #去除删除的新词列表
    word_list.sort()
    print("{}".format(len(word_list)))
    return(word_list)

def gen_wordcloud(file_name,mask_file,stop_word_file=[],out_file="out.png",font_file="msyh.ttc"):
    word_list=read_file(file_name)
    mask = imageio.imread(os.path.join(os.getcwd(),"mask",mask_file))
    stop_word_list=read_stop_word(stop_word_file)
    font_file=os.path.join(os.getcwd(),"font",font_file)
    color_func=wd.ImageColorGenerator(mask)
    w = wd.WordCloud(font_path=font_file,
                     # width=1600,
                     # height=800,
                     scale=1,
                     # stopwords=stop_word_list,
                     max_words=2000,
                     background_color=None,
                     mode = 'RGBA',
                     mask=mask,
                     color_func=color_func,
                     prefer_horizontal=0.9,
                     # margin=2,
                     collocations=False,
                     contour_width = 0,  # (float)mask轮廓线宽。若mask不为空且此项值大于0，就绘制出mask轮廓 (default=0)
                     contour_color = 'black'

    )
    wl=" ".join(word_list)
    print("正在进行词云生成...")
    w.generate(wl)
    print("正在进行词云输出...")
    w.to_file(os.path.join(os.getcwd(),"out",out_file))
    # im=Image.open(os.path.join(os.getcwd(),"out",out_file))
    # im.show()

    wm=w.to_image()
    wm.show()

if __name__=="__main__":

    file_name="鹿鼎记.txt"
    mask_file="mask1.png"
    out_png="outpng.png"
    stop_word_file=["baidu_stop_word.txt","cn_stop_word.txt","hit_stop_word.txt","scu_stop_word.txt"]
    stop_word_file=[]
    font_file="msyh.ttc"

    gen_wordcloud(file_name,mask_file,stop_word_file,out_png,font_file)



