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
from nomalib.utils import Coordinate as Coord
import nomalib.constants as const
import numpy as np
import matplotlib.pyplot as plt
from logzero import logger

# functions

# save figures
def save_fig(filename, save=False):
    if save:
        plt.savefig(const.IMG_PATH+filename+'.'+const.FORMAT, format=const.FORMAT, dpi=const.DPI)

# show figure
def show_fig(sh=False):
    if sh:
        plt.show()

# plot grid object
def plot_grid(g, sh=False, save=False, filename='grid',connect=False):
    # plot_coordinates(g.coordinates)
    plot_user_equipments(g.user_equipments)
    plot_base_stations(g.base_stations)
    if connect:
        plot_cell_connections(g)
    # plot_hexagon(g.hex, label='edsge')
    # plot_all_cells(g)
    # plot_frequency(g)
	# set figures axis and title
    plt.axis('on')
    plt.grid(False)
    plt.legend(fontsize=12)
    plt.xlabel('Posição x [m]', fontsize=12)
    plt.ylabel('Posição y [m]', fontsize=12)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

# plot hexagon object
def plot_hexagon(hex:utl.Hexagon, style='--g', lw=0.5, label=None):
    plt.plot(hex.x_axis, hex.upper, style, lw=lw, label=label)
    plt.plot(hex.x_axis, hex.bottom, style, lw=lw)

# plot coordinates
def plot_coordinates(coord, style='ow', size=10):
    x = np.array([])
    y = np.array([])
    for c in coord:
        x = np.append(x, c.x)
        y = np.append(y, c.y)
    plt.plot(x, y, style, ms=size)

# plot user equipments
def plot_user_equipments(ue, style='sw', size=3):
    x = np.array([])
    y = np.array([])
    for u in ue:
        x = np.append(x, u.coord.x)
        y = np.append(y, u.coord.y)
    plt.plot(x, y, style, ms=size, label='UE', mec='k')

# plot base station
def plot_base_stations(bs, style='^b', size=10):
    x = np.array([])
    y = np.array([])
    for b in bs:
        x = np.append(x, b.coord.x)
        y = np.append(y, b.coord.y)
    plt.plot(x, y, style, ms=size, label='BS', mec='k')

# plot one cells
def plot_cell(bs, cell_id):
    if bs.started:
        c = bs.get_cell(cell_id)
        hex = utl.Hexagon(c.r, c.center)
        plot_hexagon(hex, '--k', lw=0.5)
    else:
        logger.warn("BS with id= "+str(bs.id)+" don't started.")
        
# plot all cells of one BS
def plot_cells(bs):
    if bs.started:
        for c in bs.cells:
            plot_cell(bs, c.id)
    else:
        logger.warn("BS with id = "+str(bs.id)+" don't started.")

# plot all cells on gruid
def plot_all_cells(grid):
    for bs in grid.base_stations:
        plot_cells(bs)

# show connections from UE view
def plot_ue_connections(grid):
    for ue in grid.user_equipments:
        if ue.connected:
            bs = grid.get_bs(ue.bs_id)
            x = [ue.coord.x, bs.coord.x]
            y = [ue.coord.y, bs.coord.y]
            plt.plot(x, y, '-b', lw=.2)
        else:
            logger.warn("UE with id = "+str(ue.id)+" don't connected.")

# show connections from BS view
def plot_bs_connections(grid):
    colors = 'bgrcmy'*4
    i = 0
    for bs in grid.base_stations:
        for ue_id in bs.ue_ids:
            ue = grid.get_ue(ue_id)
            x = [ue.coord.x, bs.coord.x]
            y = [ue.coord.y, bs.coord.y]
            plt.plot(x, y, '-'+colors[i], lw=.3)
        i += 1
    for ue in grid.user_equipments:
        if not ue.connected:
            logger.warn("UE with id = "+str(ue.id)+" don't connected.")

# show connections from cell view
def plot_cell_connections(grid):
    colors = 'cmy'
    i = 0
    for bs in grid.base_stations:
        for c in bs.cells:
            for ue_id in c.ue_ids:
                ue = grid.get_ue(ue_id)
                x = [ue.coord.x, c.coord.x]
                y = [ue.coord.y, c.coord.y]
                plt.plot(x, y, '-'+colors[i], lw=.8)
            i = (i+1) if (i < 2) else (0) 
    for ue in grid.user_equipments:
        if not ue.connected:
            logger.warn("UE with id = "+str(ue.id)+" don't connected.")

# plot frequency reuse scheme
def plot_frequency(grid):
    colors = 'cmy'
    for bs in grid.base_stations:
        for c in bs.cells:
            x = c.center.x
            y = c.center.y
            plt.plot(x, y, 'H'+colors[c.ft], ms=30)
            plt.text(x-50, y-50 ,str(c.ft), fontsize=13)

# plot antenna patter and attenuation for one cells of one BS
def plot_cell_attenuation(bs, sector, ch, sh=False, save=False, filename='cell_att', px=const.PX):
    if bs.started:
        if sector in range(const.N_SEC):
            cell = bs.cells[sector]
        else:
            logger.warn('Invalid sector index. The fisrt sector will be plotted.')
            cell = bs.cells[0]
        w = 4*cell.r
        u = w/(px-1)
        c = bs.coord
        o = Coord(w/2, w/2)
        axis = [-w/2+c.x, w/2+c.x, -w/2+c.y, w/2+c.y]
        im = np.zeros([px, px])
        att = ch.path_loss.attenuation
        for x in range(px):
            for y in range(px):
                p = Coord(x*u, y*u)
                theta = utl.get_angle(p, o)
                dist = utl.get_distance(p, o)
                im[y][x] = - cell.ant.radiation_pattern(theta) + att(dist)
        im = im[::-1][:]
        plt.imshow(im, cmap=plt.cm.jet, interpolation='bilinear', extent=axis)
        plt.axis('on')
        plt.grid(True)
        plt.tick_params(labelsize=14)
        plt.xlabel('Posição x [m]', fontsize=14)
        plt.ylabel('Posição y [m]', fontsize=14)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('[dB]', fontsize=14)
        cbar.ax.tick_params(labelsize=14)
        save_fig(filename, save)
        show_fig(sh)
        # plt.clf()
    else:
        logger.error('BS was not started. Run one start base station method.')

# plot antenna patter and attenuation for 3 cells of one BS
def plot_bs_attenuation(bs, ch, sh=False, save=False, filename='bs_att', px=const.PX):
    if bs.started:
        w = 4*bs.cells[0].r
        u = w/(px-1)
        c = bs.coord
        o = Coord(w/2, w/2)
        axis = [-w/2+c.x, w/2+c.x, -w/2+c.y, w/2+c.y]
        im = np.zeros([px, px])
        att = ch.path_loss.attenuation
        for c in bs.cells:
            for x in range(px):
                for y in range(px):
                    p = Coord(x*u, y*u)
                    theta = utl.get_angle(p, o)
                    if (c.ant.theta_d == 0 and theta >= np.deg2rad(300)):
                        theta -= 2*np.pi
                    dist = utl.get_distance(p, o)
                    if (abs(theta-c.ant.theta_d) < np.deg2rad(60)):
                        im[y][x] = -c.ant.radiation_pattern(theta) + att(dist)
        im = im[::-1][:]
        plt.imshow(im, cmap=plt.cm.jet, interpolation='bilinear', extent=axis)
        plt.axis('on')
        plt.grid(True)
        plt.tick_params(labelsize=14)
        plt.xlabel('Posição x [m]', fontsize=14)
        plt.ylabel('Posição y [m]', fontsize=14)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('[dB]', fontsize=14)
        cbar.ax.tick_params(labelsize=14)
        save_fig(filename, save)
        show_fig(sh)
        plt.clf()
    else:
        logger.error('BS was not started. Run one start base station method.')

# plot lognormal shadow fading
def plot_shadow(ch, sh=False, save=False, filename='shadow'):
    shw = ch.shadow.shw_map
    shw = shw[::-1][:]
    n = shw.shape[0]
    axis = [-n/2, n/2, -n/2, n/2]
    plt.imshow(shw, cmap=plt.cm.jet, interpolation='bilinear', extent=axis)
    plt.axis('on')
    plt.grid(True)
    plt.tick_params(labelsize=14)
    plt.xlabel('Posição x [m]', fontsize=14)
    plt.ylabel('Posição y [m]', fontsize=14)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('[dB]', fontsize=14)
    cbar.ax.tick_params(labelsize=14)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()