#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:52:18 2020

@author: mani
"""
import numpy as np
from plumbum import cli
import sys
import plumbum.cli.terminal as terminal



def read_input():
    in_file=open("temp_for_create_infiles.txt")
    in_string=in_file.readlines()
    assert len(in_string)==1
    in_string=in_string[0]
    split_string=in_string.split()
    assert len(split_string)==7
    return split_string

def ask_for_data():
    in_data=terminal.prompt("Type the data in the form 'mu k N_steps x1_0 x2_0 y1_0 simulation_identifier")
    outfile=open("temp_for_create_infiles.txt",'w+')
    outfile.write(in_data)
    outfile.close()
    
def main():
    ask_for_data()
    in_data=read_input()
    mu=in_data[0]
    k=in_data[1]
    N_steps=in_data[2]
    initial_condition=[float(X) for X in in_data[3:6]]
    initial_condition1=[cond for cond in initial_condition]
    initial_condition1[0]+=2**-4
    initial_condition2=[cond for cond in initial_condition]
    initial_condition2[1]+=2**-4
    initial_condition3=[cond for cond in initial_condition]
    initial_condition3[2]+=2**-4
    initial_conditions=[initial_condition, initial_condition1,initial_condition2,initial_condition3]
    identifier=in_data[6]
    outfile=open("input_values.txt",'w+')
    for condition in initial_conditions:
        outstring=str(mu)+' '+str(k)+' '+str(N_steps)+' '+str(condition[0])+' '+str(condition[1])+' '+str(condition[2])+' '+identifier+'\n'
        outfile.write(outstring)
    
        
    
    
main()