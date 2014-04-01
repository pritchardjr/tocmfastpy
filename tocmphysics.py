#!/usr/bin/python
#Jonathan Pritchard
"""
This code is designed to analyse statistics of a box produced by 21cmFast

Underlying this is the Box class, which should contain all relevant info
on the box itself and its parameters and data

This file contains the physics of the 21cm line to calculate the optical
depth and other important quantities

"""
from Box import *
from PDF import *
import numpy as np
import os
import math
import string
import matplotlib.pyplot as plt

def getTau(z,density,xH,TS= 1):
    """
    Given NumPy arrays for density, xH and TS calculate the corresponding
    21cm optical depth in each cell


    should extend later to allow for velocity field
    """
    norm=0.009*pow(1+z,1.5)
    tau=norm*(1+density)*xH/TS

    return tau

def getTS(z):
    """
    Calculate the spin temperature at a given redshift
    Not a totally straightforward thing to work out.
    """

    TS=1
    
    return TS

    
