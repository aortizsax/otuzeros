# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:56:13 2020

@author: aorti

This code is meant to help the user define how many zeros to keep in their OTU 
table with mathematical backing. 

Load values min to max.

Input is a histogram of the number of features (yaxis)
with a certain number of zeros(xaxis). 

The histogram is then tansformed with log(hist + c)
y = log(hist + c)

A curve representing the transfromed histogram data is be made with cubic-splines. 
ys = cubicspline of y

By maximixing curvature (minizing the radius of the curve), the user can see 
when the histogram columns start to ramp up. That point where it ramps up will 
the cut off.

curvature: kappa = 1/Radius = |ys''| * (1 + ys'^2)^(-3/2)

Usage:
    python 2020-12-09_autoCutoff.py FILENAME
    
Where:
    FILENAME: is the file with the histogram data
        File Format: one row of number of zeros 
                     one row of number of features with the coorisponging 
                         of zeros from the first row
            EX: (spaces are added for ease of view) 
                1,3,4,5,6,7,8,10,11,12,13,14,15,16,17, 18,  19,  20
                1,1,5,8,4,3,2,3, 4, 2, 11,18,34,55,74,171,1272,8697

            Note: 8697 features have 0s in 20 samples

"""


import pandas as pd
import sys

from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np
import math



def MakeFileForZeroFilteringCutoff(d,OUTFILE,itterwhere=0):
    d=pd.read_table(d,
                delimiter='\t')
    histarray = []
    for i in d.iterrows():
        if histarray != []:
            pass
        else:
            for ii in i[itterwhere]:
                histarray.append(0)
    
    for i in d.iterrows():
        numzeros = 0
        for ii in i[itterwhere]:
            if ii == 0.0:
                numzeros +=1
        histarray[numzeros] +=1
        
    #print(histarray)
        
    c = 0
    carray = []
    hist=[0]*len(histarray[:-1])
    for i in histarray[:-1]:
        hist[c] = str(i)
        c += 1
        carray.append(str(c))
    
    c = 0
    with open(OUTFILE, 'w+') as f:
        f.write(','.join(carray)+'\n')
        f.write(','.join(hist))
        

if __name__ == '__main__':
    
    print("")
    print("")
    print("")
    
    #commandline check
    if len(sys.argv) <3:
        print("Usage:")
        print("    python 2020-12-09_autoCutoff.py OTUtablefile")
        print("Where:")
        print("    FILENAME: is the file with the histogram data")
        print("        File Format: one row of number of zeros")
        print("                     one row of number of features with the coorisponding ")
        print("                         of zeros from the first row")
        print("            EX: (spaces are added for ease of view) ")
        print("                1,3,4,5,6,7,8,10,11,12,13,14,15,16,17, 18,  19,  20")
        print("                1,1,5,8,4,3,2,3, 4, 2, 11,18,34,55,74,171,1272,8697")
        print("            Note: 8697 features have 0s in 20 samples")
        print("")
        print("")
        print("")
        exit()
            
    FILENAME = sys.argv[1]
    OUTFILE = 'processing.txt'
    itterwhere = int(sys.argv[2])
    MakeFileForZeroFilteringCutoff(FILENAME, OUTFILE,itterwhere)
    
    print("Histogram array for autoCutoff.py saved to:",OUTFILE)
    
    print("")
    print("")
    print("")
    
    

        
    FILENAME = OUTFILE
    bact_zero_table = {}
    with open(FILENAME, 'r') as f:
        read_data = f.read()
        a = read_data.split("\n")
        b = a[1].split(",")
        a = a[0].split(",")
    
        #histogram information as dictionary
        for i in range(len(a)):
            bact_zero_table[int(a[i])] = int(b[i])
    #transformation constant
    con = [100,1,1000]#,100000]
    conK = con[0]
    
    
    #yvalues are hieght from histograms
    y_axis = list(bact_zero_table.values())[:]
    #initialize postion from histogram
    x_axis = list(bact_zero_table.keys())#range(1,len(y_axis)+1)
    #save orginal
    y_original = y_axis.copy()
    #intialize array for reverse original
    y_OGrev = np.zeros((1,len(y_axis)))[0]
    acc = 0 #acculumation of yvalues
    i=0 #index
    
    # Sorting by acculuating
    for y in y_axis:#Accultion of 
        acc += y 
        y_axis[i] =acc
        i+=1
        
    #initialize yaxis 2 become
    y_axis2 = np.zeros((1,len(y_axis)))[0]
    for i in range(len(y_axis)):####reverse!!!!
        index = i#len(y_axis) - i -1
        y_axis2[index] = y_axis[i]
        y_OGrev[index]=y_original[i]
    y_axis = y_axis2.copy()
    
    #yaxix 2 become
    y_axis2 = []
    for y in y_axis:
        trans = np.log(y+conK)  
        y_axis2.append(trans)
    y_axis = y_axis2.copy()
    y_avg = sum(y_axis)/len(y_axis)
    
    #Cubic slpine
    cs = CubicSpline(x_axis,y_axis)#yaxis spline and derivatives 
    #xaxis spline
    step=0.05
    xs = np.arange(x_axis[0], x_axis[-1], step)
    
    #initalize curvature array
    kappa = []
    for i in range(len(xs)):
        kTemp = abs(cs(xs,2)[i]) #numerator
        kTemp /= ((1 + ( cs(xs,1)[i])**2 )**(3/2)) #denominator
        kappa.append(kTemp)
    
    #plot Curvature    
    plt.plot(xs,kappa)#,color=colmapBIO[clustNum])
    plt.xticks(np.arange(0, 20, 1)) 
    plt.gca().xaxis.grid(True)
    plt.title('Maximizing Curvature')
    plt.show()
    
    #PLOT ORIGINAL HIST
    plt.bar(x=x_axis,height=y_OGrev)
    plt.xticks(np.arange(0, 20, 1)) 
    plt.xlabel('Number of zeros in feature')
    plt.ylabel('Number of features')
    plt.title('Orignal Histogram')
    plt.show()

    # find the last max local maximum 
    for k in range(1,len(kappa)-1):
        #print(kappa[k])
        if kappa[k]-kappa[k-1]>0:        
            if kappa[k+1]-kappa[k]<0:
                maxCurv = kappa[k]
                
    # maxCurv = max(kappa[20:]) old find max 
    index = kappa.index(maxCurv)
    cutoff = xs[index]+0.5
    
# =============================================================================
#     print("Recommended  Cutoff: Keep features with up to and including",str(round(cutoff,2)),"zeros")
# =============================================================================
    print("Recommended  Cutoff: Keep features with up to and including",str(int(cutoff)),"zeros")
    
# =============================================================================
#  
#     bact_zero_table[round(cutoff,2)] = 'Cut here'
#     finaldict = {k : bact_zero_table[k] for k in sorted(bact_zero_table.keys())}
#     print("Where to cut the original data:",finaldict)
#     
#     print("")
#     print("")
#     print("")
# =============================================================================
