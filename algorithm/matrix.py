# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 00:52:53 2018

@author: litte
"""
import random
'''概率矩阵'''
def generationMatrix(imported):
    
    # 剔除充电桩
    for item in imported:
        for eachItem in item:
            if eachItem > 1000:
                item.remove(eachItem)
    #假定输入参数
#    imported =[
#        [0, 1,2,3,6,4, 0],
#        [0, 11,15,19,12, 0],
#        [0, 21,28,23, 0],
#        [0, 33, 0],
#        [0, 41,43,46, 0],
#        [0, 209, 822, 0]
#    ];
    #得到簇中点的集合
    visited = [];
    for i in imported:
        for j in i:
            if j != 0:
                visited.append(j);
    #初始化参数
    limit = 0.8;
    probability = len(visited)//5;
    route_mun = 50;
    #矩阵的维度
    n = len(visited); 
    #-----------------------------定义概率矩阵
    rect = {};
    for i in visited: 
       rect[i] = {};
       for j in visited:
            if j == i:
                rect[i][j] = 0.0;
            else:
                rect[i][j] = 1.0;
    #--------------------------------------------------开始计算
    for oneRoute in imported:
        #oneRoute:[0,5,784,...45,5,0]
        length = len(oneRoute) - 1
        for j in range(0,length):
            if oneRoute[j] == 0 or oneRoute[j+1] == 0:
                continue
            rect[oneRoute[j]][oneRoute[j+1]] +=  probability -  probability/(n-2)            
            for keys,values in rect[oneRoute[j]].items():
                rect[oneRoute[j]][keys] += probability/(n-2);
                if keys == oneRoute[j]:
                     rect[oneRoute[j]][keys] = 0
    #--------------------------------------------------归一化
    sum = 0
    for oneRoute in rect:
        for keys,values in rect[oneRoute].items():
            sum += values
        for k,v in rect[oneRoute].items():
            rect[oneRoute][k] *= 1/sum
    #--------------------------------------------------选择路径
    routes_gather = [];
    for i in range(0,route_mun):   
        #随机选取一条路线的第一个点,加入到一个List中
        one = visited[random.randint(0,n-1)]
        output = [];
        output.append(one); 
        #得到可以去的城市（未选择的城市）在visited列表中不再output列表中
        to_visit = [i for i in visited if i not in output]
        
        #当to_visit列表中还有值时，一直循环
        while len(to_visit) > 0:
    
            #得到选择的点所有相关的概率
            #p -->  {821:0, 262:1, 935:1 ....
            p = rect[output[len(output) - 1]];
            copy_p = {};
            for valuess in to_visit:
                copy_p[valuess] = p[valuess]
            random_digit = random.random();
            temp_p = 0;
            temp_k = 0;
            if random_digit<limit:
    
                for k,v in copy_p.items():
                    if v > temp_p:
                        temp_k = k            
            else:             
                #轮盘赌选择下一个城市
                #求总和
                #求累计和
                sumP = 0
                for key,value in copy_p.items():
                    sumP += value
                    copy_p[key] = sumP
    
                #按概率原则选取下一个城市             
                for kp,vp in copy_p.items():
                    copy_p[kp] = copy_p[kp] / sumP
    
                for kpe,vpe in copy_p.items():
                    if vpe >= random_digit:
                        temp_k = kpe;
                #选择的点是
            output.append(temp_k);
            to_visit = [i for i in visited if i not in output]
        routes_gather.append(output);
    return routes_gather