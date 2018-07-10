#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 08/07/2018
# Version: 0.1

# Python module for NOMA communications simulations
# Default simulation scenario values

# Simulations Paramters
TTI = 1e-3 # ms
T_SNP = 1000*TTI # s
N_SNP = int(1e4) # ideal 1e5
OUT_PATH = './output/dat/'

# Base Staion Constants
H_BS = 30 # meters
G_BS = 15 # dBi
BW = 10e6 # Hz
PW_BS_MAX = 46 # dBm

# BS Antenna Constants
ATT_MAX = 20 # dBm
THT_3DB = 65 # degree

# User Equipment Constants
PW_UE_MAX = 25 # dBm
H_UE = 1.5 # meters
G_UE = 0 # dBi
NF_UE = 9 # dB

# Grid Constants
N_UE_CELL = 2
N_BS = 19
N_SEC = 3 # three sectors
N_CELL = N_BS*N_SEC
N_UE = N_UE_CELL*N_CELL
R_CELL = 500/3 # Cell Radius in meters
N_MA_UE = 2 # number of UE on multiple access

# Channel Model Constants
ENV = 'urban' # urban or rural
FC = 2e3# MHz
MCL = 70 # dB
N_DEN = -174 # dBm/Hz (290 degree K)
TEMP = 17 # Celsius]

# Small-Scale Fading
FC_H = 2e9 # Hz
SPD = 5/3.6 # 5 km/h = 1.3889 m/s
C = 299792458.0

# Attenuation map
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

# Performance Constants
SHN_ATT = 0.75
# THR_TARGET = 80e6 # Mhz on 10Mhz band width # deprecated
N_CDF_ARG = 3