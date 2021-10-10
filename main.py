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

    # filepathLabel.set(tkf.askopenfilename(title="", filetypes=[('csv文件', '.csv')]))  # 获取文件完整路径
    # if filepathLabel.get() != "":  # 修改两个按钮的可用性参数为可用
    #     keyButton.config(state=NORMAL)
    #     SenButton.config(state=NORMAL)


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
        # tkm.showinfo("成功！", "生成关键词文件成功！")
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
        df = pandas.read_table(r"BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])  # 加载玻森情感词典
        key = df['key'].values.tolist()  # 读取词典中的key列
        score = df['score'].values.tolist()  # 读取词典中的score列
        for i in range(0, len(data)):
            segs = jieba.lcut(data.index[i])  # 使用jieba分词对data的每一行数据进行分词
            score_list = [score[key.index(x)] for x in segs if (x in key)]  # 将分词结果和key进行比对并获得出对应的score
            text.append(sum(score_list))  # 将每个分词结果的分值相加
    data["情绪值"] = text  # 将text数组作为新的一列添加到data中
    data.to_csv("output/" + name + "Sen.csv")  # 将data输出为读取的csv文件名加上Sen的csv文件
    return data


if __name__ == '__main__':
    jieba.setLogLevel(jieba.logging.INFO)  # 加这一句可以不显示Building prefix dict from the default dictionary的错误提示
    print("欢迎使用中文文本处理服务……")
    print("-------------------------")
    print("\t1.选择csv文件")
    print("-------------------------")
    func1 = input("请选择功能：")
    if func1 == "1":
        filepath = select_csv()
    print("-------------------------")
    print("\t1.关键词生成\n\t2.情绪值判断")
    print("-------------------------")
    func2 = input("请选择功能：")
    if func2 == "1":
        print("\t1.snownlp生成")
        method = input("请选择生成模式：")
        limit = input("请限制关键词数量：")
        if key_words(filepath, limit, method) is not None:
            print("生成关键词文件成功")
    elif func2 == "2":
        print("\t1.snownlp\n\t2.玻森情感词典")
        method = input("请选择生成模式：")
        if sentiment_value(filepath, method) is not None:
            print("生成情绪值文件成功")
    # table = PrettyTable(["1.关键词生成", "2.情绪值判断"])
    # print(table)

# root = tk.Tk()
# root.title("CTPS")
# filepathLabel = tk.StringVar()
# keyLimit = tk.StringVar()
# keyMethod = tk.StringVar()
# SenMethod = tk.StringVar()
# # 四个从界面中获得的属性值
#
# Button(root, text='打开文件', command=select_csv).grid(row=1, column=0, padx=5, pady=5)
# Label(root, textvariable=filepathLabel).grid(row=1, column=1, columnspan=4, padx=5, pady=5)
# keyButton = Button(root, text='生成关键词', state=DISABLED,
#                    command=lambda: key_words(filepathLabel.get(), int(keyLimit.get()) if keyLimit.get() != "" else 5,
#                                              int(keyMethod.get()) if keyMethod.get() != "" else 0))
# keyButton.grid(row=2, column=0, padx=5, pady=5)
# Entry(root, width=5, textvariable=keyLimit).grid(row=3, column=0, padx=5, pady=5)
# Label(root, text="关键词数量限制，默认为5").grid(row=3, column=1, padx=5, pady=5)
# Entry(root, width=5, textvariable=keyMethod).grid(row=4, column=0, padx=5, pady=5)
# Label(root, text="生成模式，默认为0").grid(row=4, column=1, padx=5, pady=5)
# SenButton = Button(root, text='生成情绪值', state=DISABLED,
#                    command=lambda: sentiment_value(filepathLabel.get(),
#                                                    int(SenMethod.get()) if SenMethod.get() != "" else 0))
# SenButton.grid(row=5, column=0, padx=5, pady=5)
# Entry(root, width=5, textvariable=SenMethod).grid(row=6, column=0, padx=5, pady=5)
# Label(root, text="生成模式，默认为0").grid(row=6, column=1, padx=5, pady=5)
#
# root.mainloop()
