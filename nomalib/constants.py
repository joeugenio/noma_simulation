#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 30/01/2018
# Version: 1.0

# Python module for NOMA communications simulations
# Default simulation scenario values

# Base Staion Constants
PW_BS = 43 # dBm
H_BS = 30 # meters
G_BS = 15 # dBi

# Grid Constants
N_UE = 500
N_BS = 19
N_SEC = 3 # three sectors
R_CELL = 250 # Cell Radius in meters

# User Equipment Constants
PW_UE = 25 # dBm
H_UE = 1.5 # meters
G_UE = 0 # dBi

# Channel Model Constants
ENV = 'urban' # urban or rural
FC = 2e3 # MHz
MCL = 70 # dB

# attenuation map
PX = 101 # odd number

# Shadow Fading
SD = 10 # sd [dB]
M_SH = 0 # mean
N_SH = 201 # M_SH x M_SH elements

# Plot Figure Constantes
FORMAT = 'eps'
DPI = 72
IMG_PATH = './output/img/'
