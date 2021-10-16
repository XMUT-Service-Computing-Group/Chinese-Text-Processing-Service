# **coding:utf-8**
import json
from collections import defaultdict

import jieba
import pandas
from flask import request
from snownlp import SnowNLP, sentiment


# 获得csv文件数据
def get_data():
    # 获取传入的params参数
    params = request.args.to_dict()
    path = params.get('path')
    name = params.get('name')
    if path is not None and name is not None:
        return 'path和name参数不能同时存在'
    elif path is not None and name is None:
        data = pandas.read_csv(path, index_col=0)  # 读取csv文件并不带编号
        return data
    elif name is not None and path is None:
        data = pandas.read_csv('input/' + name, index_col=0)  # 读取csv文件并不带编号
        return data


# 关键词（API）
def key_words():
    result_json = []  # 创建保存数据的list
    data = get_data()  # 获得csv文件数据
    if data == 'path和name参数不能同时存在':
        return data
    # 获取传入的params参数
    params = request.args.to_dict()
    limit = params.get('limit')

    for i in range(0, len(data)):
        temp = {'key': data.index[i], 'words': SnowNLP(data.index[i]).keywords(limit)}  # 将数据保存在一个dict中
        result_json.append(temp)  # 将dict中的数据添加到list中
    return json.dumps(result_json, ensure_ascii=False)


# 情绪值开始

# jieba分词后去除停用词
def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    stopwords = set()
    with open('dictionary/method2_stopwords.txt', 'r', encoding='utf-8') as fr:
        for i in fr:
            stopwords.add(i.strip())
    return list(filter(lambda x: x not in stopwords, seg_result))


# 找出文本中的情感词、否定词和程度副词
def classify_words(word_list):
    sen_file = open('dictionary/method2_bosondict.txt', 'r+', encoding='utf-8')  # 读取情感词典文件
    sen_list = sen_file.readlines()  # 获取词典文件内容
    sen_dict = defaultdict()  # 创建情感词典的字典
    # 读取词典每一行的内容，将其转换成字典对象
    for i in sen_list:
        if len(i.split(' ')) == 2:
            sen_dict[i.split(' ')[0]] = i.split(' ')[1]
    # 读取否定词文件
    not_word_file = open('dictionary/method2_negativewords.txt', 'r+', encoding='utf-8')
    not_word_list = not_word_file.readlines()
    # 读取程度副词文件
    degree_file = open('dictionary/method2_degreeadv.txt', 'r+', encoding='utf-8')
    degree_list = degree_file.readlines()
    degree_dict = defaultdict()
    for i in degree_list:
        degree_dict[i.split(',')[0]] = i.split(',')[1]

    sen_word = dict()
    not_word = dict()
    degree_word = dict()
    for i in range(len(word_list)):
        word = word_list[i]
        # 找出分词结果中在情感字典且不在否定词和程度副词中的词
        if word in sen_dict.keys() and word not in not_word_list and word not in degree_dict.keys():
            sen_word[i] = sen_dict[word]
        # 分词结果中在否定词中的词
        elif word in not_word_list and word not in degree_dict.keys():
            not_word[i] = -1
        # 分词结果中在程度副词中的词
        elif word in degree_dict.keys():
            degree_word[i] = degree_dict[word]
    # 关闭打开的文件
    sen_file.close()
    not_word_file.close()
    degree_file.close()
    # 返回分类结果
    return sen_word, not_word, degree_word


# 计算情绪值
def calculate_score(sen_word, not_word, degree_word, seg_result):
    W = 1  # 权重初始化为1
    score = 0  # 情绪值初始化
    sentiment_index = -1  # 情感词下标初始化
    sentiment_index_list = list(sen_word.keys())  # 情感词的位置下标集合
    # 遍历分词结果
    for i in range(0, len(seg_result)):
        # 如果是情感词
        if i in sen_word.keys():
            score += W * float(sen_word[i])  # 权重*情感词得分
            sentiment_index += 1  # 情感词下标加一，获取下一个情感词的位置
            if sentiment_index < len(sentiment_index_list) - 1:
                # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                for j in range(sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index + 1]):
                    # 更新权重，如果有否定词，权重取反
                    if j in not_word.keys():
                        W *= -1
                    elif j in degree_word.keys():
                        W *= float(degree_word[j])
        # 定位到下一个情感词
        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score


# 计算单句情绪值
def sentiment_score(sentence):
    seg_list = seg_word(sentence)  # 对文档分词
    sen_word, not_word, degree_word = classify_words(seg_list)  # 将分词结果转换成字典，找出情感词、否定词和程度副词
    score = calculate_score(sen_word, not_word, degree_word, seg_list)  # 计算情绪值
    return score


# 训练snownlp的情绪值模型（API）
def sentiment_train():
    # 获取传入的params参数
    params = request.args.to_dict()
    if params.get('filename') is None:
        filename = 'sentiment.marshal'
    else:
        filename = params.get('filename')
    sentiment.train(r'training_data/neg.csv', r'training_data/pos.csv')
    sentiment.save(r'trained_model/' + filename)
    return "成功输出训练模型文件！"


# 汇总所有情绪值（API）
def sentiment_scores():
    # 获取传入的params参数
    params = request.args.to_dict()
    method = params.get('method')
    result_json = []
    data = get_data()
    score = 0
    if isinstance(data, str):
        return data
    for i in range(0, len(data)):
        if method == "1":
            score = sentiment_score(data.index[i])
        elif method == "2":
            score = SnowNLP(data.index[i]).sentiments
        elif method is None:
            return "参数缺失"
        temp = {'key': data.index[i], 'score': score}
        result_json.append(temp)
    return json.dumps(result_json, ensure_ascii=False)

# 情绪值结束
