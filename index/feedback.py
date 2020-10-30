# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 01:34:36 2020

@author: 92385
"""

import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import xlrd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
import jieba.posseg as pseg
import joblib
import os

SVMModelName = "svclassifier.m"


def dataClean():
    # 语料集
    validData = []
    invalidData = []

    dataMeipai = xlrd.open_workbook('meipai.xlsx')
    dataVivo = xlrd.open_workbook('vivo.xlsx')

    sheelData = dataVivo.sheet_by_index(0)
    for rowI in range(1, sheelData.nrows):
        seg_list = jieba.cut(str(sheelData.cell(rowI, 9).value), cut_all=True)
        if (sheelData.cell(rowI, 11).value == 1):
            validData.append("".join(seg_list))
        else:
            invalidData.append("".join(seg_list))

    sheelData = dataMeipai.sheet_by_index(0)
    for rowI in range(1, sheelData.nrows):
        seg_list = jieba.cut(str(sheelData.cell(rowI, 9).value), cut_all=True)
        if (sheelData.cell(rowI, 15).value == 1):
            validData.append("".join(seg_list))
        else:
            invalidData.append("".join(seg_list))

    return validData, invalidData


def cleanData():
    # 基本思路，重点是过滤无效反馈，留下有效反馈，所以对无法判断是否为有效反馈的时候（没有该词向量）
    # 则默认为有效反馈
    validData, invalidData = dataClean()

    # 创建dataFrame
    df = pd.DataFrame(columns=["ascii", "nums", "word", "class"])  # 创建一个空的dataframe
    df.loc[0] = [1, 2, 3, 4]
    dfi = 0

    ascllData = [chr(i) for i in range(0, 47)]
    ascllData.extend(chr(i) for i in range(58, 127))
    ascllData.extend(['！', '@', '#', '¥', '%', '（', '）', '—', '【', '】', '「', '」',
                      '｜', '、', '；', '：', '‘', '“', '？', '《', '》', '，', '。'])
    numData = [chr(i) for i in range(48, 57)]

    allInvalid = 0

    newInvalidData = []

    # 有效
    for dataI in validData:
        dfi_data = []
        countAscall = 0
        countNum = 0
        allCount = 1
        # 逐个词分割
        for splitI in list(dataI):
            # 是否在ascall内
            allCount += 1
            if splitI in ascllData:
                countAscall += 1
            if splitI in numData:
                countNum += 1

        words = pseg.cut(dataI)
        flagCount = 0
        for word, flag in words:
            # print('%s %s' % (word, flag))
            flagCount = flagCount + 1
        rates = flagCount / (len(dataI) + 1e-10)

        dfi_data.append(countAscall / allCount)
        dfi_data.append(countNum / allCount)
        dfi_data.append(rates)
        dfi_data.append('1')

        df.loc[dfi] = dfi_data
        dfi = dfi + 1
        # 判断后输出
        if (countAscall / allCount > 1 / 3):
            allInvalid += 1
            # print(dataI)
            # print(countAscall/allCount)
            newInvalidData.append(dataI)

    # 无效分析
    for dataI in invalidData:
        dfi_data = []
        countAscall = 0
        countNum = 0
        allCount = 1
        # 逐个词分割
        for splitI in list(dataI):
            # 是否在ascall内
            allCount += 1
            if splitI in ascllData:
                countAscall += 1
            if splitI in numData:
                countNum += 1
        words = pseg.cut(dataI)
        flagCount = 0
        for word, flag in words:
            # print('%s %s' % (word, flag))
            flagCount = flagCount + 1
        rates = flagCount / (len(dataI) + 1e-10)

        # 判断后输出
        if (countAscall / allCount < 1):
            allInvalid += 1

            dfi_data.append(countAscall / allCount)
            dfi_data.append(countNum / allCount)
            dfi_data.append(rates)
            dfi_data.append('0')

            df.loc[dfi] = dfi_data
            dfi = dfi + 1

            newInvalidData.append(dataI)
    return df


def getFeature(myStr):
    # 基本思路，重点是过滤无效反馈，留下有效反馈，所以对无法判断是否为有效反馈的时候（没有该词向量）
    # 则默认为有效反馈
    dataI = myStr

    # 创建dataFrame
    df = pd.DataFrame(columns=["ascii", "nums", "word"])  # 创建一个空的dataframe
    df.loc[0] = [1, 2, 3]
    dfi = 0

    ascllData = [chr(i) for i in range(0, 47)]
    ascllData.extend(chr(i) for i in range(58, 127))
    ascllData.extend(['！', '@', '#', '¥', '%', '（', '）', '—', '【', '】', '「', '」',
                      '｜', '、', '；', '：', '‘', '“', '？', '《', '》', '，', '。'])
    numData = [chr(i) for i in range(48, 57)]

    dfi_data = []
    countAscall = 0
    countNum = 0
    allCount = 1
    # 逐个词分割
    for splitI in list(dataI):
        # 是否在ascall内
        allCount += 1
        if splitI in ascllData:
            countAscall += 1
        if splitI in numData:
            countNum += 1

    words = pseg.cut(dataI)
    flagCount = 0
    for word, flag in words:
        # print('%s %s' % (word, flag))
        flagCount = flagCount + 1
    rates = flagCount / (len(dataI) + 1e-10)

    dfi_data.append(countAscall / allCount)
    dfi_data.append(countNum / allCount)
    dfi_data.append(rates)

    df.loc[dfi] = dfi_data

    return df


# 责任链头
def dealWithOne(myStr):
    # --------------------------------------------第一层过滤--------------------------------------------
    ascllData = [chr(i) for i in range(0, 47)]
    ascllData.extend(chr(i) for i in range(58, 127))
    ascllData.extend(['！', '@', '#', '¥', '%', '（', '）', '—', '【', '】', '「', '」',
                      '｜', '、', '；', '：', '‘', '“', '？', '《', '》', '，', '。'])
    numData = [chr(i) for i in range(48, 57)]

    # 参数
    res = True
    countAscall = 0
    countNum = 0
    allCount = 1
    # 逐个词分割
    for splitI in list(myStr):
        # 是否在ascall内
        allCount += 1
        if splitI in ascllData:
            countAscall += 1
        if splitI in numData:
            countNum += 1
    # 判断后输出
    if countAscall / allCount > 1 / 3 or countNum / allCount > 1 / 2:
        res = False

    if res:
        return dealWithTow(myStr)
    else:
        return res


def dealWithTow(myStr):
    # --------------------------------------------第二层过滤--------------------------------------------
    res = True

    words = pseg.cut(myStr)
    flagCount = 0
    for word, flag in words:
        # print('%s %s' % (word, flag))
        flagCount = flagCount + 1
    rates = flagCount / (len(myStr) + 1e-10)
    if rates > 0.9:
        res = False

    return res


def dealWithSVM(myStr):
    res = False
    print(os.path.exists(SVMModelName))
    if os.path.exists(SVMModelName) is False:
        fitSVM()

    print('svclassifier' in dir())
    if ('svclassifier' in dir()) is False:
        global svclassifier
        svclassifier = joblib.load(SVMModelName)

    y_pred = svclassifier.predict(getFeature(myStr))

    res = y_pred[0] == "1"
    return res


def fitSVM():
    validData, invalidData = dataClean()
    wordData = cleanData()
    # 预处理
    X = wordData.drop('class', axis=1)
    y = wordData['class']

    # 划分训练与预测集合
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)

    # kSVM 核选择
    svclassifier = SVC(C=1, kernel='rbf', degree=6, class_weight=({'0': 0.2, '1': 2}))
    svclassifier.fit(X_train, y_train)

    joblib.dump(svclassifier, SVMModelName)


def dealWithStr(myStr):
    return False
    #return dealWithSVM(myStr)


if __name__ == "__main__":
    data = dealWithSVM("sadwajdnk")
    print(data)
