##!/usr/bin/env python3
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



def calculate_lyapunov(filename_1, filename_2,N_calc):  #TODO: remove references to N_calc
    """This function calculates the lyapunov exponent at each integration step between two solutions.
    PARAMETERS:
        filename_1: (string) String object with the file name in wich solution1 is stored
        filename_2: (string) String object with the file name in wich solution2 is stored
        N_calc    : (int) between 1 and 3. Identifies the direction of the actual calculation.
    RETURNS:
        lyaps     : (float[N_steps]) N_steps-dimension array-like containing the values of the lyapunov exponent calcuated between solution1 and solution2 at each integration step for."""
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
    """ Actual calculation of the Lyapunov exponents"""
    
    """Difference between the two simulations"""
    difference=data_1-data_2                        
    """Norms of the difference vectors"""
    norms=np.linalg.norm(difference, axis=1)
    """Norm of the initial difference"""
    norm_0=norms[0]  
    """Calculating the ln of the ratio between evolved state and initial state"""                               
    log_diff_ratio=np.ln(norms/norm_0)
    lyaps=np.empty(lenght)
    cumulative_sum=0 ####
    
    print("Lyapunov exponents calculation:", N_calc, "/1")
    for i in Progress.range(1, lenght):
        """calculating the mean of the ratios from initial state to state i"""
        cumulative_sum+=log_diff_ratio[i]
        lyaps[i]=cumulative_sum/i
        
    return lyaps        




def get_results(simulation_ID, save_dir):
    """This function leads the calculation of the lyapunov exponents of all the simulations.
    PARAMETERS:
        simulation_ID: (string) String with the simulation_ID.
        save_dir     : (string) path/to/dir in which previously calculated results are stored.
    RETURNS:
        mean_lyap     : (float) array-like containing values of lyapunov exponents beetween the unperturbed series and the perturbed one. 
                        It is calcuted taking the mean value of the last 100 lyapunov exponents.
        lyaps        : (float[N_steps]) array-like containing the series of lyapunov exponent calculated for each timestep. """
    filename=[save_dir+'/'+simulation_ID+'_'+str(i)+'.csv' for i in range(2)]
    lyaps=calculate_lyapunov(filename[0],filename[1], 1)
    """Calculating the mean of the last 100 lyapunov exponents 
    This is an indication of the actual exponent value"""
    last_100lyap=lyaps[-100:]
    mean_lyap=np.mean(last_100lyap)
    return mean_lyap, lyaps

def plot_exponents(simulation_ID, save_dir):
    """This function plots the lyapunov exponents series. 
    PARAMETERS:
        simulation_ID: (string) String representing the simulation_ID.
        save_dir     : (string) path/to/dir in which previously calculated results are stored.
    RETURNS:
            fig      : (figure object) Figure showing a plot of lyapunov exponents evolution fo
            values   : (float) array-like containing values of lyapunov exponents beetween the unperturbed series and the perturbed ones."""
    fig, subplot = plt.subplots(1, 1, figsize=(4, 4))
    mean_lyap, series=get_results(simulation_ID, save_dir)
    
    subplot.plot(series, color='r')
    subplot.set_xlabel("integration steps")
    subplot.set_ylabel("Lyapuniov exponent estimate")
    subplot.hlines(mean_lyap, 0, len(series), label=str(round(mean_lyap,2)), linestyle='dashed')
    subplot.legend()
    subplot.set_title('Greatest Lyapunov exponent')
    return fig, mean_lyap



def lyapunov(save_dir):
   """This function leads all the process, 
   calculating lyapunov exponent, creating the image and 
   then saves it as 'simulation_ID_lyap_exp.png'
   Then saves the estimated lyapunov exponents in 
   '<simulation_ID>_lyapunov_exp.dat' file.
   PARAMETERS:
       save_dir   : (string) path/to/dir in which previously calculated results are stored. Results of this process will be saved here.
   RETURNS:
       TRUE       : if all the process ended without issues."""
   
   simulation_ID=read_data.get_simulation_ID(save_dir)   
   fig, mean_lyap=plot_exponents(simulation_ID, save_dir)
   fig.savefig(save_dir+'/'+simulation_ID+"_lyap_exp.png", bbox_inches='tight')
   open_file=open(simulation_ID+'lyap.dat','w+')
   open_file.write(str(mean_lyap)+' ')
   return True
