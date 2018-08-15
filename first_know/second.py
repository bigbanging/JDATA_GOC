# -*- coding:utf-8 -*-
"""
@version :??
@Time     :2018/7/9 14:23
@Author   :'litte'
@File     :second.py
@Site     :
"""
import csv
import random
import copy

filename = "k-means.csv"
f = open(filename)
reader = csv.reader(f)
header_row = next(reader)
# 聚类列表
cluster = ['cluster_0', 'cluster_1', 'cluster_2', 'cluster_3', 'cluster_4',
           'cluster_5', 'cluster_6', 'cluster_7', 'cluster_8', 'cluster_9']
# 每一个聚类得出的种群规模
population_size = {}
# 体积
volume = []
# 重量
weight = []
# 需要用车
cars = 0
# 聚类字典
result = dict()
# ID为索引 后面为值的 字典
detail = dict()
for row in reader:
    #    print (row)
    try:
        detail[int(row[0])].append(float(row[4]))
        detail[int(row[0])].append(float(row[5]))
    except KeyError as e:
        detail[int(row[0])] = []
        detail[int(row[0])].append(float(row[4]))
        detail[int(row[0])].append(float(row[5]))

    try:
        result[row[8]].append(int(row[0]))

    except KeyError as e:
        result[row[8]] = []
        result[row[8]].append(int(row[0]))

for cluster_item in cluster:
    #    print(cluster_item)
    # 获取到每一簇的ID集合
    cluster_ids = result[cluster_item]
    i = 1
    while i <= 50:
        random.shuffle(cluster_ids)
        try:
            population_size[cluster_item].append(copy.deepcopy(cluster_ids))
        except KeyError as e:
            population_size[cluster_item] = []
            population_size[cluster_item].append(copy.deepcopy(cluster_ids))
        i += 1
    #    print(cluster_ids)
    for cluster_id in cluster_ids:
        weight.append(detail[cluster_id][0])
        #        print(weight)
        volume.append(detail[cluster_id][1])
    print('总重量：', sum(weight))
    print('总体积：', sum(volume))
# 输出了种群规模 暂订为 50
f = open("population.json", 'w')
f.write(str(population_size) + "\n")
f.close()

