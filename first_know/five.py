# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 13:47:00 2018

@author: litte
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 18:52:19 2018

@author: litte
"""

import csv
import random
import copy
import operator

# 每一个聚类得出的种群规模
population_size = {}
# 聚类列表
cluster = ['cluster_0', 'cluster_1', 'cluster_2', 'cluster_3', 'cluster_4',
           'cluster_5', 'cluster_6', 'cluster_7', 'cluster_8', 'cluster_9']
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
# detail[0] = [0,0]
# 从总列表总获取每一点到没一点的距离和时间-------三阶列表
total_data = []
# 定义一个列表存放 不满足条件而提出已定义列表的 客户点
eliminate_point = []

# 剔除已生成路径中不满足条件的客户点
unsatisfied = []

filename = "k-means.csv"
"""
ID	type	lng	    lat 	
pack_total_weight	pack_total_volume	
first_receive_time	last_receive_time	deadline
first_receive_tm	last_receive_tm	
cluster
"""


def getBaseData(filename):
    f = open(filename)
    reader = csv.reader(f)
    header_row = next(reader)
    for row in reader:
        #    print (row)
        try:
            # pack_total_weight
            detail[int(row[0])].append(float(row[4]))
            # pack_total_volume
            detail[int(row[0])].append(float(row[5]))
            # first_receive_time
            detail[int(row[0])].append(int(row[6]))
            # deadline
            detail[int(row[0])].append(int(row[8]))
        except KeyError as e:
            detail[int(row[0])] = []
            detail[int(row[0])].append(float(row[4]))
            detail[int(row[0])].append(float(row[5]))
            detail[int(row[0])].append(int(row[6]))
            detail[int(row[0])].append(int(row[8]))
        try:
            # cluster
            result[row[11]].append(int(row[0]))
        except KeyError as e:
            result[row[11]] = []
            result[row[11]].append(int(row[0]))


getBaseData(filename)


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


# 查找最近的充电桩
# 剔除已生成路径中不满足条件的客户点
# unsatisfied_point = []
def gengeration_population(cluster_item):
    # 获取到每一簇的ID集合
    cluster_ids = result[cluster_item]
    i = 1
    while i <= 50:
        #        为每一簇随机生成50个种群，并将其放入population_size字典中
        random.shuffle(cluster_ids)
        try:
            population_size[cluster_item].append(copy.deepcopy(cluster_ids))
        except:
            population_size[cluster_item] = []
            population_size[cluster_item].append(copy.deepcopy(cluster_ids))
        i += 1


# def initialPath(population_item):

for cluster_item in cluster:
    # 对每一簇进行解码验证初始解----------

    if cluster_item == 'cluster_0':
        gengeration_population(cluster_item)
        # 循环处理每一簇中的50中情况 产生初始路径
        m = 0
        while m < 50:
            unsatisfied_point = []
            population_item = population_size[cluster_item][m]
            route = []
            routes = []
            for mIdIndex in range(len(population_item)):
                weight -= detail[population_item[mIdIndex]][0]
                volume -= detail[population_item[mIdIndex]][1]
                # # 3.（一）根据装载约束（体积和重量限制）将每个路径上的客户点划分给第二种车型【2.5t,16m^3】
                if weight > 0 and volume > 0:
                    route.append(population_item[mIdIndex])
                else:
                    routes.append(route)
                    route = []
                    weight = 2.5 - detail[population_item[mIdIndex]][0]
                    volume = 16 - detail[population_item[mIdIndex]][1]
                    route.append(population_item[mIdIndex])
            routes.append(route)  # 分配得到的路径集合

            for route_item in routes:
                each_route_weight = 0
                each_route_volume = 0
                # 创建用来存储(客户点：时间窗下限) 为排序做准备
                time_route = dict()
                # 等待成本
                waiting_cost = 0.0
                # 运输成本
                transportation_cost = 0
                # 路径中使用充电桩的集合
                used_charging_pile = []
                #               # 充电成本
                charging_cost = 0
                # 车辆使用成本
                """"""
                for item in route_item:
                    # 为输出时的计算填充结果
                    each_route_weight += detail[item][0]
                    each_route_volume += detail[item][1]
                    # 3.（二）根据客户的硬时间窗和车辆的电量限制，将划分给车辆的客户排序和删除
                    # 一先将数据一一对应存入字典中(客户点：时间窗下限)
                    time_route[item] = detail[item][3]
                    # 二根据客户时间窗下限从到大排序
                    sorted_item = dict(sorted(time_route.items(), key=operator.itemgetter(1)))
                    # 对排序后得到的结果，字典sorted_item,取出客户点 重新组成一个集合
                    # 由时间窗从大到小的排序来确定客户的排序
                    sorted_route = []  # 列表存放根据时间窗排序后得出的客户点顺序
                    for key in sorted_item.keys():
                        sorted_route.append(key)
                    # 在起始位置加入仓储中心
                    sorted_route.insert(0, 0)
                    sorted_route.append(0)
                    # 车辆出发时间 8：00 转化为0 进行累加
                    time_consuming = 0
                    # 定义路径距离 为充电桩行使功能
                    distance = 120000
                    cars = len(routes)
                    # 车辆使用成本
                    use_car_cost = cars * 300
                    # 总成本
                    total_cost = 0
                    # 每一簇中使用充电桩个数
                    use_charging_pile = []

                # 依次遍历分配给车辆排序后的所有点，考虑下一点是否可取
                #                for index in range(len(sorted_route)-1):
                start_index = 0  # 起点的索引
                target_index = 1  # 目标点的索引
                while 1:
                    if target_index >= len(sorted_route):
                        break
                    # 依次取出连续两点
                    #                        print(sorted_route[index],sorted_route[index+1])
                    # 预计到达的时间
                    except_time = time_consuming + total_data[sorted_route[start_index]][sorted_route[target_index]][1]
                    # 每一条路径的起始点都是仓储中心
                    if except_time > detail[sorted_route[target_index]][3]:
                        # 到达时间超过了客户最晚等待时间 ，则将此客户点剔除出队列
                        unsatisfied_point.append(sorted_route.pop(target_index))
                        #                            unsatisfied_point.append(sorted_route.pop(index+1))
                        #                            sorted_route[index+1] = 2000 # >>>>>>这样处理不行
                        if target_index >= len(sorted_route):
                            break
                        continue
                    else:
                        if except_time < detail[sorted_route[target_index]][2]:
                            # 早于客户点开始时间 则需等待 会产生等待成本----->等待成本24元/h
                            waiting_time = detail[sorted_route[target_index]][2] - except_time
                            # 等待成本
                            waiting_cost += waiting_time / 60 * 24
                            except_time = detail[sorted_route[target_index]][2]
                        # 1、先考虑从当前点出发去下一点是否在客户的时间窗下限之前到达，
                        time_consuming = except_time
                        # 更新时间 行驶花费的时间 + 到达后卸货时间0.5h
                        time_consuming += 30
                        # 说明满足下一个时间窗要求 时间窗上 下一个点可以去
                        # >>>>>接下来要考虑电量
                        # >>>计算路径的距离
                        route_distance = total_data[sorted_route[start_index]][sorted_route[target_index]][0]
                        # 运输成本-----14元/公里
                        transportation_cost += 14 * route_distance / 1000
                        # 2、若满足时间窗要求 则考虑车辆电量是否满足去下一点，不满足则考虑附近的充电桩
                        if distance - route_distance > 0:
                            # 说明下一个点在距离上可达
                            distance = distance - route_distance
                        else:
                            #                               # 距离上不满足则 不进行运算(距离不变) 寻找充电桩
                            # 搜索剩余电量能到的充电桩集合
                            charging_pile = []
                            for i in range(1001, 1101):  # 1001~1100充电桩的编号
                                if total_data[sorted_route[start_index]][i][0] < distance:
                                    charging_pile.append(i)  # 距离上可以达到的充电桩列表
                            if len(charging_pile) == 0:  # 说明未找到合适的充电桩 则将客户点剔除
                                # 如果无可以到达的充电桩，则将该点剔除 ------未避免IndexError 不能剔除，先将其另存一份
                                unsatisfied_point.append(sorted_route.pop(target_index))
                                #                                    sorted_route[target_index] = 2000
                                #                                    unsatisfied_point.append(sorted_route.pop(index))
                                if target_index >= len(sorted_route):
                                    break
                                continue

                            # 如果超出车辆能行驶的距离 寻找能到达的充电桩 并选择一个去下一个客户点最近的充电桩
                            min_distance = total_data[charging_pile[0]][sorted_route[target_index]][0]
                            min_index = charging_pile[0]

                            for charging_pile_item in charging_pile:
                                if total_data[sorted_route[start_index]][charging_pile_item][0] < min_distance:
                                    min_distance = total_data[sorted_route[target_index]][charging_pile_item][0]
                                    min_index = charging_pile_item
                                    use_charging_pile.append(min_index)
                            transportation_cost += 14 * (
                                        min_distance + total_data[min_index][sorted_route[target_index]][0]) / 1000
                            # 求出了 去哪个充电桩充电并将其加到已知路径中
                            sorted_route.insert(target_index, min_index)
                            time_consuming += 30
                            distance = 120000

                        start_index = target_index
                        target_index = target_index + 1

                #                print(min_inde1x,sorted_route)
                #                unsatisfied.append(unsatisfied_point)
                #                    print(unsatisfied)
                #                print(sorted_route)
                #                print("总路径：",len(routes),"已分配一条路径,长度为",len(route_item),"包含客户点：",route_item,
                #                      "weight总量：",each_route_weight,"volume总量：",each_route_volume)
                #                    index += 1
                #                    for pop_point in sorted_route:
                #                        if pop_point == 2000:
                #                            sorted_route.remove(pop_point)
                #                        elif pop_point>1000:
                #                            used_charging_pile.append(pop_point)
                # 加入充电等待成本 和 充电成本
                charging_cost = 100 * len(used_charging_pile)
                with open("route1.txt", "a") as f:
                    f.write(str(m) + "/50。" + "共需要车辆数：" + str(len(routes)) +
                            "已分配一条路径,长度为:" + str(len(route_item)) +
                            "包含客户点：" + str(sorted_route) +
                            "weight总量：" + str(each_route_weight) +
                            "volume总量：" + str(each_route_volume) + "\n")
            # 总成本
            total_cost += transportation_cost + waiting_cost + charging_cost + use_car_cost
            print("迭代次数：---------------------", m, "总成本：", total_cost)
            break
            #            print("提出不满足条件的点:"+str(unsatisfied))
            m += 1
