# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 14:20:07 2021

@author: aorti
"""
import pandas as pd
import sys


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
            if ii == '0.0':
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
    if len(sys.argv) <2:
        print("Usage:")
        print("    python 2020-12-09_autoCutoff.py FILENAME")
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
    OUTFILE = sys.argv[2]
    itterwhere = int(sys.argv[3])
    MakeFileForZeroFilteringCutoff(FILENAME, OUTFILE,itterwhere)
    
    print("Histogram array for autoCutoff.py saved to:",OUTFILE)
    
    print("")
    print("")
    print("")
# =============================================================================
#     
#     
# ##periodontal data
# d=pd.read_table('../../OralCoda/data/emp-single-end-sequences/taxon-7-gg-nb-exported-feature-table/PT_table.from_biom.txt',
#                 delimiter='\t')
# d=pd.read_table('../../OralCoda/data/emp-single-end-sequences/taxon-7-gg-nb-exported-feature-table/PT_table.from_biom.txt',
#                 delimiter='\t')
# 
# MakeFileForZeroFilteringCutoff(d,
#                                '../data/PTforcoda.txt')
# 
# ###periodontal data
# d=pd.read_table('../../OralCoda/mSysData/metagenomic/Clorox_NARCH_kraken_o.txt',
#                 delimiter='\t')
# 
# d=pd.read_table('../../OralCoda/mSysData/16S/taxtable/exported-feature-table/SHT_table.from_biom.txt',
#                 delimiter='\t')
# MakeFileForZeroFilteringCutoff(d,
#                                '../data/SHTforcoda.txt')
# 
# 
# ###nick data
# d=pd.read_table('../data/nickdata/table.from_biom.tsv',
#                 delimiter='\t')
# MakeFileForZeroFilteringCutoff(d,
#                                '../data/nickdataforcoda.txt')
# 
# ###alex data
# d=pd.read_table('../data/alexdata/table.from_biom.tsv',
#                 delimiter='\t')
# 
# MakeFileForZeroFilteringCutoff(d,
#                                '../data/alexdataforcoda.txt')
# 
# =============================================================================
