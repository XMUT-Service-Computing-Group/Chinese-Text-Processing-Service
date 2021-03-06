# Chinese-Text-Processing-Service

This service offers functions to conduct text processing for Simplified Chinese. The current version has functions to
generate key words and sentiment scores for any given text dataset.

### Preparation 准备工作

#### 1.Make changes to SnowNLP package 修改SnowNLP

Purpose: to enhance its performance by introducing jieba and adding stopwords and a customised lexicon.  
目的：通过增加停用词和用户自定义词库，引入jieba分词，提升snownlp情感分析的准确率。

1. Replace the stopwords.txt in the "normal" folder of the snownlp package with the one in this repo.  
   将snownlp包的“normal”文件夹中的stopwords.txt替换为此repo中的stopwords.txt。
2. Add the words.txt in this repo to the "sentiment" folder of the snownlp package.   
   将此repo中的words.txt添加到snownlp包的“sentiment”文件夹中。
3. Make slight modifications on two .py files in the snownlp package as follows:  
   对snownlp包中的两个.py文件进行如下轻微修改：

> snownlp/\_\_init\_\_.py

```python
import jieba  # Import Jieba package. 导入jieba包


class SnowNLP(object):
    def words(self):
        return jieba.lcut(self.doc)  # Replace with the lcut method of Jieba. 替换为jieba的lcut方法

    def summary(self, limit=5):
        doc = []
        sents = self.sentences
        for sent in sents:
            words = jieba.lcut(sent)  # Replace with the lcut method of Jieba. 替换为jieba的lcut方法
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
            words = jieba.lcut(sent)  # Replace with the lcut method of Jieba. 替换为jieba的lcut方法
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

> snownlp/sentiment/\_\_init\_\_.py

```python
import jieba  # Import Jieba package. 导入jieba包

jieba.load_userdict(r'C:\Users\xkz\anaconda3\envs\python39\Lib\site-packages\snownlp\sentiment\words.txt')


# Load custom Thesaurus (The path needs to be changed to where you put the words.txt file).
# 加载自定义词库(路径需要修改成你放置words.txt文件的位置)


class Sentiment(object):
    def handle(self, doc):
        words = jieba.lcut(doc)  # Replace with the lcut method of Jieba. 替换为jieba的lcut方法
        words = normal.filter_stop(words)
        return words
```

#### 2.Add the following folder in the project root directory 在项目根目录添加如下文件夹

> input/

​	 The default folder for input files. 默认的存放输入文件的文件夹。

> ~~output/~~

​	~~The default folder for output files.  默认的存放输出文件的文件夹。~~

> training_data/

​	The default folder for training data files.  默认的存放训练数据文件的文件夹。

> trained_model/

​	The default folder for training model files.  默认的存放训练模型文件的文件夹。

Note: if you do not want to add input ~~and output files~~, it is also allowed, but the name parameter cannot be used in
the URL. You need to use the path parameter and assign it to the path of the complete input ~~and output~~
files (described in detail below).   
注意：如果你不想添加input~~和output文件~~也是允许的，但在url中，name参数将无法使用，需要使用path参数，并将它赋值为完整的输入~~和输出~~文件的路径。

###  How to use 如何使用

#### 1.函数

| Method 方法        | Description 说明                                             |
| ------------------ | :----------------------------------------------------------- |
| key_words()        | Use the snownlp built-in method to get the keyword of the text.<br>使用snownlp内置方法获得文本的关键字 |
| sentiment_train()  | Use the snownlp built-in method to train the model that generates sentiment score.<br>使用snownlp内置方法训练情绪值生成的模型 |
| sentiment_scores() | generates sentiment score.<br>生成情绪值                     |

#### 2.API调用

| URL                                             | parameter 参数                                               |
| ----------------------------------------------- | ------------------------------------------------------------ |
| http://127.0.0.1:5000/                          |                                                              |
| http://127.0.0.1:5000/key_words?path=           | **path**<br/>Absolute path of the file.<br/>文件的绝对路径   |
| http://127.0.0.1:5000/key_words?name=           | **name**<br/>Name of the file.<br/>文件的文件名              |
| http://127.0.0.1:5000/key_words?limit=          | **limit**<br/>Number limit of keywords.<br/>关键词的数量限制 |
| http://127.0.0.1:5000/sentiment_train?filename= | **filename**<br/>File name of the training model.<br/>训练模型的文件名 |
| http://127.0.0.1:5000/sentiment_scores?path=    | **path**<br>Absolute path of the file.<br>文件的绝对路径     |
| http://127.0.0.1:5000/sentiment_scores?name=    | **name**<br/>Name of the file.<br/>文件的文件名              |
| http://127.0.0.1:5000/sentiment_scores?method=  | **method**<br/>Generation mode of sentiment score.<br/>情绪值的生成模式 |
|                                                 |                                                              |

##### Example 范例：

##### http://127.0.0.1:5000/key_words?name=data.csv&limit=3

It means that the keyword of data in data.csv in the input folder is generated under the condition of quantity limit 3, and returned in JSON format.<br>表示以数量限制3为条件，生成位于input文件夹中的data.csv中数据的关键词，并以json的格式返回。
