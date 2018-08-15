# -*- coding:utf-8 -*-
"""
@version :??
@Time     :2018/7/11 10:03
@Author   :'litte'
@File     :third.py
@Site     :
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:41:04 2018
@author: litte
 -*- coding:utf-8 -*-
 Time     :2018/7/7 13:41
 Author   :gwl
 File     :first.py
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
# 体积 立方米
volume = 16
# 重量 吨
weight = 2.5
# 需要用车
cars = 0
# 聚类字典
result = dict()
# ID为索引 后面为值的 字典
detail = dict()
detail[0] = [0, 0]
# 从总列表总获取每一点到没一点的距离和时间-------三阶列表
total_data = []


# 运输工具
class Car(object):
    def __init__(self):
        # 属性
        self.weight = 2.5  # 吨
        self.volume = 16  # 立方米
        self.power = 0  # 电量


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


def getDistanceAndTime():
    total_filename = "input_distance-time.txt"
    for i in range(0, 1101):
        total_data.append([])
        for j in range(0, 1101):
            total_data[i].append([])
    with open(total_filename, 'r') as f:
        for k in f:
            [mId, from_node, to_node, distance, spend_tm] = k.strip("\n").split(",")
            total_data[int(from_node)][int(to_node)].append(int(distance))
            total_data[int(from_node)][int(to_node)].append(int(spend_tm))


# 调用一下函数 把函数要完成的任务做了 填充total_data 这个三阶矩阵
getDistanceAndTime()

for cluster_item in cluster:
    #    print(cluster_item)
    # 获取到每一簇的ID集合
    cluster_ids = result[cluster_item]
    i = 1
    while i <= 50:
        #        为每一簇随机生成50个种群，并将其放入population_size字典中
        random.shuffle(cluster_ids)
        try:
            population_size[cluster_item].append(copy.deepcopy(cluster_ids))
        except KeyError as e:
            population_size[cluster_item] = []
            population_size[cluster_item].append(copy.deepcopy(cluster_ids))
        i += 1
    # 对每一簇进行解码验证----------先期实验
    if cluster_item == 'cluster_0':
        m = 0
        while m < 50:
            population_item = population_size[cluster_item][m]
            route = []
            routes = []
            for mIdIndex in range(len(population_item)):
                weight -= detail[population_item[mIdIndex]][0]
                volume -= detail[population_item[mIdIndex]][1]
                if weight > 0 and volume > 0:
                    route.append(population_item[mIdIndex])
                else:
                    routes.append(route)
                    route = []
                    weight = 2.5 - detail[population_item[mIdIndex]][0]
                    volume = 16 - detail[population_item[mIdIndex]][1]
                    route.append(population_item[mIdIndex])
            routes.append(route)
            for route_item in routes:
                route_item.insert(0, 0)
                #            print(route_item)
                each_route_weight = 0
                each_route_volume = 0
                for item in route_item:
                    each_route_weight += detail[item][0]
                    each_route_volume += detail[item][1]
                #                print("总路径：",len(routes),"已分配一条路径,长度为",len(route_item),"包含客户点：",route_item,
                #                      "weight总量：",each_route_weight,"volume总量：",each_route_volume)
                cars = len(routes)
                #                print("共需要车辆数：",cars)
                with open("route.txt", "a") as f:
                    f.write(str(m) + "/50。" + "共需要车辆数：" + str(cars) +
                            "已分配一条路径,长度为:" + str(len(route_item)) +
                            "包含客户点：" + str(route_item) +
                            "weight总量：" + str(each_route_weight) +
                            "volume总量：" + str(each_route_volume) + "\n")
            print("---------------------", m)
            m += 1
#        for n in route:
#            if n in population_item:
#                population_item.remove(n)
#        route.clear()
#        print("未分配",population_item)
#        print(weight)
#        print(Car().weight)
#        print(Car().volume)
#        print(sum(weight))
#        with open("cluster_o.txt","w") as f:
#            f.write(str(weight))
#                for mIndex in range(len(population_item)):
#                    print(population_item[mIndex][mIndex-2+1][0])
#                print(total_data)
#    print(cluster_ids)
# 遍历得出每一个ID所对应的重量以及体积
#    for cluster_id in cluster_ids:
#        weight.append(detail[cluster_id][0])
##        print(weight)
#        volume.append(detail[cluster_id][1])
#    print('总重量：',sum(weight))
#    print('总体积：',sum(volume))
# 遍历population_size种群 进行解码---------------测试用的
# for key in population_size.keys():
#    print(key+":",population_size[key])
# 输出了种群规模 暂订为 50
# f = open("population.json",'w')
# f.write(str(population_size)+"\n")
# f.close
