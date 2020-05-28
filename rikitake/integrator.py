#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:24:22 2020

@author: mani
"""
import numpy as np
import warnings
import sys

#we take in input: mu, k, Nsteps, initial conditions, simID
class dynamo:
    """this class represents a single simulation
       states and parameters are stored"""
    
    def __init__(self, mu, k, N_steps, initial_conditions, outfile_name, dt):
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
        #TODO mettere una gestione per gli input male
        self.N_steps=N_steps
        """creating arrays to store states and setting initial conditions"""
        self.x1=np.empty(self.N_steps)
        self.x2=np.empty(self.N_steps)
        self.y1=np.empty(self.N_steps)
        self.y2=np.empty(self.N_steps)
        self.time=np.empty(self.N_steps)
        self.x1[0]=initial_conditions[0]
        self.x2[0]=initial_conditions[1]
        self.y1[0]=initial_conditions[2]
        self.time[0]=0
        self.outfile_name=outfile_name
        self.dt=dt
    
    def evolve (self):
        for i in range (1, self.N_steps):
            self.x1[i]=self.Evo_x1(i-1)
            self.x2[i]=self.Evo_x2(i-1)
            self.y1[i]=self.Evo_y1(i-1)
            self.time[i]=i*self.dt
        self.y2=self.y1-self.A
        
    def Evo_x1(self,i):
        return (self.x1[i]+self.dt*(self.k1x1(i)+self.k2x1(i)+self.k3x1(i)+self.k4x1(i)+self.k5x1(i)+self.k6x1(i))/6)
    def Evo_x2(self,i):
        return (self.x2[i]+self.dt*(self.k1x2(i)+self.k2x2(i)+self.k3x2(i)+self.k4x2(i)+self.k5x2(i)+self.k6x2(i))/6)
    def Evo_y1(self, i):
        return (self.y1[i]+self.dt*(self.k1y1(i)+self.k2y1(i)+self.k3y1(i)+self.k4y1(i)+self.k5y1(i)+self.k6y1(i))/6)
    
    def k1x1 (self, i):
        return (-self.mu*self.x1[i]+self.y1[i]*self.x2[i])
    def k1x2 (self,i):
        return (-self.mu*self.x2[i]+(self.y1[i]-self.A)*self.x1[i])
    def k1y1 (self,i):
        return(1-self.x1[i]*self.x2[i])
        
    def k2x1 (self, i):
        return (-self.mu*(self.x1[i]+self.dt*self.k1x1(i)/6.)+(self.y1[i]+self.dt*self.k1y1(i)/6)*(self.x2[i]+self.dt*self.k1x2(i)/6.))
    def k2x2 (self,i):
        return (-self.mu*(self.x2[i]+self.dt*self.k1x2(i)/6.)+((self.y1[i]+self.dt*self.k1y1(i)/6-self.A)*(self.x1[i]+self.dt*self.k1x1(i)/6.)))
    def k2y1 (self,i):
        return(1.-(self.x1[i]+self.dt*self.k1x1(i)/6.)*(self.x2[i]+self.dt*self.k1x2(i)/6.))
        
    def k3x1 (self, i):
        return (-self.mu*(self.x1[i]+self.dt*self.k2x1(i)/3.)+(self.y1[i]+self.dt*self.k2y1(i)/3)*(self.x2[i]+self.dt*self.k2x2(i)/3.))
    def k3x2 (self,i):
        return (-self.mu*(self.x2[i]+self.dt*self.k2x2(i)/3.)+((self.y1[i]+self.dt*self.k2y1(i)/3-self.A)*(self.x1[i]+self.dt*self.k2x1(i)/3.)))
    def k3y1 (self,i):
        return(1.-(self.x1[i]+self.dt*self.k2x1(i)/3.)*(self.x2[i]+self.dt*self.k2x2(i)/3.))
        
    def k4x1 (self, i):
        return (-self.mu*(self.x1[i]+0.5*self.dt*self.k3x1(i))+(self.y1[i]+0.5*self.dt*self.k3y1(i))*(self.x2[i]+0.5*self.dt*self.k3x2(i)))
    def k4x2 (self,i):
        return (-self.mu*(self.x2[i]+0.5*self.dt*self.k3x2(i))+((self.y1[i]+0.5*self.dt*self.k3y1(i)-self.A)*(self.x1[i]+0.5*self.dt*self.k3x1(i))))
    def k4y1 (self,i):
        return(1.-(self.x1[i]+0.5*self.dt*self.k3x1(i))*(self.x2[i]+0.5*self.dt*self.k3x2(i)))

    def k5x1 (self, i):
        return (-self.mu*(self.x1[i]+2*self.dt*self.k4x1(i)/3)+(self.y1[i]+2*self.dt*self.k4y1(i)/3)*(self.x2[i]+2*self.dt*self.k4x2(i)/3))
    def k5x2 (self,i):
        return (-self.mu*(self.x2[i]+2*self.dt*self.k4x2(i)/3)+((self.y1[i]+2*self.dt*self.k4y1(i)/3-self.A)*(self.x1[i]+2*self.dt*self.k4x1(i)/3)))
    def k5y1 (self,i):
        return(1.-(self.x1[i]+2*self.dt*self.k4x1(i))*(self.x2[i]+2*self.dt*self.k4x2(i)/3))
        
    def k6x1 (self, i):
        return (-self.mu*(self.x1[i]+5*self.dt*self.k5x1(i)/6.)+(self.y1[i]+5*self.dt*self.k5y1(i)/6)*(self.x2[i]+5*self.dt*self.k5x2(i)/6.))
    def k6x2 (self,i):
        return (-self.mu*(self.x2[i]+5*self.dt*self.k5x2(i)/6.)+((self.y1[i]+5*self.dt*self.k5y1(i)/6-self.A)*(self.x1[i]+5*self.dt*self.k5x1(i)/6.)))
    def k6y1 (self,i):
        return(1.-(self.x1[i]+5*self.dt*self.k5x1(i)/6.)*(self.x2[i]+5*self.dt*self.k5x2(i)/6.))
       
        
    def write_results(self):
        file_name= self.outfile_name
        outfile=open(file_name, 'w+')
        line1="mu= "+str(self.mu)+"\tk= "+str(self.k)+"\n"
        outfile.write(line1)
        line2= "Time\tx_1\tx_2\ty_1\ty_2\n"
        outfile.write(line2)
        for i in range(self.N_steps):
            line=str(self.dt*i)+';'+str(self.x1[i])+';'+str(self.x2[i])+';'+str(self.y1[i])+';'+str(self.y2[i])+'\n'
            outfile.write(line)
        
        
    
def generate_data(save_dir, dt):  
   try:
       in_data=open(save_dir+"/input_values.txt",'r')
   except OSError:
        print("Could not find input_values.txt file")
        sys.exit([2]) #could not find input_values.txt    
   in_lines=in_data.readlines()
   N_sim=0
   for line in in_lines:
        values=line.split()
        mu=float(values[0])
        k=float(values[1])
        N_steps=int(values[2])
        initial_conditions=[float(val) for val in values[3:6]]
        simulation_ID=values[6]
        outfile_name=save_dir+'/'+simulation_ID+'_'+str(N_sim)+'.csv'
        dyno=dynamo(mu, k, N_steps, initial_conditions, outfile_name, dt)
        dyno.evolve()
        dyno.write_results()
        N_sim+=1
   return True
    	   
