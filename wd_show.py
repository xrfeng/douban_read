import warnings
warnings.filterwarnings("ignore")
import re
import jieba
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0,5.0)
from wordcloud import WordCloud#词云包

def wd_show(str):
    # 去除字符串中的所有标点
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filter_str = re.findall(pattern, str)
    cleaned_str = ''.join(filter_str)

    jieba.load_userdict('userdict.txt')
    segment = jieba.lcut(cleaned_str)
    words_df = pd.DataFrame({'segment': segment})
    # print(words_df)
    stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                            encoding='gbk')  # quoting=3全不引用
    # print(stopwords)
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": np.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)

    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=100)
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}

    wordcloud = wordcloud.fit_words(word_frequence)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    with open('./novel/黑暗之门.txt','r',encoding='gbk') as f:
        str = f.read()
    wd_show(str)