#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:25:46 2020

@author: mani
"""
import numpy as np
from hypothesis import given, assume
import hypothesis.strategies as st
import warnings
import os
import sys
from subprocess import run
import integrator

class dynamo:
    """this class represents a single simulation
       states and parameters are stored"""
    
    def __init__ (self, mu, k, N_steps, initial_conditions):
        """setting parameters
        with precaution againts overflow errors"""
        if (abs(k)<10**-100 or abs(k)>10e+99):                 
            warnings.warn("value of k too big or too small, A will be set as nan")            
        elif (type(N_steps)!=int or N_steps<1):
            warnings.warn("N_steps must be a positive integer!")
        elif (np.nan in initial_conditions):
            warnings.warn("One or more initial condition in nan")
        elif (N_steps >10e+7):
            warnings.warn("N_steps too great can cause memory allocation errors")
        else:
            self.mu=mu
            self.k=k
            self.A=self.mu*(self.k**2-self.k**-2) 
        """creating arrays to store states and setting initial conditions"""
        self.N_steps=N_steps
        self.x1=np.empty(N_steps)   
        self.x2=np.empty(N_steps)
        self.y1=np.empty(N_steps)
        self.y2=np.empty(N_steps)
        
        self.initial_conditions=initial_conditions
        self.x1[0]=initial_conditions[0]
        self.x2[0]=initial_conditions[1]
        self.y1[0]=initial_conditions[2]
        self.y2[0]=self.y1[0]-self.A
        
  
        
    def evolve (self, outfile_name,dt):
        integrator.evolve(self.mu, self.k, self.N_steps, self.initial_conditions,outfile_name, dt)
        
        
def get_input_values():
    if (len(sys.argv)!=8):
        #raise error
        print('mh')
    else:
        mu=float(sys.argv[1])
        k=float(sys.argv[2])
        N_steps=int(sys.argv[3])
        initial_conditions=[float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])]
        filename=sys.argv[7]
    return mu, k, N_steps, initial_conditions, filename

def generate_data(save_dir, dt):      
   in_data=open(save_dir+"/input_values.txt", 'r')
   in_lines=in_data.readlines()
   N_sim=0
   for line in in_lines:
        values=line.split()
        mu=float(values[0])
        k=float(values[1])
        N_steps=int(values[2])
        initial_conditions=[float(val) for val in values[3:6]]
        simulation_ID=values[6]
        dyno=dynamo(mu, k, N_steps, initial_conditions)
        outfile_name=save_dir+'/'+simulation_ID+'_'+str(N_sim)+'.csv'
        dyno.evolve(outfile_name, dt)
        N_sim+=1
    	   
           
    	  
    
         
         
            
#######TESTS#######
@given(mu=st.floats(10e-100,1e+99), k=st.floats(10e-100, 10e+99))
def test_parameters (mu, k):
    A_test=mu*(k**2-k**-2)
    dynamo_test=dynamo(mu, k, 10, [1, 1, 1])
    assert dynamo_test.A==A_test
    
@given(x2_init=st.floats(), x1_init=st.floats(), y1_init=st.floats(), N_steps=st.integers(1,10e+7))
def test_initial_conditions (x1_init, x2_init, y1_init, N_steps):
    assume (not np.isnan(x1_init ))
    assume (not np.isnan(x2_init ))
    assume (not np.isnan(y1_init ))
    dynamo_test= dynamo(1,1, N_steps, [x1_init, x2_init, y1_init])
    assert len(dynamo_test.x1)==N_steps
    assert len(dynamo_test.x1)==len(dynamo_test.x2)
    assert len(dynamo_test.x2)==len(dynamo_test.y1)
    assert len(dynamo_test.y1)==len(dynamo_test.y2)
    assert dynamo_test.x1[0]==x1_init
    assert dynamo_test.x2[0]==x2_init
    assert dynamo_test.y1[0]==y1_init
    assert dynamo_test.y2[0]==y1_init #because mu=1, k=1 -> A=mu*(k**2-k**-2)=0, and y2=y1-A
    
    
    

    
