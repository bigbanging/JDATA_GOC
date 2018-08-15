# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 15:06:01 2018
寻找到 里每一个点最近的充电桩信息
@author: litte
"""

import csv

filename = "neighbor.csv"
f = open(filename)
reader = csv.reader(f)
# print(reader)
header_row = next(reader)

index_spend = dict()
index = 1
spends = []
#data2 = []
for row in reader:
    if int(row[1]) == index:
        spends.append(int(row[3]))
    else:
        index_spend[index] = spends.index(min(spends))
        index = index + 1
        spends = [int(row[3])]
    index_spend[index] = spends.index(min(spends))

filename = "neighbor.csv"
f = open(filename)
reader = csv.reader(f)
header_row = next(reader)
data2 = []

for row in reader:
    data = []
    data.append(row[0])
    data.append(row[1])
    data.append(row[2])
    data.append(row[3])
    data.append(row[4])
    # 所有数据的集合 一行数据有为一个集合
    data2.append(data)

result = []
for k, v in index_spend.items():
    result.append(data2[(k - 1) * 100 + v])

file = open("result.txt", "a")
for row in result:
    for i in row:
        file.write(str(i) + "\t")
    file.write("\n")
file.close()
