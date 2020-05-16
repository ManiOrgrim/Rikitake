#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:00:07 2020

@author: mani
"""
import sys
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D

def get_data(filename):
    a=open(filename, 'r')
    u=a.readlines()
    x1=[]
    x2=[]
    y1=[]
    y2=[]
    t=[]
    for instant in u[2:]:
        data=instant.split(';')
        t.append(float(data[0]))
        x1.append(float(data[1]))
        x2.append(float(data[2]))
        y1.append(float(data[3]))
        y2.append(float(data[4]))
    a.close()
    return t, x1, x2, y1, y2

def pl0t_just_one(filename):
    plt.figure(figsize=(10,10))
    t, x1, x2, y1, y2=get_data(filename)
    plt.plot( x2,y1)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'.png'
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
def get_infile():
    return sys.argv[1]

pl0t_just_one(get_infile())