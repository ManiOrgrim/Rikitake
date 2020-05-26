#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:25:46 2020

@author: mani
"""
import numpy as np
import warnings
import sys
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
    	   
           
    	  
    

