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
BW = 20e6 # Hz

# BS Antenna Constants
ATT_MAX = 20 # dBm
THT_3DB = 65 # degree

# User Equipment Constants
PW_UE = 25 # dBm
H_UE = 1.5 # meters
G_UE = 0 # dBi

# Grid Constants
N_UE = 500
N_BS = 19
N_SEC = 3 # three sectors
R_CELL = 500/3 # Cell Radius in meters

# Channel Model Constants
ENV = 'urban' # urban or rural
FC = 2e3# MHz
MCL = 70 # dB
N_DEN = -174 # dBm/Hz (290 degree K)

# attenuation map
PX = 101 # odd number

# Shadow Fading
SHW_M = 0
SHW_STD = 10
SHW_D = 5
R_SITE = .5
DAT_PATH = './dat/'
# Neighbour map for correlation generation
NB_MAP = [[11, 5, 10, 6, 12],[7, 1, 2, 3, 8],[9, 4, 13]]
NB = 13

# Plot Figure Constantes
FORMAT = 'eps'
DPI = 72
IMG_PATH = './output/img/'
MAP_D = 5
