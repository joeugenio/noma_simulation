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
import nomalib.constants as const
import numpy as np
import matplotlib.pyplot as plt

# functions


# save figures
def save_fig(filename, save=False):
    if save:
        plt.savefig(const.IMG_PATH+filename+'.'+const.FORMAT, format=const.FORMAT, dpi=const.DPI)
        plt.clf()

def show_fig(sh=False):
    if sh:
        plt.show()

# plot grid object
def plot_grid(g:scn.Grid, sh=False, save=False ,sh_hex=False, filename='grid'):
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
    plt.plot(x_c,y_c,'ow', ms=12)
    plt.plot(x_u, y_u, '+r', ms=8, label='UE')
    if sh_hex:
        plot_hexagon(g.hex)
    plt.axis('on')
    plt.grid(False)
    plt.legend(fontsize=12)
    plt.xlabel('Posição x [m]', fontsize=12)
    plt.ylabel('Posição y [m]', fontsize=12)
    show_fig(sh)
    save_fig(filename, save)

# plot hexagon object
def plot_hexagon(hex:utl.Hexagon, sh=False, save=False, style='--g', filename='hex'):
    plt.plot(hex.x_axis, hex.upper, style, label='edge')
    plt.plot(hex.x_axis, hex.bottom, style)
    show_fig(sh)
    save_fig(filename, save)