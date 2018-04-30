#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 30/01/2018
# Version: 1.0

# Python module for NOMA communications simulations
# The channel model classes are declared here

# modules
import scipy.constants as sci
import numpy as np
from logzero import logger
import nomalib.constants as const
from nomalib.utils import Coordinate as Coord

# classes
class PathLoss:
    ''' Distance dependent propagation model '''
    def __init__(self, env=const.ENV, fc=const.FC):
        self.env = env
        self.fc = fc

    def attenuation(self, d):
        if (d == 0):
            d_db = float('-Inf')
            logger.warn('Invalid distance (d = 0.0)')
        else:
            d_db = np.log10(d)
        if (self.env=='urban' and self.fc==900):
            l = 120.9 + 36.7*d_db
        elif (self.env=='urban' and self.fc==2e3):
            l = 128.1 + 36.7*d_db
        elif (self.env=='rural' and self.fc==900):
            l = 95.5 + 34.1*d_db
        else:
            logger.error('Invalid frequency or environment')
            l = 'None'
        return l

class Noise:
    ''' Noise floor signal '''
    def __init__(self, bw=const.SB, temp=const.TEMP, noise_figure=const.NF_UE):
        self.bw = bw
        self.temp = t = sci.convert_temperature(temp,'C','K')
        self.nf = noise_figure
        self.den = 10*np.log10(t*sci.k*1e3)
        self.noise_floor = self.den + self.nf + 10*np.log10(bw)

class ShadowFading:
    ''' Shadow fading 2D map with lognormal distribution object'''
    def __init__(self, file='s1.npy', den=const.SHW_D):
        self.shw = np.load(const.DAT_PATH+file)
        self.l, self.c = self.shw.shape
        self.den = den
        self.width = w = self.c*den
        self.hight = h = self.l*den
        self.center = Coord(w/2, h/2)
    
    def get_shw(self, coord):
        ''' Return shadow level from coordinate '''
        i = int(round((self.center.y + coord.y)/self.den))
        i = i if (i >= 0) else 0
        i = i if (i < self.l) else self.l-1
        j = int(round((self.center.x + coord.x)/self.den))
        j = j if (j >= 0) else 0        
        j = j if (j < self.c) else self.l-1        
        return self.shw[i][j]
        
class ShadowFadingGenerator:
    ''' Shadow fading 2D map withlognormal distribution generator'''
    def __init__(self, mean=const.SHW_M, std=const.SHW_STD, den=const.SHW_D, r=const.R_CELL):
        self.den = d = den
        self.width = w = 16*r
        self.hight = h = 8*np.sqrt(3)*r
        self.c = Coord(w/2, h/2)
        self.mean = mean
        self.std = std
        px_w = int(round(w/d))
        px_h = int(round(h/d))
        self.shw_map = np.random.normal(size=(px_h, px_w))

    def save_shadow_map(self, file='shadow.npy'):
        ''' Save numpy array with shadow map to file'''
        np.save(const.DAT_PATH+file,self.shw_map)

    def shw_ref_generator(self, file='s0.npy', save=False):
        ''' Generate shadow fading map reference for inte-site correlation '''
        h, w = self.shw_map.shape
        s0 = np.random.normal(0,1,(h, w))
        if save:
            np.save(const.DAT_PATH+file, s0)

    def inter_site_corr(self, corr=const.R_SITE, file='s.npy' ,save=False):
        ''' Shadown fading 2D maps with fix correlation R_SHW '''
        s = np.load(const.DAT_PATH+'s0.npy')
        shw = np.sqrt(corr)*s+(1-np.sqrt(corr))*self.shw_map
        self.shw_map = shw/shw.std()
        if save:
            np.save(const.DAT_PATH+file, self.shw_map)            

    def correlation_map_generator(self, neighbour=const.NB_MAP, nb=const.NB,save=False):
        ''' Generate correlation matrix from 12 neighbours distance'''
        # 12 neighbor matrix
        n = np.array(neighbour)
        dist = np.zeros([nb,nb])
        for i in range(len(n)):
            for j in range(len(n[i])):
                for k in range(len(n)):
                    for l in range(len(n[k])):
                        d = np.sqrt((k-i)**2 + (l-j)**2)
                        dist[n[i][j]-1, n[k][l]-1] = d
        alpha = 1/20
        corr = np.exp(-alpha*dist*self.den)
        if save:
            np.save(const.DAT_PATH+'corr.npy', corr)
        return corr

    def cross_correlation(self, file='sn.npy', save=True):
        ''' Insert cross correlation on shadow map '''
        shw = np.load(const.DAT_PATH+file)
        h, w = shw.shape
        corr = np.load(const.DAT_PATH+'corr.npy')
        chk = np.linalg.cholesky(corr)
        k = len(chk)
        row_chk = chk[-1]
        chk = chk[:k-1:, :k-1:]
        chk_inv = np.linalg.inv(chk)
        for i in range(h):
            for j in range(w):
                indexes = [(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i-2,j-1), (i-2,j+1),
                            (i-1,j-2), (i-1,j+2), (i,j-2), (i-2,j), (i-2,j-2), (i-2,j+2)]
                s = []
                for index in indexes:
                    m,n = index
                    if (0<= m < h and 0<= n < w):
                        s.append(shw[m, n])
                    else:
                        s.append(0)
                s = np.array([s])
                t = np.dot(chk_inv, s.T)
                t = np.append(t, shw[i, j]).reshape(k,1)
                shw[i,j] = np.dot(row_chk, t)
        shw = shw*(self.std/shw.std())
        if save:
            np.save(const.DAT_PATH+file, shw)            

class RayleighChannel:
    ''' Flat Rayleigh Channel - Clarke and Gans Model - Smith's Method '''
    def __init__(self, speed=const.SPD, fc=const.FC_H, time=const.T_SNP, ts=const.TTI):
        self.speed = speed
        self.fc = fc
        # calculate maximum doppler frequency (fm)
        fm = speed/(sci.c/fc)
        # estimates the number of points (n) from simulation time
        df = 1/time
        nt = time/ts
        # n even number
        nh = round(((2*fm/df) + 1)/2)
        if (nh < 5):
            logger.error('Time is very short, specify a value time greater than 500 ms')
            logger.warn('See T_SNP in nomalib.constants module')
            exit()
        n = nh*2
        # df = df =2*fm/(n-1)
        t = 1/df
        # generates gaussian random array
        a = np.random.normal(size=nh)
        b = np.random.normal(size=nh)
        g = a + 1j*b
        gc = g.conj()[::-1]
        g1 = np.concatenate((gc,g),axis=0)
        # generates gaussian random array
        a = np.random.normal(size=nh)
        b = np.random.normal(size=nh)
        g = a + 1j*b
        gc = g.conj()[::-1]
        g2 = np.concatenate((gc,g),axis=0)
        # generates doppler spectrum
        f = np.linspace(-fm,fm,n)
        ft = f.copy()
        ft[0] = ft[-1] = 0
        s=1.5/(np.pi*fm*np.sqrt(1-(ft/fm)**2))
        # truncates infinite limits
        s[0]=2*s[1]-s[2]
        s[-1]=2*s[-2]-s[-3]
        # Doppler filter
        x = g1*np.sqrt(s)
        # complete axis points one point for each TTI slot
        ax = np.zeros(int((nt-n)/2))
        x = np.concatenate((ax, x, ax))
        xt = abs(np.fft.ifft(x))
        y = g2*np.sqrt(s)
        y = np.concatenate((ax, y, ax))
        yt = abs(np.fft.ifft(y))
        r = np.sqrt(abs(xt)**2+abs(yt)**2)
        pwr_h = (abs(r)**2)
        self.gain = 10*np.log10(pwr_h/pwr_h.std())
        self.f = f
        self.s = s
        self.t = np.linspace(0, time, nt)

class SpatialChannel:
    ''' Channel model class'''
    def __init__(self, s_id, env=const.ENV, fc=const.FC):
        self.s_id = s_id
        self.env = env
        self.fc = fc
        self.shadow = ShadowFading('s'+str(s_id%100)+'.npy')
        self.path_loss = PathLoss(env=env, fc=fc)
        self.noise  = Noise()

class TemporalChannel:
    ''' Channel model with temporal'''
    def __init__(self, model='rayleigh', size=(const.N_UE, const.N_BS)):
        self.model = model
        self.size = size
        self.h = []
        if (model == 'rayleigh'):
            for u in range(size[0]):
                row = []
                for c in range(size[1]):
                    row.append(RayleighChannel())
                self.h.append(row)
        elif (model == 'others_model'):
            self.h = None

# Channel Module Methods
def create_shadow_maps(n=const.N_BS):
    # Run just one time for generate arrays files
    # Set save=True for save files maps
    ShadowFadingGenerator().shw_ref_generator(save=False)
    ShadowFadingGenerator().correlation_map_generator()
    for i in range(1,n+1):
        ShadowFadingGenerator().inter_site_corr(file='s'+str(i)+'.npy', save=False)
    for i in range(1,n+1):
        ShadowFadingGenerator().cross_correlation(file='s'+str(i)+'.npy', save=False)