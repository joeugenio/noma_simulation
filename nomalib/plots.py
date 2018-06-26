#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 06/02/2018
# Version: 0.1

# Python module for NOMA communications simulations
# The plot functions are declared here

import nomalib.constants as const
import nomalib.devices as dev
import nomalib.utils as utl
import nomalib.channel as ch
import nomalib.performance as perf
from nomalib.utils import Coordinate as Coord
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
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
def plot_grid(g, sh=False, save=False, filename='grid', cells=False, ue=False, connect=False):
    # plot_coordinates(g.coordinates)
    if ue:
        plot_user_equipments(g.user_equipments)
    plot_base_stations(g.sites)
    if connect:
        plot_cell_connections(g)
    # plot_hexagon(g.hex, label='edge')
    if cells:
        plot_all_cells(g)
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
    # plt.plot(x, y, style, ms=size, label='BS', mec='k')
    plt.plot(x, y, style, ms=size, label='ERB', mec='k')

# plot one cells
def plot_cell(site, cell_id, style='--k'):
    if site.bs.live:
        c = site.get_cell(cell_id)
        hex = utl.Hexagon(c.r, c.center)
        plot_hexagon(hex, style=style, lw=0.5)
    else:
        logger.warn("BS with ID= "+str(site.bs.id)+" don't started.")
        
# plot all cells of one BS
def plot_cells(site, style='--k'):
    if site.bs.live:
        for c in site.cells:
            plot_cell(site, c.id, style=style)
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
def plot_cell_attenuation(site, sector=1, sh=False, save=False, filename='cell_att', den=const.MAP_D, shw_level=1):
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
                im[y][x] = - cell.antenna.radiation_pattern(theta) + att(dist) + shw(s_p)*shw_level
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

# plot antenna patter and attenuation for one UE in one Site
def plot_ue_attenuation(ue, channel, r=const.R_CELL, sh=False, save=False, filename='ue_att', den=const.MAP_D, shw_level=0):
    w = 16*r
    h = 8*r*np.sqrt(3)
    px = int(round(w/den))
    py = int(round(h/den))
    c = ue.coord
    o = Coord(w/2, h/2)
    axis = [-w/2+c.x, w/2+c.x, -h/2+c.y, h/2+c.y]
    im = np.zeros([py, px])
    att = channel.path_loss.attenuation
    shw = channel.shadow.get_shw
    for x in range(px):
        for y in range(py):
            p = Coord(x*den, y*den)
            s_p = Coord(p.x-o.x, p.y-o.y)            
            theta = utl.get_angle(p, o)
            dist = utl.get_distance(p, o)
            im[y][x] = - ue.antenna.radiation_pattern(theta) + att(dist) + shw(s_p)*shw_level
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

# plot lognormal shadow fading
def plot_shadow(r=const.R_CELL, sh=False, input='s1.npy', filename='shadow', save=False):
    shw = np.load(const.DAT_PATH+input)
    shw = shw[::-1][:]
    y, x = shw.shape
    h = y*const.SHW_D
    w = x*const.SHW_D
    axis = [-w/2, w/2, -h/2, h/2]
    plt.imshow(shw, cmap=plt.cm.jet, interpolation='bilinear', extent=axis)
    plt.grid(True)
    plt.tick_params(labelsize=14)
    plt.xlabel('Posição x [m]', fontsize=14)
    plt.ylabel('Posição y [m]', fontsize=14)
    plt.axis('on')
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

def plot_doppler_filter(h, sh=False, save=False, filename='doppler_spread'):
    s = h.s
    f = h.f
    plt.plot(f, s*1e3, 'r')
    plt.yticks([])
    plt.grid(False)
    # plt.xlabel('Frequency (Hz)',fontsize=14)
    # plt.ylabel('Power (mW)',fontsize=14)
    # plt.title('Power Spectral Density of Doppler Filter')
    plt.xlabel('Frequência (Hz)',fontsize=14)
    plt.ylabel('DEP',fontsize=14)
    # plt.title('Densidade Espectral de Potência do Filtro Doppler')
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_channel_gain(h, sh=False, save=False, filename='ch_gain'):
    g = h.gain_db
    t = h.t
    plt.plot(t*1e3, g, 'b')
    # plt.xlabel('Time (ms)',fontsize=14)
    # plt.ylabel('Gain (dB)',fontsize=14)
    plt.xlabel('Tempo (ms)',fontsize=14)
    plt.ylabel('Ganho (dB)',fontsize=14)
    plt.grid(True)
    # plt.title(r'Rayleigh Channel ($DS_{max}=9.27$ Hz)')
    # plt.title(r'Canal Rayleigh ($DS_{max}=9.27$ Hz)')
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_l2s(sh=False, save=False, filename='l2s_model'):
    sinr = np.linspace(-10, 30)
    amc = perf.amc_lte(sinr)
    shn = perf.shannon(sinr, bw=1)
    shn_att = perf.shannon_att(sinr, bw=1)
    plt.plot(sinr, amc, '-', lw=1, label='AWGN AMC')
    plt.plot(sinr, shn, '-.', lw=3, label='AWGN Shannon')
    # plt.plot(sinr, shn_att,'-', label='Truncated '+str(const.SHN_ATT)+'*Shannon')
    plt.plot(sinr, shn_att, '--', lw=2, label='Truncado '+str(const.SHN_ATT)+'*Shannon')
    plt.xlabel('SINR (dB)',fontsize=16)
    # plt.ylabel('Throughput (bits/s/Hz)',fontsize=16)
    plt.ylabel('Eficiência Espectral  (bits/s/Hz)',fontsize=16)
    plt.grid(True)
    # plt.title('Link Level Performance Model', fontsize=16)
    plt.legend(fontsize=14, loc=2)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_path_loss(d=1, sh=False, save=False, filename='path_loss'):
    x = np.linspace(0,d,1001)
    pl1 = ch.PathLoss(env='urban', fc=2e3)
    pl2 = ch.PathLoss(env='urban', fc=900)
    pl3 = ch.PathLoss(env='rural', fc=900)
    l1 = [pl1.attenuation(i) for i in x]
    l2 = [pl2.attenuation(i) for i in x]
    l3 = [pl3.attenuation(i) for i in x]
    ax = x*1000
    # plt.axis([0, 1000, -20, 140])
    plt.plot(ax, l1, '-b', lw=1.5,label='Urbano 2000 MHz')
    plt.plot(ax, l2, '--g', lw=2.5,label='Urbano 900 MHz')
    plt.plot(ax, l3, '-.r', lw=4.5,label='Rural 900 MHz')
    plt.tick_params(labelsize=14)
    plt.xlabel('Distância [m]', fontsize=14)
    plt.ylabel('Perda de Percurso [dB]', fontsize=14)
    # plt.xticks(x[::100]*1000)
    plt.grid(True)
    plt.legend(fontsize=14, loc='lower right')
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_pattern(antenna, sh=False, save=False, filename='cell_pattern'):
    theta = np.linspace(-180, 180, 100)
    r = [antenna.radiation_pattern(np.deg2rad(t)) for t in theta]
    plt.plot(theta, r, lw = 2)
    plt.axis([-180, 180, -20, 0])
    plt.tick_params(labelsize=14)
    plt.xlabel('Ângulo Horizontal [Graus]', fontsize=14)
    plt.ylabel('Ganho [dB]',fontsize=14)
    plt.grid(True)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_polar_pattern(antenna, sh=False, save=False, filename='cell_polar_pattern'):
    theta = np.linspace(-180, 180, 100)
    r = [antenna.radiation_pattern(np.deg2rad(t)) for t in theta]
    ax = plt.subplot(111, projection='polar')
    ax.plot(np.radians(theta),r, label='Setor 1')
    ax.plot(np.radians(theta+120),r, label='Setor 2')
    ax.plot(np.radians(theta-120),r, label='Setor 3')
    ax.set_rmin(-20)
    ax.set_rmax(0)
    ax.set_yticks([-20, -15, -10, -5, 0])
    ax.tick_params(labelsize=14)
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.33, 0.13),fontsize=14)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_measure(grid, sh=False, save=False, filename='measure'):
    s1 = grid.sites[9]
    s2 = grid.sites[10]
    r = s1.cells[0].r
    c10 = s1.cells[0].center
    c20 = s2.cells[0].center
    c11 = s1.cells[1].center
    c22 = s2.cells[2].center
    plot_base_stations([s1, s2], style='ow', size=20)
    plot_cells(s1, style='-k')
    plot_cells(s2, style='-k')
    ax = plt.axes()
    ax.axis([-300, 900, -450, 450])
    ax.vlines(c10.x-r, c10.y-80, c10.y+80, linestyles='dashed', lw=1)
    ax.vlines(c20.x-r, c20.y-80, c20.y+80, linestyles='dashed', lw=1)
    ax.annotate(s='', xy=(c10.x-r, c10.y), xytext=(c20.x-r,c20.y), arrowprops=dict(arrowstyle='<->', color='r', lw=2))
    ax.text(c10.x-100,c10.y-25,'Dist. inter-site\n      3R', fontsize=12)
    ax.vlines(c11.x-r, c11.y-80, c11.y+80, linestyles='dashed', lw=1)
    ax.vlines(c11.x, c11.y-80, c11.y+80, linestyles='dashed', lw=1)
    ax.annotate(s='', xy=(c11.x-r, c11.y), xytext=(c11.x, c11.y), arrowprops=dict(arrowstyle='<->', color='r', lw=2))
    ax.text(c11.x-100, c11.y-25 ,'Raio\n  R', fontsize=12)
    ax.vlines(c22.x-r, c22.y-80, c22.y+80, linestyles='dashed', lw=1)
    ax.vlines(c22.x+r, c22.y-80, c22.y+80, linestyles='dashed', lw=1)
    ax.annotate(s='', xy=(c22.x-r,c22.y), xytext=(c22.x+r, c22.y), arrowprops=dict(arrowstyle='<->', color='r', lw=2))
    ax.text(c22.x-100 ,c22.y-25,'Alcance da Cel.\n         2R', fontsize=12)
    plt.xlabel('Posição x [m]', fontsize=15)
    plt.ylabel('Posição y [m]', fontsize=15)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_cdf_noma_oma(n, o, sh=False, save=False, filename='cdf', lab=''):
    plt.plot(n[0], n[1], '-*', lw=1, label=lab[0])
    plt.plot(o[0], o[1], '--o', lw=1, label=lab[1])
    # plt.plot([0, 14.14, 14.14],[1-.0503, 1-.0503,0],'--r')
    # plt.plot([13.43, 13.43],[1-.0503,0],'--r')
    # plt.text(3,.06, '95% FCP', fontsize=14)
    # plt.plot([0, 29.7, 29.7],[1-.5131, 1-.5131,0],'--r')
    # plt.plot([24.74, 24.74],[1-.5131,0],'--r')
    # plt.text(3,.44, '50% FCP', fontsize=14)
    # plt.plot([0, 52.32, 52.32],[1-.9533, 1-.9533,0],'--r')
    # plt.plot([40.30, 40.30],[1-.9533,0],'--r')
    plt.text(3,.9, '5% FCP', fontsize=14)
    plt.grid(True)
    plt.legend(fontsize=14, loc='upper right')
    plt.xlabel('Taxa de dados [Mbps]', fontsize=17)
    # plt.ylabel('CCDF', fontsize=14)
    plt.ylabel(r'FCPC    $P[X>x]$', fontsize=17)
    plt.tick_params(labelsize=14)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_multi_user_gain(n, o, u,sh=False, save=False, filename='m_user_gain', lab=''):
    plt.plot(u, n[0], '-*', lw=1, label=lab[0][0], ms=8)
    plt.plot(u, n[1], '-^', lw=1, label=lab[0][1], ms=8)
    plt.plot(u, n[2], '-s', lw=1, label=lab[0][2], ms=8)
    plt.plot(u, o[0], '--o', lw=2, label=lab[1][0], ms=8)
    plt.plot(u, o[1], '--d', lw=2, label=lab[1][1], ms=8)
    plt.plot(u, o[2], '--v', lw=2, label=lab[1][2], ms=8)
    plt.grid(True)
    plt.legend(fontsize=14, loc='upper right', ncol=2)
    plt.xlabel('Número de usuários', fontsize=17)
    plt.ylabel('Eficiência Espectral da Célula [bps/Hz]', fontsize=17)
    plt.tick_params(labelsize=14)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_coeff_gain(n, o, u,sh=False, save=False, filename='coeff_gain', lab=''):
    fig = plt.figure()
    ax = plt.subplot(111)
    plt.plot(u, n[0], '-*b', lw=1, label=lab[0][0], ms=9)
    plt.plot(u, n[1], '-^g', lw=1, label=lab[0][1], ms=9)
    plt.plot(u, o[0], '--or', lw=2, label=lab[1][0], ms=9)
    plt.plot(u, o[1], '--dm', lw=2, label=lab[1][1], ms=9)
    plt.grid(True)
    plt.legend(fontsize=14, loc='lower right', ncol=2)
    plt.xlabel('Coef. de Alocação de Potência', fontsize=17)
    plt.ylabel('Eficiência Espectral da Célula [bps/Hz]', fontsize=17)
    plt.tick_params(labelsize=14)
    e1 = patches.Ellipse((.2 , 1), .05, .8, ls='--', angle=0, linewidth=1, fill=False, zorder=2)
    e2 = patches.Ellipse((.2 , 2.5), .07, 1.5, ls='--' ,angle=0, linewidth=1, fill=False)
    plt.text(.31, 1.7, 'Ganho máx.', fontsize=14)
    plt.plot([.2, .3],[1.4,1.7],'-k', [.2, .3],[1.75,1.7],'-k', lw=0.5)
    ax.add_artist(e1)
    ax.add_artist(e2)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()

def plot_cell_edge_user(n, o, u, sh=False, save=False, filename='cell_edge', lab=''):
    plt.plot(u, n, '-*b', lw=1, label=lab[0], ms=9)
    plt.plot(u, o, '--or', lw=2, label=lab[1], ms=9)
    plt.grid(True)
    plt.legend(fontsize=14, loc='upper right', ncol=2)
    plt.xlabel('Número de usuários', fontsize=17)
    plt.ylabel('Eficiência Espectral do Usuário [bps/Hz]', fontsize=17)
    plt.tick_params(labelsize=14)
    save_fig(filename, save)
    show_fig(sh)
    plt.clf()