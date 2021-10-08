# Chinese-Text-Processing-Service
Author: Kaixiang Lin, Weisi Chen

Owned by: Service Computing Research Group, School of Software Engineering, Xiamen University of Technology

This service offers functions to conduct text processing for Simplified Chinese. The current version has functions to generate key words and sentiment scores for any given text dataset.

### Preparation 准备工作

#### Make changes to SnowNLP package 修改SnowNLP
Purpose: to enhance its performance by introducing jieba and adding stopwords and a customised lexicon.
目的：通过增加停用词和用户自定义词库，引入jieba分词，提升snownlp情感分析的准确率。

1. Replace the stopwords.txt in the "normal" folder of the snownlp package with the one in this repo.
2. Add the words.txt in this repo to the "sentiment" folder of the snownlp package.
3. Adjust the code accordingly:

"__init__.py" in the snownlp folder

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

"__init__.py" in the sentiment folder of the snownlp package:

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

The following messages indicates loading successfully when importing the jieba package:

    Building prefix dict from the default dictionary ...
    Loading model from cache C:\Users\xkz\AppData\Local\Temp\jieba.cache
    Loading model cost 0.659 seconds.
    Prefix dict has been built successfully.
