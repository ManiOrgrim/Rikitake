#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:00:07 2020

@author: mani
"""
import matplotlib.pylab as plt
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import read_data
from plumbum.cli.terminal import Progress


def generate_image(filename):
    """ this function creates the (x2,y1) plot, saving it in save_dir directory as 'filename.png'"""
    
    t, x1, x2, y1, y2, mu, k=read_data.get_data(filename, '1')
    
    """ 
    trajectory x2,y1 projection
    """
    fig, ax=plt.subplots(figsize=(10,10))
    ax.plot(x2,y1, linewidth=0.5)
    image_title='Rikitake dynamo phase space with mu ='+str(mu)+' k='+str(k)
    fig.suptitle(image_title,fontsize=20)
    plt.xlabel('x2', fontsize=18)
    plt.ylabel('y1', fontsize=18)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'_X2Y1.png' #FIXME when simulationID has '.' char
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
    
    """ 
    trajectory x1,y1 projection
    """
    fig, ax=plt.subplots(figsize=(10,10))
    ax.plot(x1,y1,linewidth=0.5)
    image_title='Rikitake dynamo phase space with mu ='+str(mu)+' k='+str(k)
    plt.suptitle(image_title,fontsize=20)
    plt.xlabel('x1', fontsize=18)
    plt.ylabel('y1', fontsize=18)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'_X1Y1.png' #FIXME when simulationID has '.' char
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
    """ 
    trajectory x1,x2 projection
    """
    
    plt.figure(figsize=(10,10))
    plt.plot(x1,x2,linewidth=0.5)
    image_title='Rikitake dynamo phase space with mu ='+str(mu)+' k='+str(k)
    plt.suptitle(image_title,fontsize=20)
    plt.xlabel('x1', fontsize=18)
    plt.ylabel('x2', fontsize=18)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'_X1X2.png' #FIXME when simulationID has '.' char
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
    """ 
    trajectory in 3D x1, x2, y1 space
    """
    
    fig=plt.figure()
    ax=fig.add_subplot(111, projection='3d')
    ax.plot(x1,x2,y1,linewidth=0.5)
    ax.set_title('3D phase space')
    ax.set_xlabel('x1', fontsize=12)
    ax.set_ylabel('x2', fontsize=12)
    ax.set_zlabel('y1', fontsize=12)
    image_filename=filename[:dot_position]+'_3Dplot.png' #FIXME when simulationID has '.' char    
    fig.savefig(image_filename,bbox_inches='tight')
    
    """ 
    x1 vs time plot
    """    
    
    plt.figure(figsize=(10,10))
    plt.plot(t,x1,linewidth=0.5)
    image_title='Rikitake dynamo phase space with mu ='+str(mu)+' k='+str(k)
    plt.suptitle(image_title,fontsize=20)
    plt.xlabel('tau', fontsize=18)
    plt.ylabel('X1', fontsize=18)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'_X1time.png' #FIXME when simulationID has '.' char
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
     """ 
    x2 vs time plot
    """    
    
    
    plt.figure(figsize=(10,10))
    plt.plot(t,x2,linewidth=0.5)
    image_title='Rikitake dynamo phase space with mu ='+str(mu)+' k='+str(k)
    plt.suptitle(image_title,fontsize=20)
    plt.xlabel('tau', fontsize=18)
    plt.ylabel('X2', fontsize=18)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'_X2time.png' #FIXME when simulationID has '.' char
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
    
    
def image_creator(save_dir):
   """This function generates the two 'path/to/data.csv' strings 
   to where data will be read.
   Each one is created by the function 'generate_image'.
   RETURNS:
       TRUE if the process finished without errors."""
   simulation_ID=read_data.get_simulation_ID(save_dir)  
   print("Image generation")
   files=[save_dir+'/'+simulation_ID+'_'+str(i)+'.csv' for i in range(2)]
   for file in Progress(files):
       generate_image(file)
   return True

