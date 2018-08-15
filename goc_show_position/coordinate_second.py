# -*-coding:utf-8-*-
#绘制坐标点
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter  
import csv
import time

t1 = time.time()
filename = 'date_point.csv'
f = open(filename)
reader = csv.reader(f)
header_row = next(reader)
print(header_row)
for index,colum_header in enumerate(header_row):
	print(index,colum_header)


types = []
lngs = []
lats = []

for row in reader:
	types.append(int(row[0]))
	lngs.append(float(row[1]))
	lats.append(float(row[2]))
print(lngs)
print(lats)
print(types)
for charge_point in types:
	"""
	if charge_point == 1:
		plt.scatter(lngs,lats,c='red', s=15)
		plt.show()
	elif charge_point == 2:
		plt.scatter(lngs,lats,c='blue',s=10)
		plt.show()
	else:
		plt.scatter(lngs,lats,c='yellow',s=5)
		plt.show()
	"""
# 绘制坐标点
#plt.scatter(lngs, lats, s=15)
# 测试：尝试三种颜色的显示
plt.scatter(lngs[0], lats[0], c='red', s=8)
plt.scatter(lngs[1:1001], lats[1:1001], c='blue', s=4)
plt.scatter(lngs[1002:], lats[1002:], c='black', s=4)
#绘制图表标题并给坐标轴加上标签
plt.title("Data Coordinate", fontsize=24)
plt.xlabel('longitude', fontsize=14)
plt.ylabel('latitude', fontsize=14)
# 设置标记刻度
plt.tick_params(axis='both', which='major', labelsize=14)
t2 = time.time()
print("time use",(t2-t1))
plt.show()

