#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:27:48 2020

@author: mani
"""
import numpy as np
from hypothesis import given, assume
import hypothesis.strategies as st
import os
import integrator
import read_data



@given(mu=st.floats(10e-100,1e+99), k=st.floats(10e-100, 10e+99))
def test_parameters (mu, k):
    A_test=mu*(k**2-k**-2)
    dynamo_test=integrator.dynamo(mu, k, 10, [1, 1, 1], "filename", 2**-8)
    assert dynamo_test.A==A_test
    
@given(x2_init=st.floats(), x1_init=st.floats(), y1_init=st.floats(), N_steps=st.integers(1,10e+7))
def test_initial_conditions (x1_init, x2_init, y1_init, N_steps):
    assume (not np.isnan(x1_init ))
    assume (not np.isnan(x2_init ))
    assume (not np.isnan(y1_init ))
    dynamo_test=integrator.dynamo(1,1, N_steps, [x1_init, x2_init, y1_init], 'filename', 2**-8)
    assert len(dynamo_test.x1)==N_steps
    assert len(dynamo_test.x1)==len(dynamo_test.x2)
    assert len(dynamo_test.x2)==len(dynamo_test.y1)
    assert len(dynamo_test.y1)==len(dynamo_test.y2)
    assert dynamo_test.x1[0]==x1_init
    assert dynamo_test.x2[0]==x2_init
    assert dynamo_test.y1[0]==y1_init
    
    
@given(mu=st.floats(0,1e+2), k=st.floats(1e-2, 1e+2), sign=st.booleans())
def test_steady_state(mu, k, sign):
    #assume(abs(mu*(k**2-k**-2))<10**2)
    if sign:
        sign=+1
    else:
        sign=-1
    x1_0=sign*k
    x2_0=sign/k
    y1_0=mu*k**2
    y2_0=mu*k**-2
    dynamo_test=integrator.dynamo(mu,k,30, [x1_0, x2_0, y1_0], "test_output.csv", 2**-8)
    dynamo_test.evolve()
    dynamo_test.write_results()
    t, x1, x2,  y1, y2, mu, k=read_data.get_data("test_output.csv", '1')
    assert (abs(x1[-1]-x1_0)<2*10**-6)
    assert (abs(x2[-1]-x2_0)<2*10**-6)
    assert (abs(y1[-1]-y1_0)<2*10**-6)
    assert (abs(y2[-1]-y2_0)<2*10**-6)
    os.remove("test_output.csv")
    
