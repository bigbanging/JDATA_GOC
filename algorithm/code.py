# -*- coding:utf-8 -*-
"""
@version :??
@Time     :2018/8/15 9:26
@Author   :'litte'
@File     :code.py
@Site     :
"""

import csv
import random
import copy
import operator
import time
import matrix

startTime = time.time()  # 开始时间戳
population_size = {}  # 每一个聚类得出的种群规模
# 聚类列表
cluster = ['cluster_0', 'cluster_1', 'cluster_2', 'cluster_3', 'cluster_4',
           'cluster_5', 'cluster_6', 'cluster_7', 'cluster_8', 'cluster_9']
volume = 16  # 体积 立方米
weight = 2.5  # 重量 吨
cars = 0  # 需要用车
result = dict()  # 聚类字典
detail = dict()  # ID为索引 后面为值的 字典
total_data = []  # 从总列表总获取每一点到没一点的距离和时间-------三阶列表
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
            detail[int(row[0])].append(int(row[7]))
        except KeyError as e:
            detail[int(row[0])] = []
            detail[int(row[0])].append(float(row[4]))
            detail[int(row[0])].append(float(row[5]))
            detail[int(row[0])].append(int(row[6]))
            detail[int(row[0])].append(int(row[7]))
        try:
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


def gengeration_population(cluster_item):
    # 获取到每一簇的ID集合
    cluster_ids = result[cluster_item]
    i = 1
    while i <= 100:
        #        为每一簇随机生成50个种群，并将其放入population_size字典中
        random.shuffle(cluster_ids)
        try:
            population_size[cluster_item].append(copy.deepcopy(cluster_ids))
        except:
            population_size[cluster_item] = []
            population_size[cluster_item].append(copy.deepcopy(cluster_ids))
        i += 1


'''
    GetNearestChargingPile(startNode,endNode,MapMsg,distance):
        获取startNode可达的，距离endNode最近的充电桩的编号
    startNode:当前客户点
    endNode：下一个客户点
    MapMsg：the message of Map, save the distance of two customer point
    distance:当前车辆从当前客户点出发可以行驶的距离
'''


def GetNearestChargingPile(startNode, endNode, MapMsg, distance):
    charging_pile = []  # 充电桩编号
    for i in range(1001, 1101):  # 1001~1100充电桩的编号
        if MapMsg[startNode][i][0] < distance:
            charging_pile.append(i)  # 距离上可以达到的充电桩列表
    if len(charging_pile) == 0:
        return -1  # 没有找到，返回-1
    else:
        min_distance = MapMsg[charging_pile[0]][endNode][0]
        min_index = charging_pile[0]
        for charging_pile_item in charging_pile:
            if MapMsg[charging_pile_item][endNode][0] < min_distance:
                min_distance = MapMsg[charging_pile_item][endNode][0]
                min_index = charging_pile_item
        return min_index


'''由customList客户点的编号 根据体重和体积约束 分配初始路径'''


def initialPath(customList):
    route = []
    routes = []
    global weight, volume
    for mIdIndex in range(len(customList)):
        weight -= detail[customList[mIdIndex]][0]
        volume -= detail[customList[mIdIndex]][1]
        # # 3.（一）根据装载约束（体积和重量限制）将每个路径上的客户点划分给第二种车型【2.5t,16m^3】
        if weight > 0 and volume > 0:
            route.append(customList[mIdIndex])
        else:
            routes.append(route)
            route = []
            weight = 2.5 - detail[customList[mIdIndex]][0]
            volume = 16 - detail[customList[mIdIndex]][1]
            route.append(customList[mIdIndex])
    routes.append(route)  # 分配得到的路径集合
    return routes


'''按客户点时间窗由小到大的排序 而得出的排序后的路径'''


def sortedRoutes(detail, time_route, singleRoute):
    sortedRoutesByTimeWindow = []  # 列表存放根据时间窗排序后得出的客户点顺序
    #    print('singleRoute++++++++++++-----------',singleRoute)
    for item in singleRoute:
        # 3.（二）根据客户的硬时间窗和车辆的电量限制，将划分给车辆的客户排序和删除
        # 一先将数据一一对应存入字典中(客户点：时间窗下限)
        time_route[item] = detail[item][3]
        # 二根据客户时间窗下限从到大排序
        sorted_item = dict(sorted(time_route.items(), key=operator.itemgetter(1)))
        # 对排序后得到的结果，字典sorted_item,取出客户点 重新组成一个集合
    # 由时间窗从大到小的排序来确定客户的排序
    for key in sorted_item.keys():
        sortedRoutesByTimeWindow.append(key)
    # 在起始位置加入仓储中心
    sortedRoutesByTimeWindow.append(0)
    sortedRoutesByTimeWindow.insert(0, 0)
    #    print(sorted_routes_by_time_window)
    return sortedRoutesByTimeWindow


'''对按时间窗排序后的路径进行解码'''


def decoding(time_consuming, waiting_cost, transportation_cost, sorted_route, distance, detail):
    unsatisfied_point = []
    start_index = 0  # 起点的索引
    target_index = 1  # 目标点的索引
    while 1:
        if target_index >= len(sorted_route):
            break
        except_time = time_consuming + total_data[sorted_route[start_index]][sorted_route[target_index]][1]
        # 每一条路径的起始点都是仓储中心
        if except_time > detail[sorted_route[target_index]][3]:
            # 到达时间超过了客户最晚等待时间 ，则将此客户点剔除出队列
            unsatisfied_point.append(sorted_route.pop(target_index))
            #            print(unsatisfied_point)
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
            # >>>>>接下来要考虑电量 >>>计算路径的距离
            route_distance = total_data[sorted_route[start_index]][sorted_route[target_index]][0]
            # 同时考虑电量是否足够从下一点去往最近的充电桩
            #            nearChargeToTarget = []
            toChargeDistance = 120000
            for chargeItem in range(1001, 1101):
                if total_data[sorted_route[target_index]][chargeItem][0] < toChargeDistance:
                    toChargeDistance = total_data[sorted_route[target_index]][chargeItem][0]
            # 2、若满足时间窗要求 则考虑车辆电量是否满足去下一点，不满足则考虑附近的充电桩
            if distance - route_distance > 0 and distance - route_distance - toChargeDistance > 0:
                # 说明下一个点在距离上可达
                distance = distance - route_distance
            else:
                # 距离上不满足则 不进行运算(距离不变) 寻找充电桩
                # 搜索剩余电量能到的充电桩集合
                min_index = GetNearestChargingPile(sorted_route[start_index], sorted_route[target_index], total_data,
                                                   distance)
                CurrentCustomer2MinIndexDistance = 0
                if min_index == -1:  # 说明未找到合适的充电桩 则将客户点剔除
                    unsatisfied_point.append(sorted_route.pop(target_index))
                    if target_index >= len(sorted_route):
                        unsatisfied_point.pop()
                        #                        print(unsatisfied_point)
                        '''到达最后一个点，把最后一个点踢掉了的情况
                        最后一个点肯定是 配送中心0点
                        判断当前情况下，倒数第一个点能否回到配送中心
                        如果可以，则将最后一个客户点踢掉，然后把0点加回来
                        如果不行，继续往前走'''
                        while 1:
                            #                            print("if---------------",start_index)
                            distance = distance + total_data[sorted_route[start_index - 1]][sorted_route[start_index]][
                                0]

                            if distance > total_data[sorted_route[start_index - 1]][0][0]:
                                unsatisfied_point.append(sorted_route.pop(start_index))
                                sorted_route.append(0)
                                break
                            else:
                                # 找充电桩
                                charging_id = GetNearestChargingPile(sorted_route[start_index - 1], 0, total_data,
                                                                     distance)
                                if charging_id == -1:
                                    start_index = start_index - 1
                                else:
                                    sorted_route.append(charging_id)
                                    sorted_route.append(0)
                                    break
                        break
                    continue
                else:
                    CurrentCustomer2MinIndexDistance = total_data[sorted_route[start_index]][min_index][0]
                # 如果超出车辆能行驶的距离 寻找能到达的充电桩 并选择一个去下一个客户点最近的充电桩
                transportation_cost += 14 * (
                        CurrentCustomer2MinIndexDistance + total_data[min_index][sorted_route[target_index]][
                    0]) / 1000
                # 求出了 去哪个充电桩充电并将其加到已知路径中
                sorted_route.insert(target_index, min_index)
                # 时间更新 去附近的充电桩的耗时 + 0.5号充电时间 + 从充电桩到下一个客户点的用时
                #                for sortItems in sorted_route:
                #                    if sortItems >1000:
                #                        time_consuming+=total_data[sorted_route[start_index]][sorted_route[target_index]][1] + 30 +total_data[sorted_route[target_index]][sorted_route[target_index+1]][1]
                distance = 120000
            #                print(sorted_route)
            start_index = target_index
            target_index = target_index + 1

    #    return unsatisfied_point,time_consuming,waiting_cost
    return unsatisfied_point, waiting_cost


# generationMatrix(imported) # 测试函数

def matrixRoutes(generateRoutesByMatrix, cluster_item):
    m = 0
    allDatas = []
    while m < 50:
        # 剔除已生成路径中不满足条件的客户点
        unsatisfied_points = []
        population_item = generateRoutesByMatrix[cluster_item][m]
        i = 0
        eachRouteData = []
        eachTotalCost = 0
        minTotalCost = 0
        while 1:
            if len(population_item) == 0:
                break
            routes = initialPath(population_item)
            # 存放这一簇中的所有 结果的集合的集合 ，为比较最小的结果 准备数据集
            for route_item in routes:
                #                print('wtf---------------1-----------',route_item)
                if len(route_item) == 0:
                    continue
                time_route = dict()  # 创建用来存储(客户点：时间窗下限) 为排序做准备
                '''计算等待时间 而后计算等待成本'''
                distance = 120000  # 定义路径距离 为充电桩行使功能
                sorted_route = sortedRoutes(detail, time_route, route_item)
                #                print('sorted_route:=================',sorted_route)
                unsatisfied_point, waiting_cost = decoding(
                    0, 0, 0, sorted_route, distance, detail)
                #                print('unsatisfied_point-----------',unsatisfied_point)
                unsatisfied_points.extend(unsatisfied_point)
                #                unsatisfied_point,time_consuming = decoding(0,0,0,sorted_route,distance,detail)
                '''计算"每一条"路径的成本流程'''
                '''每一条路径的距离'''
                each_execute_path_distance = 0
                '''每一条路径的载重量'''
                each_execute_path_weight = 0.0
                '''每一条路径的装载体积'''
                each_execute_path_volume = 0.0
                '''充电桩计数'''
                each_execute_path_charge = []
                smallCar = 0  # 小车
                bigCar = 0  # 大车
                transCost = 0.0  # 运输成本
                chargeCost = 0  # 充电成本
                carUsedCost = 300  # 车辆使用成本
                eachCost = 0  # 每条路径的总成本
                # 时间
                expectTime = 0
                waitingTime = 0
                waitCost = 0
                timeConsume = 0
                ''' 判断 行驶路径所使用的距离 来选择车辆类型 
                    到达第一个充电桩时 的路径长度 >10万 使用大车； <= 10万 使用小车'''
                carTypeDistance = 0
                for each_execute_path_index in range(len(sorted_route) - 1):
                    expectTime = timeConsume + total_data[sorted_route[each_execute_path_index]][
                        sorted_route[each_execute_path_index + 1]][1]
                    if expectTime < detail[sorted_route[each_execute_path_index + 1]][2]:
                        # 早于客户点开始时间 则需等待 会产生等待成本----->等待成本24元/h
                        waitingTime = detail[sorted_route[each_execute_path_index + 1]][2] - expectTime
                        waitCost += waitingTime / 60 * 24
                        expectTime = detail[sorted_route[each_execute_path_index + 1]][2]
                    # 1、先考虑从当前点出发去下一点是否在客户的时间窗下限之前到达，
                    timeConsume = expectTime
                    # 更新时间 行驶花费的时间 + 到达后卸货时间0.5h
                    timeConsume += 30
                    # 每一条路径的总里程
                    each_execute_path_distance += \
                        total_data[sorted_route[each_execute_path_index]][sorted_route[each_execute_path_index + 1]][0]
                    if sorted_route[each_execute_path_index] > 1000:
                        # 路径中充电桩计数
                        each_execute_path_charge.append(sorted_route[each_execute_path_index])
                        chargeCost = len(each_execute_path_charge) * 100 * 0.5
                    #                        waiting_time += len(each_execute_path_charge)*30 # 充电的半个小时不算作等待时间
                    # 判断使用车辆类型
                    each_execute_path_weight += detail[sorted_route[each_execute_path_index]][0]
                    each_execute_path_volume += detail[sorted_route[each_execute_path_index]][1]  # 错误出处

                    if len(each_execute_path_charge) == 0:  # 没有使用充电桩
                        # 查看全路径长度 和 10万比较
                        carTypeDistance = each_execute_path_distance
                    else:  # 使用了两个甚至以上个充电桩
                        # 比较出现多充电桩时的每段路径 取出最大值 来判断车型选择
                        carTypeDistanceList = []
                        for chargeIndex in range(len(sorted_route) - 1):
                            carTypeDistance += total_data[sorted_route[chargeIndex]][sorted_route[chargeIndex + 1]][0]
                            if sorted_route[chargeIndex] > 1000:
                                carTypeDistanceList.append(carTypeDistance)
                                carTypeDistance = 0
                        carTypeDistance = max(carTypeDistanceList)
                    if each_execute_path_weight <= 2 and each_execute_path_volume <= 12 and carTypeDistance <= 100000:
                        smallCar += 1
                        vehicle_type = 1
                        transCost = 12 * each_execute_path_distance / 1000
                        carUsedCost = 200
                    else:
                        bigCar += 1
                        vehicle_type = 2
                        transCost = 14 * each_execute_path_distance / 1000
                        carUsedCost = 300
                #                eachCost = transCost+chargeCost+carUsedCost+waiting_cost
                eachCost = transCost + chargeCost + carUsedCost + waitCost
                strResult = ''
                for routeIndex in range(len(sorted_route)):
                    if routeIndex == len(sorted_route) - 1:
                        strResult += str(sorted_route[routeIndex])
                    else:
                        strResult += str(sorted_route[routeIndex]) + ';'
                # 时间的处理
                hour = (timeConsume - 30) // 60 + 8
                minute = (timeConsume - 30) % 60
                if minute < 10:
                    minute = '0' + str(minute)
                time_arr = str(hour) + ':' + str(minute)
                # 用来存放每一簇路径所需的结果的集合
                datas = ['DP000' + str(i + 1), vehicle_type, strResult, str('8:00'), time_arr,
                         each_execute_path_distance, round(transCost, 2), chargeCost, round(waitCost, 2),
                         carUsedCost, round(eachCost, 2), len(each_execute_path_charge)]
                eachRouteData.append(datas)
                i = i + 1
            #            print('unsatisfied_points============================',unsatisfied_points)
            population_item = unsatisfied_points
            unsatisfied_points = []
        #        print(sorted_route)
        allDatas.append(eachRouteData)
        #        print("迭代次数：---------------------",m )
        #        break
        m += 1
    minTotalCost = 10000000
    for datasItem in allDatas[0]:
        minTotalCost += datasItem[10]
    minDatasCostItem = allDatas[0]
    for allDatasItem in allDatas:
        eachTotalCost = 0
        for datasItem in allDatasItem:
            eachTotalCost += datasItem[10]
        if eachTotalCost < minTotalCost:
            minTotalCost = eachTotalCost
            minDatasCostItem = allDatasItem
    return minTotalCost, minDatasCostItem


def getResult(cluster_item):
    gengeration_population(cluster_item)
    # 循环处理每一簇中的50中情况 产生初始路径
    minTotalCost, minDatasCostItem = matrixRoutes(population_size, cluster_item)
    #    for minresult in minDatasCostItem:
    #        with open('result13.csv','a',newline='') as csvFile:
    #            writer = csv.writer(csvFile)
    #            writer.writerow(minresult)
    return minTotalCost, minDatasCostItem


# [cost,costItem] = getResult('cluster_9')

allcost = 0
allItem = []
customerpos = []
for cluster_item in cluster:
    [cost, costItem] = getResult(cluster_item)
    allcost += cost
    allItem.append(costItem)
mincost = allcost
minItems = allItem
print('未加概率矩阵的成本：', mincost)

m = 0
while 1:
    allcost = 0
    allItem = []
    population_size = dict()
    for cluster_item in cluster:
        # 对每一簇进行解码验证初始解----------
        [cost, costItem] = getResult(cluster_item)
        #        [cost,costItem] = getResult('cluster_0')
        allcost += cost
        allItem.append(costItem)
    if allcost < mincost:
        mincost = allcost
        minItems = allItem
    print(mincost)
    m += 1
    if m > 10:
        forMartix = dict()
        resultByMartix = dict()
        iCluster = 0
        for eachCluster in minItems:
            finallRoute = []
            for itemList in eachCluster:
                newEachRoute = []
                for i in itemList[2].split(';'):
                    newEachRoute.append(int(i))
                finallRoute.append(newEachRoute)
            forMartix[cluster[iCluster]] = finallRoute
            iCluster += 1
        martixCosts = 0
        martixItems = []
        martixCustomerpos = []
        for clusterItem in cluster:
            eachClusterExecute = forMartix[clusterItem]
            # 通过概率矩阵生成50条 重新排序的路径列表
            generationRoutesByMartix = matrix.generationMatrix(eachClusterExecute)
            resultByMartix[clusterItem] = generationRoutesByMartix
            [martixCost, martixItem] = matrixRoutes(resultByMartix, clusterItem)
            martixCosts += martixCost
            martixItems.append(martixItem)
        minMartixCost = martixCosts
        minMartixItem = martixItems
        n = 0
        while 1:
            martixCosts = 0
            martixItems = []
            resultByMartix = dict()
            for clusterItem in cluster:
                eachClusterExecute = forMartix[clusterItem]
                # 通过概率矩阵生成50条 重新排序的路径列表
                generationRoutesByMartix = matrix.generationMatrix(eachClusterExecute)
                resultByMartix[clusterItem] = generationRoutesByMartix
                [martixCost, martixItem] = matrixRoutes(resultByMartix, clusterItem)
                martixCosts += martixCost
                martixItems.append(martixItem)
            if martixCosts < minMartixCost:
                minMartixCost = martixCosts
                minMartixItem = martixItems
            print('添加概率矩阵的成本：', minMartixCost)
            n += 1
            if n > 20:
                #        for clusterItem in cluster:
                #            eachClusterExecute = forMartix[clusterItem]
                #            # 通过概率矩阵生成50条 重新排序的路径列表
                #            generationRoutesByMartix = matrix.generationMatrix(eachClusterExecute)
                #            resultByMartix[clusterItem] = generationRoutesByMartix
                #
                #            minTotalCost,minDatasCostItem = matrixRoutes(resultByMartix,clusterItem)

                for minresult in minMartixItem:
                    for row in minresult:
                        with open('result41.csv', 'a', newline='') as csvFile:
                            writer = csv.writer(csvFile)
                            writer.writerow(row)
                    for cusitem in row[2].split(';'):
                        if int(cusitem) == 0 or int(cusitem) > 1000:
                            continue
                        customerpos.append(int(cusitem))
                break
        break
endTime = time.time()
timeUsed = endTime - startTime
print('程序运行耗时：', timeUsed)
