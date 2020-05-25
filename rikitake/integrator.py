#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:24:22 2020

@author: mani
"""
import numpy as np

#we take in input: mu, k, Nsteps, initial conditions, simID
class dynamo:
    def __init__(self, mu, k, N_steps, initial_conditions, outfile_name, dt):
        self.mu=mu
        self.k=k
        self.A=mu*(k**2-k**-2)
        self.N_steps=N_steps
        self.x1=np.empty(self.N_steps)
        self.x2=np.empty(self.N_steps)
        self.y1=np.empty(self.N_steps)
        self.x1[0]=initial_conditions[0]
        self.x2[0]=initial_conditions[1]
        self.y1[0]=initial_conditions[2]
        self.outfile_name=outfile_name
        self.dt=dt
    
    def evolve (self):
        for i in range (1, self.N_steps):
            self.x1[i]=self.Evo_x1(i-1)
            self.x2[i]=self.Evo_x2(i-1)
            self.y1[i]=self.Evo_y1(i-1)
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
        
        
    

def evolve (mu, k, N_steps, initial_conditions, outfile_name, dt):
    dyno=dynamo(mu,k,N_steps, initial_conditions, outfile_name, dt)
    dyno.evolve()
    dyno.write_results()
