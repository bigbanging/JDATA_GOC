# -*- coding: utf-8 -*-
"""
Created on Sat May 13 15:38:15 2017

@author: Administrator
"""
import math
import numpy as np
import copy
import random

# 变量空间#
i = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
j = [0, 1, 2, 5, 7, 8, 10]
r = [1, 2]
K = [10, 10]

Small = [0, 2, 3, 5, 6, 0, 4, 3, 1, 6, 1]
Large = [0, 2, 1, 0, 0, 3, 0, 2, 1, 0, 3]
g = []
for ii in range(11):
    g.append(Small[ii] * 40 + Large[ii] * 120)

Sat = np.array(Large) * 2
Sst = np.array(Large) * 0.5
# Wi=np.array(Large)*120+np.array(Small)*40

del ii, Small, Large

x = np.array([0, 10, 30, 50, 50, 30, -10, -30, -40, -40, -30])
y = np.array([0, 40, 20, 10, -10, -30, -30, -50, -10, 20, 50])
d = [[], [], [], [], [], [], [], [], [], [], []]
for ii in range(11):
    for ij in range(11):
        d[ii].append(math.hypot(x[ii] - x[ij], y[ii] - y[ij]))  # hypot(x,y)  sqrt(x*x+y*y)
d = np.array(d)
del ii, ij, x, y

# ta=d/40
# ts=d/50

t = []
v = [50, 40]
for rr in r:
    R = []
    for ii in i:
        I = []
        for ij in i:
            I.append(d[ii][ij] / v[rr - 1])
        R.append(I)
    t.append(R)
del rr, ii, ij, I, R, v

w2 = []
T1 = []
T2 = []
for ii in i:
    w2.append(0)
    T1.append(0)
    T2.append(0)
del ii

Large = [0, 2, 1, 0, 0, 3, 0, 2, 1, 0, 3]
vt = [0.5, 2]
S = []
for rr in r:
    R = []
    for ii in i:
        R.append(vt[rr - 1] * Large[ii])
    S.append(R)
del vt, Large, rr, ii, R


##
def Target(X, d, K):
    global r
    global i
    MThou = K[0] * 200 + K[1] * 400
    sum1 = []
    for rr in r:
        sum_t = 0.0
        for kk in range(K[rr - 1]):
            for ii in i:
                for ij in i:
                    sum_t = sum_t + d[ii][ij] * X[rr - 1][kk][ii][ij]
        sum1.append(sum_t)
    return sum(sum1) + MThou


def Target2(X, d, K, w2):
    global r
    global i
    MThou = K[0] * 200 + K[1] * 400
    TimePunish = sum(np.array(w2) * 100)
    sum1 = []
    for rr in r:
        sum_t = 0.0
        for kk in range(K[rr - 1]):
            for ii in i:
                for ij in i:
                    sum_t = sum_t + d[ii][ij] * X[rr - 1][kk][ii][ij]
        sum1.append(sum_t)
    return sum(sum1) + MThou + TimePunish


# print Target(X,d,K)

def YueShu():
    flag = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    global g
    global Y
    global K
    #####s.t.1
    for kk in range(K[0]):
        Jg = sum(np.array(g) * np.array(Y[0][kk]))
        if Jg > 1200:
            flag[0] = 0

    #####s.t.2
    #    global K1
    sumY1 = 0.0
    for kk in range(K[0]):
        sumY1 = sumY1 + Y[0][kk][0]
    if K[0] != sumY1:
        flag[1] = 0

    #####s.t.3
    #    global K2
    sumY2 = 0.0
    for kk in range(K[1]):
        sumY2 = sumY2 + Y[1][kk][0]
    if K[1] != sumY2:
        flag[2] = 0

    #####s.t.4
    global X
    global r

    for rr in r:
        var_out = []
        var_in = []
        for kk in range(K[rr - 1]):
            var_out.append(sum(X[rr - 1][kk][0][:]))
            var_in_temp = 0
            for ii in i:
                var_in_temp = var_in_temp + X[rr - 1][kk][ii][0]
            var_in.append(var_in_temp)
        if var_out != var_in:
            flag[3] = 0

    #####s.t.5
    for ii in i[1:]:
        sumY = 0.0
        for kk in range(K[0]):
            sumY = sumY + Y[0][kk][ii]
        if sumY != 1:
            flag[4] = 0

    #####s.t.6
    for ii in j[1:]:
        sumY = 0.0
        for kk in range(K[1]):
            sumY = sumY + Y[1][kk][ii]
        if sumY != 1:
            flag[5] = 0

    #####s.t.7
    for rr in r:
        for kk in range(K[rr - 1]):
            for ii in i:
                sumX = 0
                for ij in i:
                    sumX = sumX + X[rr - 1][kk][ij][ii]
                if sum(X[rr - 1][kk][ii][:]) - sumX != 0:
                    flag[6] = 0

    #####s.t.8
    for rr in r:
        for kk in range(K[rr - 1]):
            for ij in i[1:]:
                sumX = 0
                for ii in i:
                    sumX = sumX + X[rr - 1][kk][ii][ij]
                if sumX != Y[rr - 1][kk][ij]:
                    flag[7] = 0

    #####s.t.9
    for rr in r:
        for kk in range(K[rr - 1]):
            for ii in i[1:]:
                if sum(X[rr - 1][kk][ii][:]) != Y[rr - 1][kk][ii]:
                    flag[8] = 0

    #####s.t.10
    global t
    global S
    for kk in range(K[0]):
        var_t = 0.0
        for ii in i:
            for ij in i:
                var_t = var_t + X[0][kk][ii][ij] * (t[0][ii][ij] + S[0][ii])
        if var_t > 10:
            flag[9] = 0

    #####s.t.11
    global w2
    for kk in range(K[1]):
        var_t = 0.0
        for ii in i:
            for ij in i:
                var_t = var_t + X[1][kk][ii][ij] * (t[1][ii][ij] + S[1][ii] + w2[ii])
        if var_t > 14:
            flag[10] = 0

    #####s.t.12
    global T1
    global T2
    for ij in i:
        T_temp = 0.0
        for ii in i:
            for kk in range(K[0]):
                T_temp = T_temp + X[0][kk][ii][ij] * (T1[ii] + t[0][ii][ij] + S[0][ij])
        T1[ij] = T_temp

    for ij in i:
        T_temp = 0.0
        for ii in i:
            for kk in range(K[1]):
                T_temp = T_temp + X[1][kk][ii][ij] * (T2[ii] + t[1][ii][ij] + S[1][ij] + w2[ij])
        T2[ij] = T_temp
    for ii in i:
        if T2[ij] < T1[ij]:
            flag[11] = 0
    #
    #    #####s.t.13
    #    for ii in i:
    #        Yfang=0
    #        for kk in range(K[0]):
    #            Yfang=Yfang+Y[0][kk][ii]
    #        if Yfang==0:
    #            flag[12]=0
    #
    #    #####s.t.14
    #    for ii in i:
    #        Yfang=0
    #        for kk in range(K[1]):
    #            Yfang=Yfang+Y[1][kk][ii]
    #        if Yfang==0:
    #            flag[13]=0

    #
    #    for flag_t in flag:
    #        if flag_t==0:
    #            return False
    #    return True
    #    print flag
    return flag.count(0)


# num=0
# OutputX=[]
# OutputY=[]
# OutputK1=[]
# OutputK2=[]
# changshi=0
def perm(Kehulist, k, m):
    global BeiXuan
    if k == m - 1:
        newK = []
        newK = copy.deepcopy(Kehulist)
        BeiXuan.append(newK)
    for ii in range(k, m):
        Kehulist[k], Kehulist[ii] = Kehulist[ii], Kehulist[k]
        perm(Kehulist, k + 1, m)
        Kehulist[k], Kehulist[ii] = Kehulist[ii], Kehulist[k]


BeiXuan = []
perm(i[1:], 0, 10)
BeiXuanS = copy.deepcopy(BeiXuan)
BeiXuan = []
perm(j[1:], 0, len(j) - 1)
BeiXuanA = copy.deepcopy(BeiXuan)

ZQGS = 50  # 种群数量
Output = [[], []]
for ii in range(ZQGS):
    jj = int(random.random() * len(BeiXuanS))
    Output[0].append(BeiXuanS[jj])
    ji = int(random.random() * len(BeiXuanA))
    Output[1].append(BeiXuanA[ji])


def CalculateT(t, MJ, S):
    T = t[0][MJ[0]]
    for i in range(len(MJ) - 1):
        T = T + t[MJ[i]][MJ[i + 1]] + S[MJ[i]]
    T = T + t[MJ[len(MJ) - 1]][0] + S[len(MJ) - 1]
    return T


def CalculateTA(t, MJ, S, T1):
    global w2
    T = t[0][MJ[0]]
    for i in range(len(MJ) - 1):
        T = T + t[MJ[i]][MJ[i + 1]] + S[MJ[i]] + w2[MJ[i]]
    if T < T1[MJ[len(MJ) - 1]]:
        w2[MJ[len(MJ) - 1]] = T1[MJ[len(MJ) - 1]] - T
        T = T1[MJ[len(MJ) - 1]]
        T = T + t[MJ[len(MJ) - 1]][0] + S[len(MJ) - 1]
    else:
        T = T + t[MJ[len(MJ) - 1]][0] + S[len(MJ) - 1]
    return T


def CalculateW(MJ, Wi):
    W = 0.0
    for i in MJ:
        W = W + Wi[i]
    return W


def ChangeLtoV(Output):
    global w2
    global T1
    Var_CSnum = []
    Var_CAnum = []
    for ilist in Output[0]:
        Var_CSnum_temp = []
        newL = []
        for item in ilist:
            newL.append(item)
            if CalculateT(t[0], newL, Sst) > 10 or CalculateW(newL, g) > 1200:
                newLL = copy.deepcopy(newL[:len(newL) - 1])
                Var_CSnum_temp.append(newLL)
                newL = []
                newL.append(item)
        Var_CSnum_temp.append(newL)
        Var_CSnum.append(Var_CSnum_temp)

    for ilist1 in Output[1]:
        w2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        T1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Var_CAnum_temp = []
        newL = []
        for ilist in Var_CSnum[Output[1].index(ilist1)]:
            for ii in range(len(ilist)):
                if ii == 0:
                    T1[ilist[ii]] = t[0][0][ilist[ii]] + S[0][ilist[ii]]
                else:
                    T1[ilist[ii]] = T1[ilist[ii - 1]] + t[0][ilist[ii - 1]][ilist[ii]]
        for item in ilist1:
            newL.append(item)
            if CalculateTA(t[1], newL, Sat, T1) > 14:
                newLL = copy.deepcopy(newL[:len(newL) - 1])
                Var_CAnum_temp.append(newLL)
                newL = []
                newL.append(item)
        Var_CAnum_temp.append(newL)
        Var_CAnum.append(Var_CAnum_temp)

    Var_num = []
    Var_num.append(Var_CSnum)
    Var_num.append(Var_CAnum)
    return Var_num


Var_num = ChangeLtoV(Output)

# print Target(X,d,K)
# YueShu()

End = 1000
Yichuandiedai = 0
while (1):
    TribeList = []
    Var_num = ChangeLtoV(Output)
    for im in range(len(Output[0])):
        K[0] = len(Var_num[0][im])
        K[1] = len(Var_num[1][im])
        X = []
        for rr in r:
            R = []
            for kk in range(K[rr - 1]):
                Kk = []
                for ii in i:
                    I = []
                    for ij in i:
                        I.append(0)
                    Kk.append(I)
                R.append(Kk)
            X.append(R)
        del rr, kk, ii, ij, R, Kk, I
        Y = []
        for rr in r:
            R = []
            for kk in range(K[rr - 1]):
                Kk = []
                for ii in i:
                    Kk.append(0)
                R.append(Kk)
            Y.append(R)
        del rr, kk, ii, R, Kk
        for rr in r:
            for kk in range(K[rr - 1]):
                X[rr - 1][kk][0][Var_num[rr - 1][im][kk][0]] = 1
                for ii in range(len(Var_num[rr - 1][im][kk]) - 1):
                    X[rr - 1][kk][Var_num[rr - 1][im][kk][ii]][Var_num[rr - 1][im][kk][ii + 1]] = 1
                    Y[rr - 1][kk][Var_num[rr - 1][im][kk][ii]] = 1
                X[rr - 1][kk][Var_num[rr - 1][im][kk][len(Var_num[rr - 1][im][kk]) - 1]][0] = 1
                Y[rr - 1][kk][Var_num[rr - 1][im][kk][len(Var_num[rr - 1][im][kk]) - 1]] = 1
                X[rr - 1][kk][0][0] = 1
                Y[rr - 1][kk][0] = 1
        newT = []
        newT.append(YueShu())
        newT.append(Target(X, d, K))
        newT.append(im)
        TribeList.append(newT)

    TribeList.sort()
    P = 0.8
    randomJorB = random.random()
    if randomJorB < P:
        sumT = 0.0
        for ilist in TribeList:
            sumT = sumT + 1 / ilist[1]
        Pc = []
        for ilist in TribeList:
            Pc.append((1 / ilist[1]) / sumT)
        Qc = []
        for pi in Pc:
            Qc.append(sum(Pc[:Pc.index(pi) + 1]))
        chose = []

        while (1):
            randomR = random.random()
            for ii in range(30):
                if len(chose) == 2:
                    break
                if ii == 0:
                    if randomR < Qc[ii]:
                        if chose.count(TribeList[ii]) != 0:
                            continue
                        chose.append(TribeList[ii])
                else:
                    if randomR < Qc[ii] and randomR > Qc[ii - 1]:
                        if chose.count(TribeList[ii]) != 0:
                            continue
                        chose.append(TribeList[ii])
            if len(chose) == 2:
                break

        ####选择父母进行结合
        ParentAS = []
        ParentBS = []
        ChildCS = []
        ChildDS = []
        ParentAS = Output[0][chose[0][2]]
        ParentBS = Output[0][chose[1][2]]
        LeftJP = int(random.random() * 10)
        RightJP = int(random.random() * (10 - LeftJP)) + LeftJP
        Ap = ParentAS[LeftJP:RightJP]
        Bp = ParentBS[LeftJP:RightJP]
        for item in ParentAS:
            if Bp.count(item) == 0:
                Bp.append(item)
        ChildCS = copy.deepcopy(Bp)

        for item in ParentBS:
            if Ap.count(item) == 0:
                Ap.append(item)
        ChildDS = copy.deepcopy(Ap)

        ParentAA = []
        ParentBA = []
        ChildCA = []
        ChildDA = []
        ParentAA = Output[1][chose[0][2]]
        ParentBA = Output[1][chose[1][2]]
        Ap = ParentAA[LeftJP:RightJP]
        Bp = ParentBA[LeftJP:RightJP]
        for item in ParentAA:
            if Bp.count(item) == 0:
                Bp.append(item)
        ChildCA = copy.deepcopy(Bp)

        for item in ParentBA:
            if Ap.count(item) == 0:
                Ap.append(item)
        ChildDA = copy.deepcopy(Ap)

        Output[0].append(ChildCS)
        Output[0].append(ChildDS)
        Output[1].append(ChildCA)
        Output[1].append(ChildDA)
        ceshi_var = ChangeLtoV(Output)

        ceshi_tribe = []
        for im in range(len(Output[0])):
            K[0] = len(ceshi_var[0][im])
            K[1] = len(ceshi_var[1][im])
            X = []
            for rr in r:
                R = []
                for kk in range(K[rr - 1]):
                    Kk = []
                    for ii in i:
                        I = []
                        for ij in i:
                            I.append(0)
                        Kk.append(I)
                    R.append(Kk)
                X.append(R)
            del rr, kk, ii, ij, R, Kk, I
            Y = []
            for rr in r:
                R = []
                for kk in range(K[rr - 1]):
                    Kk = []
                    for ii in i:
                        Kk.append(0)
                    R.append(Kk)
                Y.append(R)
            del rr, kk, ii, R, Kk
            for rr in r:
                for kk in range(K[rr - 1]):
                    X[rr - 1][kk][0][ceshi_var[rr - 1][im][kk][0]] = 1
                    for ii in range(len(ceshi_var[rr - 1][im][kk]) - 1):
                        X[rr - 1][kk][ceshi_var[rr - 1][im][kk][ii]][ceshi_var[rr - 1][im][kk][ii + 1]] = 1
                        Y[rr - 1][kk][ceshi_var[rr - 1][im][kk][ii]] = 1
                    X[rr - 1][kk][ceshi_var[rr - 1][im][kk][len(ceshi_var[rr - 1][im][kk]) - 1]][0] = 1
                    Y[rr - 1][kk][ceshi_var[rr - 1][im][kk][len(ceshi_var[rr - 1][im][kk]) - 1]] = 1
                    X[rr - 1][kk][0][0] = 1
                    Y[rr - 1][kk][0] = 1
            newT = []
            newT.append(YueShu())
            newT.append(Target(X, d, K))
            newT.append(im)
            ceshi_tribe.append(newT)
        ceshi_tribe.sort()
        RemoveList = []
        RemoveList.append(ceshi_tribe[len(ceshi_tribe) - 1][2])
        RemoveList.append(ceshi_tribe[len(ceshi_tribe) - 2][2])
        RemoveList.sort()
        for item in RemoveList[::-1]:
            Output[0].pop(item)
            Output[1].pop(item)


    else:
        #####发生突变
        TuBian = int(random.random() * len(Output))
        Left = int(random.random() * 10)
        Right = int(random.random() * (10 - Left) + Left)
        Output[0][TuBian][Left:Right] = Output[0][TuBian][Left:Right][::-1]

    Yichuandiedai = Yichuandiedai + 1
    print Yichuandiedai
    if Yichuandiedai == End:
        print Yichuandiedai
        break

best = TribeList[0]
print best
print Output[0][best[2]]
print Output[1][best[2]]

best_var = ChangeLtoV(Output)

print best_var[0][best[2]]
print best_var[1][best[2]]

bestS = best_var[0][best[2]]
bestA = best_var[1][best[2]]


def CalculateTimeWindow(Svar, Avar):
    for ilist in Svar:
        for ii in range(len(ilist)):
            if ii == 0:
                T1[ilist[ii]] = t[0][0][ilist[ii]] + S[0][ilist[ii]]
            else:
                T1[ilist[ii]] = T1[ilist[ii - 1]] + t[0][ilist[ii - 1]][ilist[ii]]

    for ilist in Avar:
        for ii in range(len(ilist)):
            if ii == 0:
                T2[ilist[ii]] = t[1][0][ilist[ii]]
            else:
                T2[ilist[ii]] = T2[ilist[ii - 1]] + t[1][ilist[ii - 1]][ilist[ii]] + S[1][ilist[ii - 1]] + w2[
                    ilist[ii - 1]]
            if T2[ilist[ii]] < T1[ilist[ii]]:
                w2[ilist[ii]] = max(0, T1[ilist[ii]] - T2[ilist[ii]])
    return w2


for ilist in best_var[0][best[2]]:
    for ii in range(len(ilist)):
        if ii == 0:
            T1[ilist[ii]] = t[0][0][ilist[ii]] + S[0][ilist[ii]]
        else:
            T1[ilist[ii]] = T1[ilist[ii - 1]] + t[0][ilist[ii - 1]][ilist[ii]]

for ilist in best_var[1][best[2]]:
    for ii in range(len(ilist)):
        if ii == 0:
            T2[ilist[ii]] = t[1][0][ilist[ii]]
        else:
            T2[ilist[ii]] = T2[ilist[ii - 1]] + t[1][ilist[ii - 1]][ilist[ii]] + S[1][ilist[ii - 1]] + w2[ilist[ii - 1]]
        if T2[ilist[ii]] < T1[ilist[ii]]:
            w2[ilist[ii]] = max(0, T1[ilist[ii]] - T2[ilist[ii]])

for ilist in best_var[0][best[2]]:
    for ii in range(len(ilist)):
        if ii == 0:
            T1[ilist[ii]] = t[0][0][ilist[ii]] + S[0][ilist[ii]]
        else:
            T1[ilist[ii]] = T1[ilist[ii - 1]] + t[0][ilist[ii - 1]][ilist[ii]]

for ilist in best_var[1][best[2]]:
    for ii in range(len(ilist)):
        if ii == 0:
            T2[ilist[ii]] = t[1][0][ilist[ii]]
        else:
            T2[ilist[ii]] = T2[ilist[ii - 1]] + t[1][ilist[ii - 1]][ilist[ii]] + S[1][ilist[ii - 1]] + w2[ilist[ii - 1]]
        if T2[ilist[ii]] < T1[ilist[ii]]:
            w2[ilist[ii]] = max(0, T1[ilist[ii]] - T2[ilist[ii]])
            T2[ilist[ii]] = T1[ilist[ii]]

# Wdengdai=[0,0,0,0,0,0,0,0,0,0,0]
# for jj in j:
#    w2[jj]=T1[jj]-T2[jj]
#    if w2[jj]!=0:
#        for ij in j[j.index(jj)+1:]:
#            w2[ij]=w2[ij]+w2[jj]
#    Wdengdai[jj]=max(0,abs(T1[jj]-T2[jj]))
print T1
print T2
print w2
#    break
# X=OutputX[0]
# Y=OutputY[0]
# K1=OutputK1[0]
# K2=OutputK2[0]
#
# YueShu()
#
# print random.random()
# print X[0][:][:][:]
# a=np.array([11,2,3])
# b=np.array([1,2,3])
# print a*b

# def Backtrack(i,C,S,Output,Num,Small,Large,best,d):
#    global besttp
#    global bestnum
#    if i>Num:
#        if besttp>C and len(Output)>bestnum:
#            besttp=C
#            bestnum=len(Output)
#            new=copy.deepcopy(Output)
#            best.append(new)
#        return
#    flag=0
#    jiashe=copy.deepcopy(Output)
#    jiashe.append(S[i])
#    if (CalculateT(C,Large,jiashe)<=10 and CalculateW(Small,Large,jiashe)<=1200):
#        Output.append(S[i])
#        C=PingjiaFunction()
#        Backtrack(i+1,C,S,Output,Num,Small,Large,best,d)
#        Output.pop(Output.index(S[i]))
#        C=CalculateC(Output,d)
#        flag=1
#        
#    if flag==1:
#        Backtrack(i+1,C,S,Output,Num,Small,Large,best,d)
#    

#
# def CalculateC(MJ,d):
#    C=0.0
#    for i in range(len(MJ)-1):
#        C=C+d[i][i+1]
#    C=C+d[MJ[len(MJ)-1]][0]
#    return C
#
# def lujingSelect(S,d):
#    Out=[]
#    for x in S:
#        new=[]
#        new.append(x)
#        Out.append(new)
#        
#
# def PingjiaFunction(MAJ,MSJ,i,j,d):
#    global V
#    CV=V-400*i-200*j
#    Sa=0
#    Ss=0
#    for x in range(i):
#        Sa=Sa+CalculateC(MAJ[x],d)
#    for x in range(j):
#        Ss=Ss+CalculateC(MSJ[x],d)
#    CV=CV-Sa-Ss
#    return CV
#    
# x=np.array([0,10,30,50,50,30,-10,-30,-40,-40,-30])
# y=np.array([0,40,20,10,-10,-30,-30,-50,-10,20,50])
# d=[[],[],[],[],[],[],[],[],[],[],[]]
# for i in range(11):
#    for j in range(11):
#        d[i].append(math.hypot(x[i]-x[j],y[i]-y[j]))    # hypot(x,y)  sqrt(x*x+y*y)
# d=np.array(d)
#
# S=[0,1,2,3,4,5,6,7,8,9,10]
# Small=[0,2,3,5,6,0,4,3,1,6,1]
# Large=[0,2,1,0,0,3,0,2,1,0,3]
# Output=[0]
# best=[]
# besttp=1000
# bestnum=0
# Num=len(S)-1
# Backtrack(1,0.0,S,Output,Num,Small,Large,best,d)
# C=CalculateC(best[0],d)
# print CalculateT(C,Large,best[0])
#
# print CalculateW(Large,Small,best[0])
#
# print CalculateC(best[0],d)

# for x in best[0]:
#    S.pop(S.index(x))
#    
#
# Small=[0,2,3,5,6,0,4,3,1,6,1]
# Large=[0,2,1,0,0,3,0,2,1,0,3]
# Output2=[0]
# best2=[]
# besttp=1000.0
# bestnum=0
# Num2=len(S)-1
# Backtrack(1,0.0,S,Output2,Num2,Small,Large,best2,d)
#        
# C=CalculateC(best2[0],d)
# print CalculateT(C,Large,best2[0])
#
# print CalculateW(Large,Small,best2[0])
#
# print CalculateC(best2[0],d)
