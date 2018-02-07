#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 06/02/2018
# Version: 1.0

# Python module for NOMA communications simulations
# The plot functions are declared here

import nomalib.scenario as scn
import nomalib.utils as utl
import numpy as np
import matplotlib.pyplot as plt

# functions

# plot grid object
def plot_grid(g:scn.Grid, sh_hex=False, hex_style='--b'):
    c = g.coordinates
    u = g.users
    x_c = []
    y_c = []
    x_u = []
    y_u = []
    for p in c:
        x_c = np.append(x_c,p.x)
        y_c = np.append(y_c,p.y)
    for k in u:
        x_u = np.append(x_u,k.coord.x)
        y_u = np.append(y_u,k.coord.y)
    plt.plot(x_c,y_c,'^k', ms=10)
    plt.plot(x_u, y_u, '+r', ms=8)
    if sh_hex:
        plot_hexagon(g.hex, hex_style)
    plt.show()

# plot hexagon object
def plot_hexagon(hex:utl.Hexagon, style='--b'):
    plt.plot(hex.x_axis, hex.upper, style, hex.x_axis, hex.bottom, style)
    plt.show()