#!/usr/bin/python
###########################################################################
# filename      : taxa.py
# date written  : 24/12/2013
# written by    : THChew (teonghan@gmail.com)
# description   : convert taxanomies & values?
# last update   : 24/12/2013    - version 0.1
#                 26/12/2013    - dealing with chloroplast entries
###########################################################################
'''
k(ingdom a.k.a domain) > p(hylum) > c(lass) > o(rder) > f(amily) > g(enus)
'''
import csv
import sys

if len(sys.argv)!=int(2):
    print "Invalid argument"
    print "Usage: python taxa.py input_file"

else:

    inputfile=str(sys.argv[1])
    out=inputfile+'.out'
    '''
    inputfile='To_convert.stat'
    '''
    data=[]
    chloroplast=[]
    taxa=['kingdom','phylum','class','order','family','genus']

    with open(inputfile,'r') as csvfile:
        csvreader=csv.reader(csvfile,delimiter='\t')
        for row in csvreader:
            if row[0]!='taxid':
                if row[0]=='0':
                    ABS=float(row[4])
                else:
                    TMP=row[1].split(';')[2:-1]
                    if 'subclass' in TMP or 'suborder' in TMP:
                        TMP=[]
                    FIX=[]
                    if len(TMP)!=0:
                        for i in range(1,len(TMP),2):
                            if TMP[i][0:3]!='sub':
                                if TMP[i]=='domain':
                                    TMP[i]='kingdom'
                                FIX.append([TMP[i],TMP[i-1].replace('"','')])
                        
                        for i in range(0,len(FIX)):
                            if FIX[i][0]=='':
                                if FIX[i-1][0]=='':
                                    FIX[i][0]=taxa[0]
                                else:
                                    INDEX=taxa.index(FIX[i-1][0])
                                    FIX[i][0]=taxa[INDEX+1]

                        STR=''
                        for i in range(0,len(FIX)):
                            if STR=='':
                                STR=STR+FIX[i][0][0]+'__'+FIX[i][1]
                            else:
                                STR=STR+'|'+FIX[i][0][0]+'__'+FIX[i][1]

                        if 'chloroplast' in STR.lower():
                            chloroplast.append([STR,float(row[4])])
                        else:
                            data.append([STR,float(row[4])])

    chloroplast.sort()
    root=chloroplast[0]
    error=[]

    #----------------------------------------------------
    # checking if all chloroplast share the same ancestor
    #----------------------------------------------------
    for i in range(1,len(chloroplast)):
        if root[0] not in chloroplast[i][0]:
            error.append(chloroplast[i])

    if len(error)==0:
        ABS=ABS-root[1]
        for i in range(0,len(data)):
            '''
            if i==0:
                data[i][1]=((data[i][1]-root[1])*100)/ABS
            '''
            else:
                data[i][1]=(data[i][1]*100)/ABS

        fout=open(out,'w')
        for i in data:
            fout.write('%s\t%f\n' % (i[0],i[1]))
        fout.close()
        
    else:
        print '[error] Some chloroplast entries do not share the same root...'


