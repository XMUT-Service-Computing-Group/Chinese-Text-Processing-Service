# **coding:utf-8**

from NLPfunctions import *


def main():
    print("-------------------------")
    print("\t1.关键词生成\n\t2.情绪值判断\n\t3.退出")
    print("-------------------------")
    func = input("请选择功能：")
    if func == "1":
        print("-------------------------")
        print("\t1.snownlp生成")
        print("-------------------------")
        method = input("请选择生成模式：")
        limit = input("请限制关键词数量：")
        if key_words(filepath, limit, method) is not None:
            print("生成关键词文件成功")
    elif func == "2":
        print("-------------------------")
        print("\t1.snownlp\n\t2.玻森情感词典")
        print("-------------------------")
        method = input("请选择生成模式：")
        if sentiment_value(filepath, method) is not None:
            print("生成情绪值文件成功")
    elif func == "3":
        print("退出")
        exit()
    main()


if __name__ == '__main__':
    jieba.setLogLevel(jieba.logging.INFO)  # 加这一句可以不显示Building prefix dict from the default dictionary的错误提示
    print("欢迎使用中文文本处理服务……")
    print("-------------------------")
    print("\t1.选择csv文件")
    print("-------------------------")
    func = input("请选择功能：")
    if func == "1":
        filepath = select_csv()
    main()
