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

class dynamo:
    """this class represents a single simulation.
       states and parameters are stored in internal variables."""
    
    def __init__(self, mu, k, initial_conditions, dt, simtype):
        """Initializer of dynamo class.
        PARAMETERS:
            mu                : (float) the mu parameter of rikitake dynamo equations
            k                 : (float) the k parameter of rikitake dynamo equations
            N_steps           : (int) Number of integration steps that the user wants to perform
            initial_conditions: (float[3]) array storing the initial states of the system, in the order [x_1, x_2, y_1]
            simtype           : {'perturbed'', ''unperturbed'}
            dt                : (float) size of the discretized time step."""
        self.mu=mu
        self.k=k
        self.A=self.mu*(self.k**2-self.k**-2) 
        """creating arrays to store states and setting initial conditions"""
        self.time=np.empty(self.N_steps)
        self.x1_0=initial_conditions[0]
        self.x2_0=initial_conditions[1]
        self.y1_0=initial_conditions[2]
        self.time[0]=0
        self.dt=dt
        self.simtype=simtype
    
    def evolve (self, N_steps):
        x1=np.empty(N_steps)
        x1[0]=self.x1_0
        x2=np.empty(N_steps)
        x2[0]=self.x2_0
        y1=np.empty(N_steps)
        y1[0]=self.y1_0
        y2=np.empty(N_steps)
        time=np.empty(N_steps)
        time[0]=0
        """This function performs the evolution of the states."""
        if self.simtype=="unperturbed":
            print("Integration 1/2 (unperturbed initial conditions)")
        if self.simtype=="perturbed":
            print("Integration 2/2 (perturbed initial conditions)")
        for i in Progress.range(1,N_steps):
            x1[i]=self.__Evo_x1(i-1)
            x2[i]=self.__Evo_x2(i-1)
            y1[i]=self.__Evo_y1(i-1)
            time[i]=i*self.dt
        y2=y1-self.A
        
    #TODO MAKE SOPRA E SOTTO COHERENT
    """The following functions perform a single step of the 4th order Runge-Kutta integration for each variable."""
    def __Evo_x1(self,i):
        return (self.x1[i]+self.dt*(self.__k1x1(i)+2*self.__k2x1(i)+2*self.__k3x1(i)+self.__k4x1(i))/6)
    def __Evo_x2(self,i):
        return (self.x2[i]+self.dt*(self.__k1x2(i)+2*self.__k2x2(i)+2*self.__k3x2(i)+self.__k4x2(i))/6)
    def __Evo_y1(self, i):
        return (self.y1[i]+self.dt*(self.__k1y1(i)+2*self.__k2y1(i)+2*self.__k3y1(i)+self.__k4y1(i))/6)
    
    """The following functions calculate the 4th order RK factors"""
    def __k1x1 (self, i):
        return (-self.mu*self.x1[i]+self.y1[i]*self.x2[i])
    def __k1x2 (self,i):
        return (-self.mu*self.x2[i]+(self.y1[i]-self.A)*self.x1[i])
    def __k1y1 (self,i):
        return(1-self.x1[i]*self.x2[i])
        
    def __k2x1 (self, i):
        return (-self.mu*(self.x1[i]+0.5*self.dt*self.__k1x1(i))+(self.y1[i]+0.5*self.dt*self.__k1y1(i))*(self.x2[i]+0.5*self.dt*self.__k1x2(i)))
    def __k2x2 (self,i):
        return (-self.mu*(self.x2[i]+0.5*self.dt*self.__k1x2(i))+((self.y1[i]+0.5*self.dt*self.__k1y1(i)-self.A)*(self.x1[i]+0.5*self.dt*self.__k1x1(i))))
    def __k2y1 (self,i):
        return(1.-(self.x1[i]+0.5*self.dt*self.__k1x1(i))*(self.x2[i]+0.5*self.dt*self.__k1x2(i)))
        
    def __k3x1 (self, i):
        return (-self.mu*(self.x1[i]+0.5*self.dt*self.__k2x1(i))+(self.y1[i]+0.5*self.dt*self.__k2y1(i))*(self.x2[i]+0.5*self.dt*self.__k2x2(i)))
    def __k3x2 (self,i):
        return (-self.mu*(self.x2[i]+0.5*self.dt*self.__k2x2(i))+((self.y1[i]+0.5*self.dt*self.__k2y1(i)-self.A)*(self.x1[i]+0.5*self.dt*self.__k2x1(i))))
    def __k3y1 (self,i):
        return(1.-(self.x1[i]+0.5*self.dt*self.__k2x1(i))*(self.x2[i]+0.5*self.dt*self.__k2x2(i)))
        
    def __k4x1 (self, i):
        return (-self.mu*(self.x1[i]+self.dt*self.__k3x1(i))+(self.y1[i]+self.dt*self.__k3y1(i))*(self.x2[i]+self.dt*self.__k3x2(i)))
    def __k4x2 (self,i):
        return (-self.mu*(self.x2[i]+self.dt*self.__k3x2(i))+((self.y1[i]+self.dt*self.__k3y1(i)-self.A)*(self.x1[i]+self.dt*self.__k3x1(i))))
    def __k4y1 (self,i):
        return(1.-(self.x1[i]+self.dt*self.__k3x1(i))*(self.x2[i]+self.dt*self.__k3x2(i)))
       
        
    def write_results(self, save_dir, simulation_ID):
        """This function saves the integration results in outfile_name file."""
        if self.simtype=="unperturbed":
            simlabel=0
        elif self.simtype=="perturbed":
            simlabel=1
        outfile_name=save_dir+'/'+self.simulation_ID+'_'+str(simlabel)+'.csv'
        outfile=open(outfile_name, 'w+')
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
   for line in in_lines:
        """Each line represents a set of integration parameters.
        First line represents the unperturbed solution
        Second line represents the perturbed solution"""
        if line==in_lines[0]:
            simtype="unperturbed"
        else:
            simtype="perturbed"
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
        
        """actual integration"""
        dyno=dynamo(mu, k, initial_conditions, dt, simtype)
        dyno.evolve(N_steps)
        
        """writing the results"""
        dyno.write_results(save_dir, simulation_ID)
        
   return True
    	   

    	   
