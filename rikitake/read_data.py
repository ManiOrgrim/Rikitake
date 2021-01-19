#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:55:15 2020

@author: mani
"""
import numpy as np
import sys
from plumbum import colors

def get_param_values(line):
    """this function takes the parameter values from the specific string in the input file.
    PARAMETERS:
        line: (string) String from wich the parameters mu and k will be read.
    RETRNS:
        mu  : (float) Value of mu.
        k   : (float) Value of k"""

    mu=float(line.split()[1])
    k=float(line.split()[3])
    return mu, k

def get_data(filename, form):
    if (form=='1'):
        return get_data_format1(filename)
    elif (form=='2'):
        return get_data_format2(filename)
    else:
        raise ValueError('Wrong paramteter in get_data function')
        pass

def get_data_format1(filename):
    """this function opens the input file and read the lines containing data.
    PARAMETERS:
            filename: (string) name of the file from which informations will be read.
    RETURNS:
            t       : (float[N_steps]) series of time values
            x1      : (float[N_steps]) series of x1 values
            x2      : (float[N_steps]) series of x2 values
            y1      : (float[N_steps]) series of y1 values
            y2      : (float[N_steps]) series of y2 values
            mu      : (float) value of mu
            k       : (float) value fo k """
    try:
       infile=open(filename, 'r')
    except OSError:
       print(colors.red|"\nCould not open {}, maybe you did not perform integration first?".format(filename), file=sys.stderr)
       sys.exit([1]) #4: could not open integration files
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

def get_data_format2(filename):
    """this function opens the input file and read the lines containing data.
    differs from get_data_format1 in the format (but not in the contents) of the output
    PARAMETERS:
        filename: (string) name of the file from which informations will be read.
    RETURNS:
        data    : (float[N_series, 4]) value of [x1, x2, y1, y2] at each time step
        mu      : (float) value of mu
        k       : (float) value fo k """
    try:
       infile=open(filename, 'r')
    except OSError:
       print(colors.red|"\nCould not open {}, maybe you did not perform integration first?".format(filename), file=sys.stderr)
       sys.exit([1]) #4: could not open integration files
    
    lines=infile.readlines()
    mu, k =get_param_values(lines[0])
    data=np.empty((len(lines[2:]), 4))
    for i in range(len(lines[2:])):
        line=lines[2+i]
        values=line.split(';')
        data[i]=[values[1],values[2], values[3], values[4]]
    return data, mu, k

def get_simulation_ID(save_dir):
    """This function gets the simultaion_ID for this particular integration.
    PARAMETERS:
        save_dir     : (string) Directory in which the 'input_values.txt' file is stored.
    RETURNS:
        simulation_ID: (string) String object reporting simulation_ID."""
    try:
       in_file=open(save_dir+"/input_values.txt",'r')
    except OSError:
        print(colors.red|"Could not open input_values.txt file")
        sys.exit([2]) #could not open input_values.txt
    line=in_file.readline()
    split_line=line.split()
    simulation_ID=split_line[-1]
    return simulation_ID