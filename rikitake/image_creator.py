#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:00:07 2020

@author: mani
"""
import matplotlib.pylab as plt
import read_data

    
    

def generate_image(filename):
    """ this function creates the (x2,y1) plot saving it in working directory as 'filename.png'"""
    plt.figure(figsize=(10,10))
    t, x1, x2, y1, y2, mu, k=read_data.get_data(filename, '1')
    plt.plot(x2,y1)
    title_text='Rikitake dynamo phase space with mu ='+str(mu)+' k='+str(k)
    plt.suptitle(title_text,fontsize=20)
    plt.xlabel('x2', fontsize=18)
    plt.ylabel('y1', fontsize=18)
    dot_position=filename.index('.')
    image_filename=filename[:dot_position]+'.png'
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()
    
def generate_images(save_dir):
   simulation_ID=read_data.get_simulation_ID(save_dir)    
   files=[save_dir+'/'+simulation_ID+'_'+str(i)+'.csv' for i in range(4)]

   for file in files:
       generate_image(file)
