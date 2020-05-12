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


class dynamo:
    """this class represents a single simulation
       states and parameters are stored"""
    
    def __init__ (self, mu, k):
        """setting parameters"""
        if (abs(k)<10**-154 or k**2>10**154):
            warnings.warn("value of k too big or too small, A will be set as nan")
            self.A=np.nan
        else:
            self.mu=mu
            self.k=k
            self.A=self.mu*(self.k**2-self.k**-2) 
        
    


#######TESTS#######
@given(mu=st.floats(), k=st.floats())
def test_parameters (mu, k):
    assume (k!=0)
    assume (k**2<10**154)
    assume (abs(mu)<10**100)
    assume (abs(k)>10**-100)
    A_test=mu*(k**2-k**-2)
    dynamo_test=dynamo(mu, k)
    assert dynamo_test.A==A_test