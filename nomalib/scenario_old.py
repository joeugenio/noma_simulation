#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 29/01/2018
# Last update: 29/01/2018
# Version: 1.0

# Python classes for NOMA communications simulations
# The scenarios are defined based on 3GPP TR 36.942 v14.0.0

import numpy as np
import matplotlib.pyplot as plt

# Constants
# ===================================================================

# number of points on graphs
P = 100


# Classes
# ===================================================================

class Coord:
    ''' Coordinate x and y '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Area:
    ''' Interest area '''
    def __init__(self, width:int, hight:int):
        self.w = width
        self.h = hight

    def plot(self):
        ''' Plot the graphic region '''
        plt.plot(self.w, self.h)

class ENodeB:
    '''' eNodeB class'''
    def __init__(self, hight=30, power=40, n_sec=3):
        h = self.hight
        pw = self.power
        ns = self.n_sec

class Cell:
    ''' Three hexagonal sectors cell'''
    def __init__(self, r, pos:Coord):
        self.r = r
        self.p = pos

    # upper left limit of hexagon
    def ull(self, x):
        return np.sqrt(3)*(x)
    # upper center limit of hexagon
    def ucl(self, x):
        return self.r*np.sqrt(3)*.5*(x/x)
    # upper right limit of hexagon
    def url(self, x):
        return (2*self.r-x)*np.sqrt(3)
    # lower left limit of hexagon
    def lll(self, x):
        return (-1)*np.sqrt(3)*(x)
    # lower center limit of hexagon
    def lcl(self, x):
        return (-1)*self.r*np.sqrt(3)*.5*(x/x)
    # lower right limit of hexagon
    def lrl(self, x):
        return (x-2*self.r)*np.sqrt(3)

    # determine if one coordinate is in cell region
    def in_or_out(self, c:Coord):
        x = c.x-self.p.x
        cond_l = cond_c = cond_r = False
        if (0 <=  x < .5*self.r):
            if (self.lll(x) <= c.y-self.p.y <= self.ull(x)):
                cond_l = True
        elif (.5*self.r <= x < 1.5*self.r):
            if (self.lcl(x) <= c.y-self.p.y <= self.ucl(x)):
                cond_c = True
        elif (1.5*self.r <= x < 2*self.r):
            if (self.lrl(x) <= c.y-self.p.y <= self.url(x)):
                cond_r = True
        if (cond_l or cond_c or cond_r):
            return 'in'
        else:
            return 'out'

    # plot hexagonal cell
    def plot(self):
        # x axis
        x_l = np.linspace(0,.5*self.r,P)
        x_c = np.linspace(.5*self.r,1.5*self.r,P)
        x_r = np.linspace(1.5*self.r,2*self.r,P)
        # y axis
        y_lu = self.ull(x_l) + self.p.y
        y_cu = self.ucl(x_c) + self.p.y
        y_ru = self.url(x_r) + self.p.y
        y_ll = self.lll(x_l) + self.p.y
        y_cl = self.lcl(x_c) + self.p.y
        y_rl = self.lrl(x_r) + self.p.y
        # plot
        plt.plot(x_l + self.p.x, y_lu, 'k', x_c + self.p.x, y_cu, 'k', x_r + self.p.x, y_ru, 'k', lw=.5)
        plt.plot(x_l + self.p.x, y_ll, 'k', x_c + self.p.x, y_cl, 'k', x_r + self.p.x, y_rl, 'k', lw=.5)

class Site:
    ''' Site with 3 sectors '''
    def __init__(self, r, pos=Coord(0,0)):
        self.r = r
        self.p = pos
        self.c1 = Cell(r, Coord(self.p.x-1.5*r, self.p.y-np.sqrt(3)*r*.5))
        self.c2 = Cell(r, Coord(self.p.x-1.5*r, self.p.y+np.sqrt(3)*r*.5))
        self.c3 = Cell(r, Coord(self.p.x, self.p.y))

    def in_or_out(self, c):
        check = [self.c1.in_or_out(c), self.c2.in_or_out(c), self.c3.in_or_out(c)]

        if ('in' in check):
            return 'in'
        else:
            return 'out'

    def plot(self, enb=True):
        ''' Plot cells and eNodeB '''
        if enb:
            plt.plot(self.p.x, self.p.y, 'o', ms=25)
        self.c1.plot()
        self.c2.plot()
        self.c3.plot()

class Grid:
    ''' Hexagonal grid with 19 eNodeBs'''
    def __init__(self,r):
        self.r = r
        self.coord = [[Coord(5*r, np.sqrt(3)*r), Coord(8*r, np.sqrt(3)*r), Coord(11*r, np.sqrt(3)*r)],
                      [Coord(3.5*r, 2.5*np.sqrt(3)*r), Coord(6.5*r, 2.5*np.sqrt(3)*r), Coord(9.5*r, 2.5*np.sqrt(3)*r), Coord(12.5*r, 2.5*np.sqrt(3)*r)],
                      [Coord(2*r, 4*np.sqrt(3)*r), Coord(5*r, 4*np.sqrt(3)*r), Coord(8*r, 4*np.sqrt(3)*r), Coord(11*r, 4*np.sqrt(3)*r), Coord(14*r, 4*np.sqrt(3)*r)],
                      [Coord(3.5*r, 5.5*np.sqrt(3)*r), Coord(6.5*r, 5.5*np.sqrt(3)*r), Coord(9.5*r, 5.5*np.sqrt(3)*r), Coord(12.5*r, 5.5*np.sqrt(3)*r)],
                      [Coord(5*r, 7*np.sqrt(3)*r), Coord(8*r, 7*np.sqrt(3)*r), Coord(11*r, 7*np.sqrt(3)*r)]]
        x_ori = self.r*8
        y_ori = self.r*7
        self.sites = [];
        for line in self.coord:
            for c in line:
#                 c.x = c.x - x_ori
#                 c.y = c.y - y_ori
                self.sites += [Site(r,c)]

    def plot(self):
        for s in self.sites:
            s.plot()
        plt.xlabel('Posição x [m]', fontsize=12)
        plt.ylabel('Posição y [m]', fontsize=12)

    def plot_rad(self):
        c = int(np.ceil((3*5+1)*self.r))
        l = int(np.ceil(np.sqrt(3)*self.r*8))

        f_corr = 100
        im = np.zeros([l,c])
        im[:][:] = rx_pwr(d=(2*self.r/f_corr))

        for s in self.sites:
            o = s.p
            for x in range(c):
                for y in range(l):
                    if (s.in_or_out(Coord(x,y)) == 'in'):
                        dx = x-o.x
                        dy = y-o.y
                        try:
                            theta = np.arctan((dy)/(dx))
                        except ZeroDivisionError:
                            theta = np.arctan(float('Inf'))
                        if ((x-o.x) >= 0):
                            if (abs(theta) <= np.radians(60)):
                                im[y][x] = attenuation(theta)
                            elif (theta > np.radians(60)):
                                im[y][x] = attenuation(theta-np.radians(120))
                            elif (theta < np.radians(-60)):
                                im[y][x] = attenuation(theta+np.radians(120))
                        elif ((y-o.y)>=0):
                            im[y][x] = attenuation(theta+np.radians(60))
                        else:
                            im[y][x] = attenuation(theta-np.radians(60))

                        dist = (np.sqrt((dx**2)+(dy**2)))/f_corr
                        im[y][x] += rx_pwr(d=dist)

        im = im[::-1][:]
        ext=[-c*5,c*5,-l*5,l*5]
        plt.imshow(im, cmap=plt.cm.jet, interpolation='bilinear', extent=ext)
        plt.axis('on')
        plt.grid(True)
        plt.xlabel('Posição x [m]', fontsize=12)
        plt.ylabel('Posição y [m]', fontsize=12)
        plt.colorbar()

class Channel():
    ''' Channel propagation model'''
    def __init__(self, type):
        if (type=='Urban'):
            pass
        if (type=='Rural'):
            pass

# Funções do módulo
# ===================================================================

    # radiation pattern
def plot_pattern():
    theta = np.linspace(-180, 180, P)

    r = np.zeros(P)
    for i in range(P):
        r[i] = attenuation(np.radians(theta[i]))
    plt.figure(1)
    ax1 =plt.subplot(111)
    ax1.plot(theta, r, lw = 2)
    ax1.axis([-180, 180, -20, 0])
    ax1.tick_params(labelsize=14)
    ax1.set_xlabel('Ângulo Horizontal [Graus]', fontsize=14)
    ax1.set_ylabel('Atenuação [dB]',fontsize=14)
    ax1.grid(True)
#     ax1.set_title('Diagrama de Radiação Linear')

    plt.figure(2)
    ax2 = plt.subplot(111, projection='polar')
    ax2.plot(np.radians(theta),r, label='Setor 1')
    ax2.plot(np.radians(theta+120),r, label='Setor 2')
    ax2.plot(np.radians(theta-120),r, label='Setor 3')
    ax2.set_rmin(-20)
    ax2.set_rmax(0)
    ax2.set_yticks([-20, -15, -10, -5, 0])
    ax2.tick_params(labelsize=14)
    ax2.grid(True)
    ax2.legend(bbox_to_anchor=(1.33, 0.13),fontsize=14)
#     ax2.set_title('Diagrama de Radiação Polar')

def attenuation(theta, theta3db=65, att_max=20):
    a = 12*(theta/np.radians(theta3db))**2
    return (-1)*np.min([a,att_max])


def plot_radiation(M=200, N=200, s = Site(50,Coord(100,100))):
    im = np.zeros([M,N])
    o = s.p
    for x in range(N):
        for y in range(M):
            if (s.in_or_out(Coord(x,y)) == 'in'):
                try:
                    theta = np.arctan((y-o.y)/(x-o.x))
                except ZeroDivisionError:
                    theta = np.arctan(float('Inf'))
                if ((x-o.x) >= 0):
                    if (abs(theta) <= np.radians(60)):
                        im[y][x] = attenuation(theta)
                    elif (theta > np.radians(60)):
                        im[y][x] = attenuation(theta-np.radians(120))
                    elif (theta < np.radians(-60)):
                        im[y][x] = attenuation(theta+np.radians(120))
                elif ((y-o.y)>=0):
                    im[y][x] = attenuation(theta+np.radians(60))
                else:
                    im[y][x] = attenuation(theta-np.radians(60))
            else:
                im[y][x] = attenuation(np.radians(60))

    im = im[::-1][:]
    plt.imshow(im, cmap=plt.cm.jet, interpolation='bilinear')
    plt.axis('off')
    plt.colorbar()

def path_loss(d, env='urban', fc=2000):
    # macro cell urban and suburban model
    # frequency carrie  = 2000 MHz
    if env=='urban':
        if (fc==2000):
            try:
                l = 128.1 + 36.7*np.log10(d)
            except ZeroDivisionError:
                l = 128.1 + 36.7*float('-Inf')
        elif (fc==900):
            l = 120.9 + 36.7*np.log10(d)
        else:
            print('ERRO: invalid frequency')
            exit()
    elif (env=='rural' and fc==900):
        l = 95.5 + 34.1*np.log10(d)
    else:
        print('ERRO: invalid environment')
        exit()
    return l

def rx_pwr(d, tx_pwr=43, g_tx=15, g_rx=0, mcl=70):
    pl = path_loss(d)-g_tx-g_rx
#     m = [i if (i > mcl) else mcl for i in pl]
    return tx_pwr-np.maximum(pl,mcl)


def ue_rad(w=51, h=51, c_a = Coord(25,25)):
    im = np.zeros([h, w])
    for i in range(h):
        for j in range(w):
            x = j-c_a.x
            y = i-c_a.y
            dist = (np.sqrt((x**2)+(y**2)))/100
            im[i][j] = rx_pwr(d=dist, tx_pwr=30)

    plt.imshow(im, cmap=plt.cm.jet, interpolation='bilinear')
#     plt.axis('off')
    plt.colorbar()


def plot_path_loss(d=1):
    x = np.linspace(0,d,1001)
    l1 = path_loss(x)
    l2 = path_loss(x,fc=900)
    l3 = path_loss(x,env='rural', fc=900)
    ax = x*1000
    plt.plot(ax, l1, lw=1.5,label='Urbano 2000 MHz')
    plt.plot(ax, l2, lw=1.5,label='Urbano 900 MHz')
    plt.plot(ax, l3, lw=1.5,label='Rural 900 MHz')
    plt.tick_params(labelsize=14)
    plt.xlabel('Distância [m]', fontsize=14)
    plt.ylabel('Perda de Percurso [dB]', fontsize=14)
    plt.xticks(x[::100]*1000)
    plt.grid(True)
    plt.legend(fontsize=14)


def single_cell_rx(pl_model='urban', fc=2000, n=500, mcl=70):
    im = np.zeros([n,n])
    l = n/2
    o = Coord(l,l)
    for x in range(n):
        for y in range(n):
            dx=x-o.x
            dy=y-o.y
            dist = (np.sqrt((dx**2)+(dy**2)))/1000
            try:
                theta = np.arctan(dy/dx)
            except ZeroDivisionError:
                theta = np.arctan(float('Inf'))
            if (dx >= 0) and (abs(theta) <= np.radians(90)):
                im[y][x] = attenuation(theta) + rx_pwr(d=dist, mcl=mcl)
            else:
                im[y][x] = -20 + rx_pwr(d=dist, mcl=mcl)

    im = im[::-1][:]
    plt.imshow(im, cmap=plt.cm.jet, interpolation='bilinear', extent=[-l,l,-l,l])
    plt.axis('on')
    plt.grid(True)
    plt.xlabel('Posição x [m]', fontsize=12)
    plt.ylabel('Posição y [m]', fontsize=12)
    plt.colorbar()

def single_cell_path_loss(pl_model='urban', fc=2000, n=500, mcl=70):
    im = np.zeros([n,n])
    l = n/2
    o = Coord(l,l)
    for x in range(n):
        for y in range(n):
            dx=x-o.x
            dy=y-o.y
            dist = (np.sqrt((dx**2)+(dy**2)))/1000
            try:
                theta = np.arctan(dy/dx)
            except ZeroDivisionError:
                theta = np.arctan(float('Inf'))
            if (dx >= 0) and (abs(theta) <= np.radians(90)):
                im[y][x] = path_loss(d=dist) - attenuation(theta)
            else:
                im[y][x] = path_loss(d=dist) + 20

    im = im[::-1][:]
    plt.imshow(im, cmap=plt.cm.jet, interpolation='bilinear', extent=[-l,l,-l,l])
    plt.axis('on')
    plt.grid(True)
    plt.tick_params(labelsize=14)
    plt.xlabel('Posição x [m]', fontsize=14)
    plt.ylabel('Posição y [m]', fontsize=14)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Perda de Percurso [dB]', fontsize=14)
    cbar.ax.tick_params(labelsize=14)

def cell_measure(r=250):
    s1 = Site(r)
    s2 = Site(r, Coord(750,0))
    ax1 = s1.plot(True)
    ax2 = s2.plot(True)
    ax = plt.axes()
    h = np.sqrt(3)*r*.5
    ax.vlines(0,-100,100, linestyles='dashed', lw=1)
    ax.vlines(750,-100,100, linestyles='dashed', lw=1)
    ax.vlines(-375,125,325, linestyles='dashed', lw=1)
    ax.vlines(-125,125,325, linestyles='dashed', lw=1)
    ax.vlines(375,-125,-325, linestyles='dashed', lw=1)
    ax.vlines(875,-125,-325, linestyles='dashed', lw=1)
    ax.annotate(s='', xy=(0,0), xytext=(750,0), arrowprops=dict(arrowstyle='<->', lw=1))
    ax.annotate(s='', xy=(-375,h), xytext=(-125,h), arrowprops=dict(arrowstyle='<->', lw=1))
    ax.annotate(s='', xy=(375,-h), xytext=(875,-h), arrowprops=dict(arrowstyle='<->', lw=1))
    ax.text(90,-42,'Dist. Inter ERB\n      3R', fontsize=12)
    ax.text(-320,h-42,'Raio\n  R', fontsize=12)
    ax.text(420,-h-42,'Alcance da Cel.\n         2R', fontsize=12)
    plt.xlabel('Posição x [m]', fontsize=12)
    plt.ylabel('Posição y [m]', fontsize=12)