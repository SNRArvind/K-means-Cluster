# -*- coding: utf-8 -*-
"""
Created on Tue Sep 04 23:34:33 2018

Roll No: 18AT91R02
Name: Arvind Kumar Gupta
Assignment No.: 7

"""
import math 
import sys
from random import uniform
import pandas as pd

def FindColMinMax(items):
    n = len(items[0]);
    minima = [sys.maxsize for i in range(n)];
    maxima = [-sys.maxsize -1 for i in range(n)];
    
    for item in items:
        for f in range(len(item)):
            if(item[f] < minima[f]):
                minima[f] = item[f];
            
            if(item[f] > maxima[f]):
                maxima[f] = item[f];
    return minima,maxima;

def EuclideanDistance(x,y):
    S = 0; 
    for i in range(len(x)):
        S += math.pow(x[i]-y[i],2);

    return math.sqrt(S); 

def InitializeMeans(items,k,cMin,cMax):
    
    f = len(items[0]); 
    means = [[0 for i in range(f)] for j in range(k)];   
    for mean in means:
        for i in range(len(mean)):
            mean[i] = uniform(cMin[i]+1,cMax[i]-1);
    return means;

def UpdateMean(n,mean,item):
    for i in range(len(mean)):
        m = mean[i];
        m = (m*(n-1)+item[i])/float(n);
        mean[i] = round(m,3);    
    return mean;

def FindClusters(means,items):
    clusters = [[] for i in range(len(means))]; 
    
    for item in items:
        index = Classify(means,item);
        clusters[index].append(item);
    return clusters;

def Classify(means,item):
    minimum = sys.maxsize;
    index = -1;

    for i in range(len(means)):
        dis = EuclideanDistance(item,means[i]);
        if(dis < minimum):
            minimum = dis;
            index = i;    
    return index;


###_Main_###
train_set = pd.read_csv('data7.csv', header=None)
train_set = train_set.values
k = 2;
maxIterations=100000;

cMin, cMax = FindColMinMax(train_set);
means = InitializeMeans(train_set,k,cMin,cMax);
clusterSizes = [0 for i in range(len(means))];
belongsTo = [0 for i in range(len(train_set))];
for e in range(maxIterations):
    noChange = True;
    for i in range(len(train_set)):
        item = train_set[i];
        index = Classify(means,item);
        clusterSizes[index] += 1;
        means[index] = UpdateMean(clusterSizes[index],means[index],item);

        if(index != belongsTo[i]):
            noChange = False;
        belongsTo[i] = index;
    if(noChange):
        break;                      

output = [0 for i in range(len(train_set))];                      
clusters = FindClusters(means,train_set);
for i in range(len(belongsTo)):
    if (belongsTo[i]==0):
        output[i] =1
    if (belongsTo[i]==1):
        output[i]=2
    
print(output);

f2= open("18AT91R02_7.out","w+")
f2.write(str(output))
f2.close()
