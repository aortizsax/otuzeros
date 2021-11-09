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
    FILENAME: 

"""

import pandas as pd
import sys
import os


from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np



def MakeFileForZeroFilteringCutoff(d,OUTFILE,itterwhere=0):
    d=pd.read_table(d,
                delimiter='\t')
    histarray = []
    for i in d.iterrows():
        if histarray != []:
            pass
        else:
            try:
                for ii in i[itterwhere]:
                    histarray.append(0)
            except TypeError:
                itterwhere += 1
                for ii in i[itterwhere]:
                    histarray.append(0)
    
    totspec = 0
    for i in d.iterrows():
        totspec += 1
        totsamp = 0
        numzeros = 0
        for ii in i[itterwhere]:
            totsamp += 1
            if (ii == 0.0)|(ii == '0.0'):
                numzeros +=1
        histarray[numzeros] +=1
        

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
    return (totsamp,totspec)
        

if __name__ == '__main__':
    
    print("")
    print("")
    print("")
    
    #commandline check
    if len(sys.argv) <2:
        print("Usage:")
        print("    python calccutoff.py OTUtablefile")
        print("Where:")
        print(" ")   
        print("")
        print("")
        exit()
            
    FILENAME = sys.argv[1]
    PATH = '/'.join(sys.argv[1].split("/")[:-1])+'/zerofilteredOTU'


    # Check whether the specified path exists or not
    isExist = os.path.exists(PATH)
    
    if isExist == False:
          # Create a new directory because it does not exist 
          os.makedirs(PATH)
          print("The new directory is created! PATH:",PATH)

    OUTFILE = PATH+'/processing.txt'
    dimen = MakeFileForZeroFilteringCutoff(FILENAME, OUTFILE)
    
    print("Processing file saved to:",OUTFILE)
    
    print("")
    print("")
    print("")
    
    

        
    processfile = OUTFILE
    bact_zero_table = {}
    with open(processfile, 'r') as f:
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
    x_axis = list(bact_zero_table.keys())
    #save orginal
    y_original = y_axis.copy()
    #intialize array for reverse original
    y_OGrev = np.zeros((1,len(y_axis)))[0]
    
    acc = 0 #acculumation of yvalues
    i=0 #index
    # Sorting by acculuating
    for y in y_axis:#Accultion of histogram for monotonically decreasing funciton
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
    
    #yaxix 2 TRANSFORMATION
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
    



    # find the last max local maximum 
    for k in range(1,len(kappa)-1):
        #print(kappa[k])
        if kappa[k]-kappa[k-1]>0:        
            if kappa[k+1]-kappa[k]<0:
                maxCurv = kappa[k]
                
    # maxCurv = max(kappa[20:]) old find max 
    index = kappa.index(maxCurv)
    cutoff = xs[index]+0.5
    

    
    print("Recommended  Cutoff: Keep features with up to and including",str(round(cutoff,2)),"zeros")
    print("")
    print("")
    print("")
    
    

    
    
    
    #plot Curvature    
    plt.plot(xs,kappa)#,color=colmapBIO[clustNum])
    plt.gca().xaxis.grid(True)
    plt.title('Maximizing Curvature')
    plt.xlabel("# samples species is absent")
    plt.ylabel('# of species')
    plt.savefig(PATH+'/maxcurvplot.png')
    plt.show()
    
    
    

    
    cutoffabsent = cutoff
    cutoff = dimen[0]-cutoff
    presentheight = y_original.copy()
    presentheight.reverse()
    presentx = x_axis.copy()
    presentx.reverse()
    presentheight = np.subtract(dimen[1],presentheight)
    presentx = np.subtract(dimen[0],presentx)
    strt = 0
    end = -1
    
    plt.bar(x=presentx,height=presentheight)
    plt.xlabel("# samples species is present")
    plt.ylabel('# of species')
    plt.title('Trim Features that are present in less than ' +str(cutoff)+ ' samples')
    plt.axvline(x=cutoff,color='red')
    plt.xlim([0,50])
    plt.savefig(PATH+'/processingcutoff.png')

    plt.show()
    
    
    df = pd.read_csv(FILENAME,sep='\t')#index_col=0,header = 0)
    

    
    if df.columns.to_list()[0] == '# Constructed from biom file':
        df = pd.read_csv(FILENAME,
                         sep='\t',
                         skiprows=1)#index_col=0,header = 0)
        
    
    iszero = df == 0.0
    ispres = df != 0.0
    
    OTUzerofiltered = df[ispres.sum(axis=1)>cutoff]
    OTUzerofiltered.to_csv(PATH+'/table.zerofiltered.csv')
   
    print("Zero Filtered OTU table saved:",PATH+'/table.zerofiltered.csv')

    
    
    
    
    