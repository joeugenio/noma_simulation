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

from scipy.constants import k as btz_k
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
    def __init__(self, bw=const.BW, d_den=const.N_DEN):
        
        print(btz_k)


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

class FastFading:
    ''' Fast Fading model - Rayleigh fading '''
    pass

class Interference:
    ''' Interference from others cells '''
    pass

class Channel:
    ''' Channel model class'''
    def __init__(self, s_id, env=const.ENV, fc=const.FC):
        self.s_id = s_id
        self.env = env
        self.fc = fc
        self.path_loss = PathLoss(env=env, fc=fc)
        self.shadow = ShadowFading('s'+str(s_id%100)+'.npy')
        # self.noise  = Noise()