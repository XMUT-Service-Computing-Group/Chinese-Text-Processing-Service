# Chinese-Text-Processing-Service
Author: Kaixiang Lin, Weisi Chen

Owned by: Service Computing Research Group, School of Software Engineering, Xiamen University of Technology

This service offers functions to conduct text processing for Simplified Chinese. The current version has functions to generate key words and sentiment scores for any given text dataset.

通过增加停用词和用户自定义词库，优化snownlp分词效果，从而提升snownlp情感判断准确率。

##### 1.增加停用词：

对snownlp中-normal文件夹中-stopwords.txt进行补充

##### 2.增加用户自定义词库：

修改snownlp文件夹下的__init__.py ：

```python
import jieba  #导入jieba包


class SnowNLP(object):
    def words(self):
        return jieba.lcut(self.doc)  # 替换为jieba的lcut方法
    def summary(self, limit=5):
        doc = []
        sents = self.sentences
        for sent in sents:
            words = jieba.lcut(sent)  # 替换为jieba的lcut方法
            words = normal.filter_stop(words)
            doc.append(words)
        rank = textrank.TextRank(doc)
        rank.solve()
        ret = []
        for index in rank.top_index(limit):
            ret.append(sents[index])
        return ret

    def keywords(self, limit=5, merge=False):
        doc = []
        sents = self.sentences
        for sent in sents:
            words = jieba.lcut(sent)  # 替换为jieba的lcut方法
            words = normal.filter_stop(words)
            doc.append(words)
        rank = textrank.KeywordTextRank(doc)
        rank.solve()
        ret = []
        for w in rank.top_index(limit):
            ret.append(w)
        if merge:
            wm = words_merge.SimpleMerge(self.doc, ret)
            return wm.merge()
        return ret
```

修改snownlp中sentiment文件夹下的__init__.py ：

```python
import jieba  #导入jieba包
jieba.load_userdict('words.txt')  # 加载自定义词库(路径自定义)


class Sentiment(object):
    def handle(self, doc):
        words = jieba.lcut(doc)  # 替换为jieba的lcut方法
        words = normal.filter_stop(words)
        return words
```

```python
import jieba
```

导入jieba包时显示以下文字即是导入正常

Building prefix dict from the default dictionary ...
Loading model from cache C:\Users\xkz\AppData\Local\Temp\jieba.cache
Loading model cost 0.659 seconds.
Prefix dict has been built successfully.