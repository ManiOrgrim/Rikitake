#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:24:22 2020

@author: mani
"""
import numpy as np
import sys
from plumbum.cli.terminal import Progress
from plumbum import colors


#we take in input: mu, k, Nsteps, initial conditions, simID
class dynamo:
    """this class represents a single simulation.
       states and parameters are stored in internal variables."""
    
    def __init__(self, mu, k, N_steps, initial_conditions, outfile_name, dt):
        """Initializer of dynamo class.
        PARAMETERS:
            mu                : (float) the mu parameter of rikitake dynamo equations
            k                 : (float) the k parameter of rikitake dynamo equations
            N_steps           : (int) Number of integration steps that the user wants to perform
            initial_conditions: (float[3]) array storing the initial states of the system, in the order [x_1, x_2, y_1]
            outfile_name      : (str) name of the file in wich the result of the integration will be stored
            dt                : (float) size of the discretized time step."""
        self.mu=mu
        self.k=k
        self.A=self.mu*(self.k**2-self.k**-2) 
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
    
    def evolve (self, N_sim):
        """This function performs the evolution of the states.
        PARAMETERS:
            N_sim: (int) ranging from 0 to 3, it is the identifier of the simulation."""
        print("Integration ", N_sim+1, "/2")
        for i in Progress.range(1,self.N_steps):
            self.x1[i]=self.Evo_x1(i-1)
            self.x2[i]=self.Evo_x2(i-1)
            self.y1[i]=self.Evo_y1(i-1)
            self.time[i]=i*self.dt
        self.y2=self.y1-self.A
    """The following functions perform a single step of the 4th order Runge-Kutta integration for each variable."""
    def Evo_x1(self,i):
        return (self.x1[i]+self.dt*(self.k1x1(i)+2*self.k2x1(i)+2*self.k3x1(i)+self.k4x1(i))/6)
    def Evo_x2(self,i):
        return (self.x2[i]+self.dt*(self.k1x2(i)+2*self.k2x2(i)+2*self.k3x2(i)+self.k4x2(i))/6)
    def Evo_y1(self, i):
        return (self.y1[i]+self.dt*(self.k1y1(i)+2*self.k2y1(i)+2*self.k3y1(i)+self.k4y1(i))/6)
    
    """The following functions calculate the 4th order RK factors"""
    def k1x1 (self, i):
        return (-self.mu*self.x1[i]+self.y1[i]*self.x2[i])
    def k1x2 (self,i):
        return (-self.mu*self.x2[i]+(self.y1[i]-self.A)*self.x1[i])
    def k1y1 (self,i):
        return(1-self.x1[i]*self.x2[i])
        
    def k2x1 (self, i):
        return (-self.mu*(self.x1[i]+0.5*self.dt*self.k1x1(i))+(self.y1[i]+0.5*self.dt*self.k1y1(i))*(self.x2[i]+0.5*self.dt*self.k1x2(i)))
    def k2x2 (self,i):
        return (-self.mu*(self.x2[i]+0.5*self.dt*self.k1x2(i))+((self.y1[i]+0.5*self.dt*self.k1y1(i)-self.A)*(self.x1[i]+0.5*self.dt*self.k1x1(i))))
    def k2y1 (self,i):
        return(1.-(self.x1[i]+0.5*self.dt*self.k1x1(i))*(self.x2[i]+0.5*self.dt*self.k1x2(i)))
        
    def k3x1 (self, i):
        return (-self.mu*(self.x1[i]+0.5*self.dt*self.k2x1(i))+(self.y1[i]+0.5*self.dt*self.k2y1(i))*(self.x2[i]+0.5*self.dt*self.k2x2(i)))
    def k3x2 (self,i):
        return (-self.mu*(self.x2[i]+0.5*self.dt*self.k2x2(i))+((self.y1[i]+0.5*self.dt*self.k2y1(i)-self.A)*(self.x1[i]+0.5*self.dt*self.k2x1(i))))
    def k3y1 (self,i):
        return(1.-(self.x1[i]+0.5*self.dt*self.k2x1(i))*(self.x2[i]+0.5*self.dt*self.k2x2(i)))
        
    def k4x1 (self, i):
        return (-self.mu*(self.x1[i]+self.dt*self.k3x1(i))+(self.y1[i]+self.dt*self.k3y1(i))*(self.x2[i]+self.dt*self.k3x2(i)))
    def k4x2 (self,i):
        return (-self.mu*(self.x2[i]+self.dt*self.k3x2(i))+((self.y1[i]+self.dt*self.k3y1(i)-self.A)*(self.x1[i]+self.dt*self.k3x1(i))))
    def k4y1 (self,i):
        return(1.-(self.x1[i]+self.dt*self.k3x1(i))*(self.x2[i]+self.dt*self.k3x2(i)))
       
        
    def write_results(self):
        """This function saves the integration results in outfile_name file."""
        file_name= self.outfile_name
        outfile=open(file_name, 'w+')
        line1="mu= "+str(self.mu)+"\tk= "+str(self.k)+"\n"
        outfile.write(line1)
        line2= "Time\tx_1\tx_2\ty_1\ty_2\n"
        outfile.write(line2)
        for i in range(self.N_steps):
            line=str(self.dt*i)+';'+str(self.x1[i])+';'+str(self.x2[i])+';'+str(self.y1[i])+';'+str(self.y2[i])+'\n'
            outfile.write(line)
        outfile.close()
        
        

def generate_data(save_dir, dt):  
   """This function leads the integration process and writes the data.
   RETURNS:
       TRUE:  if the process ended without errors"""
   
   """reading all the needed parameters"""
   try:
       in_data=open(save_dir+"/input_values.txt",'r')
   except OSError:
        print(colors.red|"Could not open input_values.txt file")
        sys.exit([2]) #could not open input_values.txt    
   in_lines=in_data.readlines()
   N_sim=0
   for line in in_lines:
        """Each line represents a set of integration parameters"""
        values=line.split()
        try:
           mu=float(values[0])
           k=float(values[1])
           N_steps=int(values[2])
           initial_conditions=[float(value) for value in values[3:6]]
           simulation_ID=values[6]
        except ValueError or IndexError:
           print(colors.red|"'input_values.txt' is not written as expected.")
           sys.exit([5]) #Error in 'input_values.txt
        outfile_name=save_dir+'/'+simulation_ID+'_'+str(N_sim)+'.csv'
        
        """actual integration"""
        dyno=dynamo(mu, k, N_steps, initial_conditions, outfile_name, dt)
        dyno.evolve(N_sim)
        
        """writing the results"""
        dyno.write_results()
        
        N_sim+=1
   return True
    	   

    	   
