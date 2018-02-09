#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 06/02/2018
# Version: 1.0

# Python module for NOMA communications simulations
# The plot functions are declared here

import nomalib.devices as dev
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
# show figure
def show_fig(sh=False):
    if sh:
        plt.show()

# plot grid object
def plot_grid(g, sh=False, save=False ,sh_hex=False, filename='grid'):
    plot_coordinates(g.coordinates)
    plot_user_equipments(g.user_equipments)
    plot_base_stations(g.base_stations)
    if sh_hex:
        plot_hexagon(g.hex)
	# set figures axis and title
    plt.axis('on')
    plt.grid(False)
    plt.legend(fontsize=12)
    plt.xlabel('Posição x [m]', fontsize=12)
    plt.ylabel('Posição y [m]', fontsize=12)
    show_fig(sh)
    save_fig(filename, save)

# plot hexagon object
def plot_hexagon(hex:utl.Hexagon, style='--g'):
    plt.plot(hex.x_axis, hex.upper, style, label='edge')
    plt.plot(hex.x_axis, hex.bottom, style)

# plot coordinates
def plot_coordinates(coord, style='ow', size=12):
    x = np.array([])
    y = np.array([])
    for c in coord:
        x = np.append(x, c.x)
        y = np.append(y, c.y)
    plt.plot(x, y, style, ms=size)

# plot user equipments
def plot_user_equipments(ue, style='+r', size=8):
    x = np.array([])
    y = np.array([])
    for u in ue:
        x = np.append(x, u.coord.x)
        y = np.append(y, u.coord.y)
    plt.plot(x, y, style, ms=size, label='UE')

# plot base station
def plot_base_stations(bs, style='3k', size=20):
    x = np.array([])
    y = np.array([])
    for b in bs:
        x = np.append(x, b.coord.x)
        y = np.append(y, b.coord.y)
    plt.plot(x, y, style, ms=size, label='BS')



    
