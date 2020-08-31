#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:09:06 2020
@author: mani
"""
import numpy as np
import matplotlib.pylab as plt
import read_data
import sys
from plumbum.cli.terminal import Progress
from plumbum import colors



def calculate_lyapunov(filename_1, filename_2,N_calc):
    """This function calculates the lyapunov exponent of the integrations stores in filename_1 and filename_2
    Returns an array containing the value of the lyapunov exponent calcuated at each integration step."""
    data_1, mu_1, k_1=read_data.get_data(filename_1,'2')
    data_2, mu_2, k_2=read_data.get_data(filename_2,'2')
    lenght=len(data_1)
    try:
      assert lenght==len(data_2)
      assert mu_1==mu_2
      assert k_1==k_2
    except AssertionError:
        print(colors.red|"The integration results are not written as expexted", file=sys.stderr)
        sys.exit([6]) #Integration results are not written as expected
    difference=data_1-data_2
    norms=np.linalg.norm(difference, axis=1) #work on better names
    norm_0=norms[0]
    log_diff_ratio=np.log(norms/norm_0)
    lyaps=np.empty(lenght)
    cumulative_sum=0 ####
    print("Lyapunov exponents calculation:", N_calc, "/3")
    for i in Progress.range(1, lenght):
        cumulative_sum+=log_diff_ratio[i]
        lyaps[i]=cumulative_sum/i
    return lyaps


def get_results(simulation_ID, save_dir):
    """This function leads the calculation of the lyapunov exponents of all the simulations."""
    filename=[save_dir+'/'+simulation_ID+'_'+str(i)+'.csv' for i in range(4)]
    lyaps=[calculate_lyapunov(filename[0],filename[i], i) for i in range(1,4)]
    results=[]
    for lyap in lyaps:
        last_100lyap=lyap[-100:]
        mean_lyap=np.mean(last_100lyap)
        results.append(mean_lyap)
    return results, lyaps

def plot_exponents(simulation_ID, save_dir):
    """This function plots the lyapunov exponents series"""
    fig, subplots = plt.subplots(1, 3, figsize=(12, 4))
    values, series=get_results(simulation_ID, save_dir)
    for i in range(3):
        subplots[i].plot(series[i], color='r')
        subplots[i].set_xlabel("integration steps")
        subplots[i].set_ylabel("Lyapuniov exponent estimate")
        subplots[i].hlines(values[i], 0, len(series[i]), label=str(round(values[i],2)))
        subplots[i].legend()
    subplots[0].set_title('Direction x_1')
    subplots[1].set_title('DIrection x_2')
    subplots[2].set_title('Direction y_1')
    return fig, values

def lyapunov(save_dir):
   """This function leads all the process, calculating lyapunov exponents, creating the image and then saves it as 'simulation_ID_lyap_exp.png'
   The saves the estimated lyapunov exponents in 'simulation_ID_lyapunov_exp.dat' file."""
   simulation_ID=read_data.get_simulation_ID(save_dir)   
   fig, exp_values=plot_exponents(simulation_ID, save_dir)
   fig.savefig(save_dir+'/'+simulation_ID+"_lyap_exp.png", bbox_inches='tight')
   open_file=open(save_dir+'/'+simulation_ID+"_lyapunov_exp.dat",'w+')
   for exp in exp_values:
       open_file.write(str(exp)+' ')
   return True