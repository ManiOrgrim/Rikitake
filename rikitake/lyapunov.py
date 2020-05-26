#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:09:06 2020
@author: mani
"""
import numpy as np
import matplotlib.pylab as plt
import read_data


def calculate_lyapunov(filename_1, filename_2):
    data_1, mu_1, k_1=read_data.get_data(filename_1,'2')
    data_2, mu_2, k_2=read_data.get_data(filename_2,'2')
    lenght=len(data_1)
    assert lenght==len(data_2)
    assert mu_1==mu_2
    assert k_1==k_2
    difference=data_1-data_2
    norms=np.linalg.norm(difference, axis=1)
    norm_0=norms[0]
    log_diff_ratio=np.log(norms/norm_0)
    lyaps=np.empty(lenght)
    sum_til_now=0 ####
    for i in range(1,lenght):
        if (i%10000==0):
            print("sono al ", i*100/lenght, '%')
        sum_til_now+=log_diff_ratio[i]####
        #lyaps[i]=np.mean(log_diff_ratio[:i])
        lyaps[i]=sum_til_now/i
    return lyaps


def get_results(simulation_ID, save_dir):
    
    filename=[save_dir+'/'+simulation_ID+'_'+str(i)+'.csv' for i in range(4)]
    lyaps=[calculate_lyapunov(filename[0],file) for file in filename[1:]]
    results=[]
    for lyap in lyaps:
        lenght_ten=int(len(lyap)/10)
        last_lyap=lyap[lenght_ten:]
        mean_lyap=np.mean(last_lyap)
        results.append(mean_lyap)
    return results, lyaps

def plot_exponents(simulation_ID, save_dir):
    fig, subplots = plt.subplots(1, 3, figsize=(12, 4))
    values, series=get_results(simulation_ID, save_dir)
    for i in range(3):
        subplots[i].plot(series[i], color='r')
        subplots[i].set_xlabel("integration steps")
        subplots[i].set_ylabel("Lyapuniov exponent estmate")
        subplots[i].hlines(values[i], 0, len(series[i]), label=str(values[i]))
        subplots[i].legend()
    return fig, values

def lyapunov(save_dir):
   simulation_ID=read_data.get_simulation_ID(save_dir)   
   fig, exp_values=plot_exponents(simulation_ID, save_dir)
   fig.savefig(save_dir+'/'+simulation_ID+"lyap_exp.png", bbox_inches='tight')
   open_file=open(save_dir+'/'+simulation_ID+"lyapunov_exp.dat",'w+')
   for v in exp_values:
       open_file.write(str(v)+' ')