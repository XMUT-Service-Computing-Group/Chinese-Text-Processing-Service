# **coding:utf-8**
import os
import tkinter.filedialog as tkf
from tkinter import *

import jieba
import pandas
from snownlp import SnowNLP


# 选择csv文件
def select_csv():
    root = Tk()
    root.withdraw()  # 实现主窗口隐藏
    path = tkf.askopenfilename(title="", filetypes=[('csv文件', '.csv')])  # 获得文件路径
    print("您选择的csv文件是：" + os.path.basename(path))  # 输出文件名
    return path


# 生成关键词文件
def key_words(filename, limit, method):
    text = []  # 储存关键词列数据
    name = os.path.basename(filename).split('.')[0]  # 提取不包含后缀的文件名
    data = pandas.read_csv(filename, index_col=0)  # 读取csv文件并不带编号
    if method == "1":
        for i in range(0, len(data)):
            text.append(SnowNLP(data.index[i]))  # 将data的第一列（index）数据转换为SnowNLP类型并添加到text数组中
            text[i] = text[i].keywords(int(limit))  # 将text数组中的数据进行关键词提取并覆盖到原位置
    data["关键词"] = text  # 将text数组作为新的一列添加到data中
    data.to_csv("output/" + name + "Key.csv")  # 将data输出为读取的csv文件名加上Key的csv文件
    return data


# 生成情绪值文件
def sentiment_value(filename, method):
    name = os.path.basename(filename).split('.')[0]  # 提取不包含后缀的文件名
    data = pandas.read_csv(filename, index_col=0)  # 读取csv文件并不带编号
    if method == "1":  # 使用snownlp内置方法
        text = []  # 储存情绪值列数据
        for i in range(0, len(data)):
            text.append(SnowNLP(data.index[i]))  # 将data的第一列（index）数据转换为SnowNLP类型并添加到text数组中
            text[i] = text[i].sentiments  # 将text数组中的数据进行情绪值判断并覆盖到原位置
        # tkm.showinfo("成功！", "生成情绪值文件成功！")
    if method == "2":  # 使用玻森情感词典
        text = []  # 储存情绪值列数据
        df = pandas.read_table(r"BosonNLP.txt", sep=" ", names=['key', 'score'])  # 加载玻森情感词典
        key = df['key'].values.tolist()  # 读取词典中的key列
        score = df['score'].values.tolist()  # 读取词典中的score列
        for i in range(0, len(data)):
            segs = jieba.lcut(data.index[i])  # 使用jieba分词对data的每一行数据进行分词
            score_list = [score[key.index(x)] for x in segs if (x in key)]  # 将分词结果和key进行比对并获得出对应的score
            text.append(sum(score_list))  # 将每个分词结果的分值相加
    data["情绪值"] = text  # 将text数组作为新的一列添加到data中
    data.to_csv("output/" + name + "Sen.csv")  # 将data输出为读取的csv文件名加上Sen的csv文件
    return data
