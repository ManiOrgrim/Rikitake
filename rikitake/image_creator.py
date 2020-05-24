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
    """this function opens the input file and read the lines containing data.
    Returns a list of floats for time and variables"""
    infile=open(filename, 'r')
    lines=infile.readlines()
    mu, k =get_param_values(lines[0])
    x1=[]
    x2=[]
    y1=[]
    y2=[]
    t=[]
    for instant in lines[2:]:
        data=instant.split(';')
        t.append(float(data[0]))
        x1.append(float(data[1]))
        x2.append(float(data[2]))
        y1.append(float(data[3]))
        y2.append(float(data[4]))
    infile.close()
    return t, x1, x2, y1, y2, mu, k

def get_param_values(line):
    """this function takes the parameter values form the specific string in the input file"""

    mu=float(line.split()[1])
    k=float(line.split()[3])
    return mu, k
    
    

def generate_image(filename):
    """ this function creates the (x2,y1) plot saving it in working directory as 'filename.png'"""
    plt.figure(figsize=(10,10))
    t, x1, x2, y1, y2, mu, k=get_data(filename)
    plt.plot(x2,y1)
    title_text='Rikitake dynamo phase space with mu ='+str(mu)+' k='+str(k)
    plt.suptitle(title_text,fontsize=20)
    plt.xlabel('x2', fontsize=18)
    plt.ylabel('y1', fontsize=18)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'.png'
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
def get_simulation_ID(save_dir):
    in_file=open(save_dir+"/input_values.txt",'r')
    line=in_file.readline()
    split_line=line.split()
    simulation_ID=split_line[-1]
    return simulation_ID

def generate_images(save_dir):
   simulation_ID=get_simulation_ID(save_dir)    
   files=[save_dir+'/'+simulation_ID+'_'+str(i)+'.csv' for i in range(4)]

   for file in files:
       generate_image(file)
