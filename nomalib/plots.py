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
    plot_base_stations(g.sites)
    if connect:
        plot_cell_connections(g)
    # plot_hexagon(g.hex, label='edge')
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
def plot_coordinates(coord, style='ok', size=10):
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
def plot_base_stations(sites, style='^b', size=10):
    x = np.array([])
    y = np.array([])
    for s in sites:
        x = np.append(x, s.bs.coord.x)
        y = np.append(y, s.bs.coord.y)
    plt.plot(x, y, style, ms=size, label='BS', mec='k')

# plot one cells
def plot_cell(site, cell_id):
    if site.bs.live:
        c = site.get_cell(cell_id)
        hex = utl.Hexagon(c.r, c.center)
        plot_hexagon(hex, '--k', lw=0.5)
    else:
        logger.warn("BS with id= "+str(site.bs.id)+" don't started.")
        
# plot all cells of one BS
def plot_cells(site):
    if site.bs.live:
        for c in site.cells:
            plot_cell(site, c.id)
    else:
        logger.warn("BS with id = "+str(site.bs.id)+" don't started.")

# plot all cells on gruid
def plot_all_cells(grid):
    for site in grid.sites:
        plot_cells(site)

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
    for s in grid.sites:
        for c in s.cells:
            for ue_id in c.ue_ids:
                ue = grid.get_ue(ue_id)
                x = [ue.coord.x, s.bs.coord.x]
                y = [ue.coord.y, s.bs.coord.y]
                plt.plot(x, y, '-'+colors[i], lw=.8)
            i = (i+1) if (i < 2) else (0)
    for ue in grid.user_equipments:
        if not ue.connected:
            logger.warn("UE with id = "+str(ue.id)+" don't connected.")

# plot frequency reuse scheme
def plot_frequency(grid):
    colors = 'cmy'
    for site in grid.sites:
        for c in site.cells:
            x = c.center.x
            y = c.center.y
            plt.plot(x, y, 'H'+colors[c.fr], ms=30)
            plt.text(x-50, y-50 ,str(c.fr), fontsize=13)

# plot antenna patter and attenuation for one cells of one BS
def plot_cell_attenuation(site, sector, sh=False, save=False, filename='cell_att', den=const.MAP_D):
    if site.bs.live:
        if sector in range(const.N_SEC):
            cell = site.cells[sector]
        else:
            logger.warn('Invalid sector index. The fisrt sector will be plotted.')
            cell = site.cells[0]
        w = 16*site.cells[0].r
        h = 8*site.cells[0].r*np.sqrt(3)
        px = int(round(w/den))
        py = int(round(h/den))
        c = site.bs.coord
        o = Coord(w/2, h/2)
        axis = [-w/2+c.x, w/2+c.x, -h/2+c.y, h/2+c.y]
        im = np.zeros([py, px])
        att = site.channel.path_loss.attenuation
        shw = site.channel.shadow.get_shw
        for x in range(px):
            for y in range(py):
                p = Coord(x*den, y*den)
                s_p = Coord(p.x-o.x, p.y-o.y)            
                theta = utl.get_angle(p, o)
                dist = utl.get_distance(p, o)
                im[y][x] = - cell.antenna.radiation_pattern(theta) + att(dist) + shw(s_p)
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
def plot_bs_attenuation(site, sh=False, save=False, filename='bs_att', den=const.MAP_D):
    if site.bs.live:
        w = 16*site.cells[0].r
        h = 8*site.cells[0].r*np.sqrt(3)
        px = int(round(w/den))
        py = int(round(h/den))        
        c = site.bs.coord
        o = Coord(w/2, h/2)
        axis = [-w/2+c.x, w/2+c.x, -h/2+c.y, h/2+c.y]
        im = np.zeros([py, px])
        att = site.channel.path_loss.attenuation
        shw = site.channel.shadow.get_shw        
        for c in site.cells:
            for x in range(px):
                for y in range(py):
                    p = Coord(x*den, y*den)
                    s_p = Coord(p.x-o.x, p.y-o.y)
                    theta = utl.get_angle(p, o)
                    if (c.antenna.theta_d == 0 and theta >= np.deg2rad(300)):
                        theta -= 2*np.pi
                    dist = utl.get_distance(p, o)
                    if (abs(theta-c.antenna.theta_d) < np.deg2rad(60)):
                        im[y][x] = -c.antenna.radiation_pattern(theta) + att(dist) + shw(s_p)
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
def plot_shadow(r=const.R_CELL, sh=False, input='s1.npy', filename='shadow', save=False):
    shw = np.load(const.DAT_PATH+input)
    shw = shw[::-1][:]
    y, x = shw.shape
    h = y*const.SHW_D
    w = x*const.SHW_D
    axis = [-w/2, w/2, -h/2, h/2]
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

def plot_shadow_zoom(r=const.R_CELL, n=50, sh=False, input='s1.npy', filename='shadow', save=False):
    shw = np.load(const.DAT_PATH+input)
    shw = shw[::-1][:]
    y, x = shw.shape
    h = n*const.SHW_D
    w = n*const.SHW_D
    c_y = int(round(y/2))
    c_x = int(round(x/2))
    axis = [-w/2, w/2, -h/2, h/2]
    shw_zoom = shw[c_y-int(n/2):c_y+int(n/2):, c_x-int(n/2):c_x+int(n/2):]
    plt.imshow(shw_zoom, cmap=plt.cm.jet, interpolation='bilinear', extent=axis)
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

def plot_doppler_filter(ssf, sh=False, save=False, filename='doppler_spread'):
    s = ssf.s
    f = ssf.f
    plt.plot(f, s*1e3, 'r')
    plt.xlabel('Frequency (Hz)',fontsize=14)
    plt.ylabel('Power (mW)',fontsize=14)
    plt.title('Power Spectral Density of Doppler Filter')
    plt.grid(True)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_channel_gain(ssf, sh=False, save=False, filename='ch_gain'):
    g = ssf.gain
    t = ssf.t
    plt.plot(t*1e3, g, 'b')
    plt.xlabel('Time (ms)',fontsize=14)
    plt.ylabel('Gain (dB)',fontsize=14)
    plt.grid(True)
    plt.title(r'Rayleigh Channel ($DS_{max}=9.27$ Hz)')
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()