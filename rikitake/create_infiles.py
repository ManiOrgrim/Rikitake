#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:52:18 2020

@author: mani
"""

import plumbum.cli.terminal as terminal
import sys
import os
import warnings
from plumbum import colors

def read_input():
    """This function reads the temporary file '.temp_for_create_infiles.txt';
    Reading the values of the parameters, the number of integration steps to  perform,
    the initial conditions and the simulation_ID"""
    try:
       in_file=open(".temp_for_create_infiles.txt",'r')
    except OSError:
        print(colors.red|"Could not open '.temp_for_create_infiles.txt'. Maybe the file has been deleted?", file=sys.stderr)
        sys.exit([3]) #could not find .temp_for_create_infiles.txt
    in_string=in_file.readlines()
    try:
      assert len(in_string)==1
      in_string=in_string[0]
      split_string=in_string.split()
      assert len(split_string)==7
    except AssertionError:
        print(colors.red|"'.temp_for_create_infile.txt' file is not written as expected. Maybe writing process went wrong or the file has been modified.")
        sys.exit([4]) #.temp_for_create_infile not as expected.
    return split_string

def ask_for_data():
    """This function asks the user the values of parameters, number of integration steps,
    initial conditions and simulation_ID. Then creates a '.temp_for_create_infiles.txt' file to store them."""
    while (True):
       in_data=terminal.prompt("Type the data in the form 'mu k N_steps x1_0 x2_0 y1_0 simulation_identifier")
       split_values=in_data.split()
       if (len(split_values)!=7):
           print(colors.yellow|"You did not give 7 values. Try again.")
           continue
       try:
          mu=float(in_data.split()[0])
          k=float(in_data.split()[1])
          N_steps=int(in_data.split()[2])
          if (N_steps<20000):
              warnings.warn(colors.yellow|"The number of integration steps may be too small. Convergence of Lyapunov exponents is not granted.")
          x1_0=float(in_data.split()[3])
          x2_0=float(in_data.split()[4])
          y1_0=float(in_data.split()[5])
       except ValueError:
          print(colors.yellow|"Some of the parameter values you gave are not numbers. Please try again.")
          continue
       if (0<mu<10**2 and 1e-2<k<1e+2):
           break
       else:
           go_on=terminal.ask(colors.yellow|"""The values of mu or k you choose may cause overflow issues.
                        It is reccommended that 0< mu< 10^2 and 10^-2< k < 10^2.
                        Continue anyway?""")
           if (go_on):
               break         
    
    outfile=open(".temp_for_create_infiles.txt",'w+')
    outfile.write(in_data)
    outfile.close()
    
def create_infile(save_dir):
    """This function reads the needed values from '.temp_for_create_infiles.txt' file,
    then creates a 'simulation_ID.txt' file in wich the necessary values for the integration are stored.
    Each line of this file is in the form 'mu k N_steps initial conditions simulation_ID'.
    The first line shows the values as given in input
    In the following three the initial conditions are slightly changed in order to calcuate lyapunov exponentes."""
    ask_for_data()
    in_data=read_input()
    mu=in_data[0]
    k=in_data[1]
    N_steps=in_data[2]
    """Creation of slightly different initial conditions."""
    initial_condition=[float(X) for X in in_data[3:6]]
    initial_condition1=[cond for cond in initial_condition]
    initial_condition1[0]+=2**-5
    initial_condition2=[cond for cond in initial_condition]
    initial_condition2[1]+=2**-5
    initial_condition3=[cond for cond in initial_condition]
    initial_condition3[2]+=2**-5
    initial_conditions=[initial_condition, initial_condition1,initial_condition2,initial_condition3]
    identifier=in_data[6]
    outfile=open(save_dir+"/input_values.txt",'w+')
    for condition in initial_conditions:
        outstring=str(mu)+' '+str(k)+' '+str(N_steps)+' '+str(condition[0])+' '+str(condition[1])+' '+str(condition[2])+' '+identifier+'\n'
        outfile.write(outstring)
    try:
        os.remove(".temp_for_create_infiles.txt")
    except FileNotFoundError:
        print(colors.red|"Could not remove '.temp_for_create_infiles.txt'. Maybe the file has been deleted alright or you don't have permissions. The process will go on")
    

