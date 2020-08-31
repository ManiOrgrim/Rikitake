#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:00:07 2020

@author: mani
"""
import matplotlib.pylab as plt
import read_data
from plumbum.cli.terminal import Progress


def generate_image(filename):
    """ this function creates the (x2,y1) plot, saving it in save_dir directory as 'filename.png'"""
    plt.figure(figsize=(10,10))
    t, x1, x2, y1, y2, mu, k=read_data.get_data(filename, '1')
    plt.plot(x2,y1)
    image_title='Rikitake dynamo phase space with mu ='+str(mu)+' k='+str(k)
    plt.suptitle(image_title,fontsize=20)
    plt.xlabel('x2', fontsize=18)
    plt.ylabel('y1', fontsize=18)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'.png' #BUG when simulationID has '.' char
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
def image_creator(save_dir):
   """This function generates the four 'path/to/image.png' string to where images will be saved.
   Each one is created by the function 'generate_image'.
   RETURNS:
       TRUE if the process finished without errors."""
   simulation_ID=read_data.get_simulation_ID(save_dir)  
   print("Image generation")
   files=[save_dir+'/'+simulation_ID+'_'+str(i)+'.csv' for i in range(4)]
   for file in Progress(files):
       generate_image(file)
   return True

