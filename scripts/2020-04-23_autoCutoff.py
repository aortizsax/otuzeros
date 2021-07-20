# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:56:13 2020

@author: aorti
"""

#bact_zero_table = {1:1,3:1,4:5,5:8,6:4,7:3,8:2,10:3,11:4,12:2,13:11,14:18,15:34,16:55,17:74,19:1272,20:8697}
bact_zero_table = {0:11,1:2,2:4,3:3,4:1,5:11,6:5,7:3,8:10,9:5,10:15,11:16,12:16,13:31,14:27,15:66,16:151,17:529,18:9459}
bact_zero_table = {3:2,4:2,5:5,6:2,7:2,8:1,9:2,10:1,11:3,12:3,13:6,14:4,15:9,16:16,17:37,18:96,19:247,20:2864,21:7060}

bact_zero_table = {2:1,3:3,4:7,5:3,6:2,7:4,8:1,9:2,10:2,11:5,12:3,13:16,14:24,15:36,16:55,17:135,18:823,19:9243}

#bact_zero_table = {6:1,7:3,8:5,9:3,13:1,15:2,16:1,17:2,18:6,19:16,20:29,21:44,22:109,23:689,24:9454}

# =============================================================================
# bact_zero_table = {1:1,2:1,3:7,4:2,9:2,10:1,12:2,13:7,14:9,15:13,16:22,17:59,18:148,19:983,20:9108}
# =============================================================================

# =============================================================================
# bact_zero_table = {2:1, 3:3, 5:4, 6:4, 7:4, 8:4, 9:5, 10:3,11:9,12:13,13:25,14:63,15:190,16:1719,17:8318}
# =============================================================================

from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np
import math

print(list(bact_zero_table.values()).reverse())

y_axis = list(bact_zero_table.values())#[:-1]
y_OG = y_axis.copy()
acc = 0
i=0
for y in y_axis:#CDF
    acc += y 
    y_axis[i] =acc
    i+=1
x_axis = range(len(y_axis))
print(y_axis,x_axis)


y_axis[:] = [x for x in y_axis]
y_axis2 = np.zeros((1,len(y_axis)))[0]#[]#list(range(len(y_axis)))
print(y_axis2)
# =============================================================================
# for i in range(len(y_axis)):####reverse!!!!
#     index = len(y_axis) - i -1
#     y_axis2[index] = y_axis[i]
#     y_OG[index]=y_axis[i]
# =============================================================================
#y_axis = y_axis2.copy()
print(y_axis)




y_axis2 = []
trans=0
temp = y_axis[0]
for y in y_axis:
    trans = (y)
    print(y,trans)
    y_axis2.append(trans)
    temp = 0
y_axis = y_axis2.copy()
y_avg = sum(y_axis)/len(y_axis)
#y_axis[:] = [math.atan(x) for x in y_axis]


#print(y_axis)
cs = CubicSpline(x_axis,y_axis)
xs = np.arange(x_axis[1], x_axis[-1], 0.05)
slope = max(y_axis)/len(y_axis)
maxList = {}
falseMaxDict={}
count=0
temp_prime = list(cs(xs,1))[0]
for y_prime in cs(xs,1):
    if y_prime > 0:
        print('here',xs[count],y_prime,y_prime/temp_prime,slope*0.05)
        if y_prime/temp_prime>slope*0.05:
            print('here')
            maxList[int(xs[count])] = list(cs(xs))[count]

# =============================================================================
#                 if list(cs(xs))[count] >0:
#     
#                 else:
#                     falseMaxDict[int(xs[count])] = list(cs(xs))[count]
# =============================================================================
    
    temp_prime = y_prime
    count+=1

print("maxDict",maxList)
maxRegi = list(maxList.keys())

plt.bar(x=x_axis,height=y_axis)
plt.show()
plt.bar(x=x_axis,height=y_OG)
plt.vlines(maxRegi,max(cs(xs,1)),min(cs(xs,1)),color='b',linestyles='dashed')
plt.show()



fig = plt.figure(figsize=(8,5), dpi=100)
axes = fig.add_subplot(1, 1, 1)
plt.scatter(x_axis,y_axis)
plt.plot(xs,cs(xs),label="S")#,color=colmapBIO[clustNum])
plt.xlabel('Amino Acid Index',fontsize=15)
plt.xticks(fontsize=15)

plt.yticks(fontsize=15)
plt.ylabel('Faith\'s Distance Transformed',fontsize=15)#_withoutArrow
# =============================================================================
# plt.savefig('../BSH_data/MotifScannerOut/2020-04-22_'+str(clustNum)+'_'+str(stepSize)+'_log10_MotifScanBSH.png')
plt.show()
# =============================================================================


plt.plot(xs,cs(xs,1),label="S'")#,color=colmapBIO[clustNum])
plt.legend()

plt.title('')
plt.xlabel('Amino Acid Index',fontsize=15)
plt.ylabel('Rate of Faiths Transforms per Amino Acid Index')
#plt.savefig('../BSH_data/MotifScannerOut/2020-04-22_ff_log10_MotifScanBSH_prime'+str(clustNum)+'.png')
plt.show()


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.spines['left'].set_position(('data', 0.0))
ax.spines['bottom'].set_position(('data', 0.0))
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.plot(xs,cs(xs,2),label="S''")#,color=colmapBIO[clustNum])
plt.legend()
plt.title('')
plt.xlabel('Amino Acid Index',fontsize=15)
plt.ylabel('Rate of Faiths Transforms per Amino Acid Index')
#plt.savefig('../BSH_data/MotifScannerOut/2020-04-22_ff_log10_MotifScanBSH_prime'+str(clustNum)+'.png')
plt.show()


# =============================================================================
# colvec = ['k' for i in range(len(maxRegi))]
# falseRegi = list(falseMaxDict.keys())
# colvec = ['r' for i in range(len(maxRegi))]
# =============================================================================



# =============================================================================
# anno_i = [(True,True)==i for i in [(x>230,x<=230+stepSize) for x in x_axis]].index(True)
# print(x_axis[anno_i],y_axis[anno_i])
# x_Curr = x_axis[anno_i]
# y_Curr = y_axis[anno_i]
# y_extend = (max(cs(xs))-min(cs(xs)))*0.1
# ###################################################
# 
# 
# attrDict = {}
# ###################################################
# fig = plt.figure(figsize=(5,4), dpi=100)
# plt.scatter(x_untrans,y_untrans,color=colmapBIO[clustNum])
# plt.vlines(maxRegi,max(y_untrans),min(y_untrans),color='b',linestyles='dashed')
# plt.vlines(falseRegi,max(y_untrans),min(y_untrans),color='r',linestyles='dashed')
# plt.title('')
# plt.xlabel('Amino Acid Index',fontsize=15)
# plt.ylabel('Faith\'s Distance',fontsize=15)
# plt.savefig('../BSH_data/MotifScannerOut/2020-04-22_clusternum'+str(clustNum)+'_MotifScanBSH.png')
# plt.show()
# ###################################################
# # =============================================================================
# #         plt.ylim(min(cs(xs)),max(cs(xs))+y_extend*1.1)
# #         axes.annotate('Scan Across Alignment',
# #             xy=(x_Curr+30, max(cs(xs))+y_extend-y_extend*0.4),
# #             #xycoords='data',
# #             xytext=(x_Curr-13, max(cs(xs))+y_extend-y_extend*0.4),
# #             fontsize=13,
# #             arrowprops=
# #                 dict(facecolor='black', shrink=0.05),
# #                 horizontalalignment='right',
# #                 verticalalignment='top')
# # =============================================================================
# 
# 
# 
#    
# 
# attrDict[maxRegi[1]] = []
# 
# 
# 
# =============================================================================
