# -*- coding:utf-8 -*-
# Time     :2018/7/7 13:41
# Author   :gwl
# File     :first.py
import csv
import random

filename = "k-means.csv"
f = open(filename)
reader = csv.reader(f)
header_row = next(reader)
# 聚类列表
cluster = ['cluster_0', 'cluster_1', 'cluster_2', 'cluster_3', 'cluster_4', 'cluster_5', 'cluster_6', 'cluster_7',
           'cluster_8', 'cluster_9']
# 获取每一聚类的列表
# cluster_0, cluster_1, cluster_2, cluster_3, cluster_4, cluster_5, cluster_6, cluster_7, cluster_8, cluster_9 = []
# cluster_0 = []
# list_id = []
# 体积
volume = 0.00000
# 重量
weight = 0.00000
# 需要用车
cars = 0

result = dict()
for row in reader:
    try:
        result[row[8]].append(int(row[0]))
    except KeyError as e:
        result[row[8]] = []
        result[row[8]].append(int(row[0]))
# print(result)
for cluster_item in cluster:
    print(cluster_item)
    # 获取到每一簇的ID集合
    cluster_ids = result[cluster_item]
    random.shuffle(cluster_ids)
    print(cluster_ids)
    # 随机产生 种群规模N 个全排列
    # 解决方法一随机产生50中随机排序情况
    # i = 0
    # while i <= 50:
    #     cluster_0.append(random.shuffle(cluster_ids))
    # print(cluster_0)
