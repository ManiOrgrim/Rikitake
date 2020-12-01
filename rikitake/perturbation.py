#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 09:20:14 2020

@author: mani
"""
import numpy as np
import scipy.linalg as la


def jacobian (starting_point, mu, A):
    x1=starting_point[0]
    x2=starting_point[1]
    y1=starting_point[2]
    jacobian=np.empty([3,3])
    
    jacobian[0][0]=-mu
    jacobian[0][1]=y1
    jacobian[0][2]=x2
    jacobian[1][0]=y1-A
    jacobian[1][1]=-mu
    jacobian[1][2]=-A*x1
    jacobian[2][0]=-x2
    jacobian[2][1]=-x1
    jacobian[2][2]=0
    
    return jacobian

def max_eigenvector (jacobian):
    eigenvalues, eigenvectors=la.eig(jacobian)
    index_max=np.where(max(eigenvalues))
    max_eigenvector=eigenvectors[index_max][0]
    return max_eigenvector.real

def perturbed_start (starting_point, mu, k, factor):
    A=mu*(k**2-k**-2)
    jacobian_matrix=jacobian(starting_point, mu, A)
    max_eigenvect=max_eigenvector(jacobian_matrix)
    return starting_point+factor*max_eigenvect
    
