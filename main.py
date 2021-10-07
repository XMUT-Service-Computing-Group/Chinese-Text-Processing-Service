import os
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
from tkinter import *

import pandas
from snownlp import SnowNLP


# 选择csv文件
def select_csv():
    filepathLabel.set(tkf.askopenfilename(title="", filetypes=[('csv文件', '.csv')]))  # 获取文件完整路径
    if filepathLabel.get() != "":  # 修改两个按钮的可用性参数为可用
        keyButton.config(state=NORMAL)
        SenButton.config(state=NORMAL)


# 生成关键词文件
def key_words(filename, limit, method):
    if method == 0:
        text = []  # 储存关键词列数据
        data = pandas.read_csv(filename, index_col=0)  # 读取csv文件并不使用编号
        for i in range(0, len(data)):
            text.append(SnowNLP(data.index[i]))  # 将data的第一列（index）数据转换为SnowNLP类型并添加到text数组中
            text[i] = text[i].keywords(limit)  # 将text数组中的数据进行关键词提取并覆盖到原位置
        data["关键词"] = text  # 将text数组作为新的一列添加到data中
        data.to_csv(os.path.basename(filename).split('.')[0] + "Key.csv")  # 将data输出为读取的csv文件名加上Key的csv文件
        tkm.showinfo("成功！", "生成关键词文件成功！")
        return data


def sentiment_value(filename, method):
    if method == 0:
        text = []  # 储存情绪值列数据
        data = pandas.read_csv(filename, index_col=0)  # 读取csv文件并不使用编号
        for i in range(0, len(data)):
            text.append(SnowNLP(data.index[i]))  # 将data的第一列（index）数据转换为SnowNLP类型并添加到text数组中
            text[i] = text[i].sentiments  # 将text数组中的数据进行情绪值判断并覆盖到原位置
        data["情绪值"] = text  # 将text数组作为新的一列添加到data中
        data.to_csv(os.path.basename(filename).split('.')[0] + "Sen.csv")  # 将data输出为读取的csv文件名加上Sen的csv文件
        tkm.showinfo("成功！", "生成情绪值文件成功！")
        return data


root = tk.Tk()
root.title("CTPS")
filepathLabel = tk.StringVar()
keyLimit = tk.StringVar()
keyMethod = tk.StringVar()
SenMethod = tk.StringVar()
# 四个从界面中获得的属性值

Button(root, text='打开文件', command=select_csv).grid(row=1, column=0, padx=5, pady=5)
Label(root, textvariable=filepathLabel).grid(row=1, column=1, columnspan=4, padx=5, pady=5)
keyButton = Button(root, text='生成关键词', state=DISABLED,
                   command=lambda: key_words(filepathLabel.get(), int(keyLimit.get()) if keyLimit.get() != "" else 5,
                                             int(keyMethod.get()) if keyMethod.get() != "" else 0))
keyButton.grid(row=2, column=0, padx=5, pady=5)
Entry(root, width=5, textvariable=keyLimit).grid(row=3, column=0, padx=5, pady=5)
Label(root, text="关键词数量限制，默认为5").grid(row=3, column=1, padx=5, pady=5)
Entry(root, width=5, textvariable=keyMethod).grid(row=4, column=0, padx=5, pady=5)
Label(root, text="生成模式，默认为0").grid(row=4, column=1, padx=5, pady=5)
SenButton = Button(root, text='生成情绪值', state=DISABLED,
                   command=lambda: sentiment_value(filepathLabel.get(),
                                                   int(SenMethod.get()) if SenMethod.get() != "" else 0))
SenButton.grid(row=5, column=0, padx=5, pady=5)
Entry(root, width=5, textvariable=SenMethod).grid(row=6, column=0, padx=5, pady=5)
Label(root, text="生成模式，默认为0").grid(row=6, column=1, padx=5, pady=5)

root.mainloop()

