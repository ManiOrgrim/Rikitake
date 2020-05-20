#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:09:06 2020

@author: mani
"""
import numpy as np
import matplotlib.pylab as plt
import matplotlib.pyplot as pyplot


def get_data(filename):
    """this function opens the input file and read the lines containing data.
    Returns a list of floats for time and variables"""
    infile=open(filename, 'r')
    lines=infile.readlines()
    mu, k =get_param_values(lines[0])
    data=np.empty((len(lines[2:]), 4))
    for i in range(len(lines[2:])):
        line=lines[2+i]
        values=line.split(';')
        data[i]=[values[1],values[2], values[3], values[4]]
    return data, mu, k

def get_param_values(line):
    """this function takes the parameter values form the specific string in the input file"""
    mu=float(line.split()[1])
    k=float(line.split()[3])
    return mu, k

def calculate_lyapunov(filename_1, filename_2):
    data_1, mu_1, k_1=get_data(filename_1)
    data_2, mu_2, k_2=get_data(filename_2)
    lenght=len(data_1)
    assert lenght==len(data_2)
    assert mu_1==mu_2
    assert k_1==k_2
    difference=data_1-data_2
    norms=np.linalg.norm(difference, axis=1)
    norm_0=norms[0]
    log_diff_ratio=np.log(norms/norm_0)
    lyaps=np.empty(lenght)
    for i in range(1,lenght):
        if (i%10000==0):
            print("sono al ", i*100/lenght, '%')
        lyaps[i]=np.mean(log_diff_ratio[:i])
    return lyaps

def get_results():
    filename=[]
    for n in range (1,4):
        filename.append("simulation_"+str(n)+".csv")
    lyaps=[]
    for file in filename:
        lyaps.append(calculate_lyapunov("simulation_0.csv", file))
    results=[]
    for lyap in lyaps:
        lenght_ten=int(len(lyap)/10)
        last_lyap=lyap[lenght_ten:]
        mean_lyap=np.mean(last_lyap)
        results.append(mean_lyap)
    return results, lyaps

def plot_exponents():
    fig, subplots = plt.subplots(1, 3, figsize=(12, 4))
    values, series=get_results()
    for i in range(3):
        subplots[i].plot(series[i], color='r')
        subplots[i].set_xlabel("simulation time")
        subplots[i].set_ylabel("Lyapuniov exponent estmate")
        subplots[i].hlines(values[i], 0, len(series[i]), label=str(values[i]))
        subplots[i].legend()
    return fig, values
    
fig, exp_values=plot_exponents()
fig.savefig("lyapunov_exp.png", bbox_inches='tight')
open_file=open("lyapunov_exp.dat",'w')
for v in exp_values:
    open_file.write(str(v))
        
    

