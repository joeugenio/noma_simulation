#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 07/05/2018
# Version: 1.0

# Main Python Script for NOMA communications simulations

import nomalib.channel as ch
import nomalib.plots as plt
import nomalib.simulator as sim
import logzero
from logzero import logger
import numpy as np

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/run.log', mode='w', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

# create simulation
s = sim.Simulator(n_snap=1)
# create scenario
s.scenario_generator()

# ==========================================================================
# PLOT AREA
# ==========================================================================
# logger.info('Plotting Link Level Performance Model')
# plt.plot_l2s(sh=True)

# logger.info('Plotting grid scenario')
# plt.plot_grid(s.grid, save=True, filename='grid_scen', cells=True)

# logger.info('Plotting grid scenario')
# logger.info('Deploing users equipments on grid')
# s.grid.deploy_user_equipments(n_ue=57*10)
# logger.info('Connecting UE to best BS')
# s.grid.connect_all_ue(n_ue=10)
# plt.plot_grid(s.grid, sh=True, save=False, ue=True, connect=True)

# c = ch.TemporalChannel()
# logger.info('Plotting  Doppler Filter PSD')
# plt.plot_doppler_filter(c.h[0][0], save=True)
# logger.info('Plotting  Rayleigh Channel Gain')
# plt.plot_channel_gain(c.h[0][0], save=True)

# logger.info('Plotting attenuation figures')
# plt.plot_cell_attenuation(s.grid.sites[9], sh=False, save=True)
# plt.plot_cell_attenuation(s.grid.sites[9], save=True, filename='cell_att_half_shw', shw_level=0.5)
# plt.plot_cell_attenuation(s.grid.sites[9], save=True, filename='cell_att_no_shw', shw_level=0)
# plt.plot_bs_attenuation(s.grid.sites[9], sh=True)
# s.grid.deploy_user_equipment(region='hexagon')
# s.grid.connect_all_ue()
# plt.plot_ue_attenuation(s.grid.user_equipments[0], s.grid.sites[0].channel, save=True)
# plt.plot_ue_attenuation(s.grid.user_equipments[0], s.grid.sites[0].channel, filename='ue_att_half_shw', save=True, shw_level=.5)
# plt.plot_ue_attenuation(s.grid.user_equipments[0], s.grid.sites[0].channel, filename='ue_att_no_shw', save=True, shw_level=0)

# logger.info('Plotting path loss')
# plt.plot_path_loss(save=True)

# logger.info('Plotting radiation pattern')
# antenna = s.grid.sites[0].cells[0].antenna
# plt.plot_pattern(antenna, save=True)
# plt.plot_polar_pattern(antenna, save=True)

# logger.info('Plotting Grid measures')
# plt.plot_measure(s.grid, save=True)

# logger.info('Plot shadow fading map')
# plt.plot_shadow(input='s0.npy', save=True, filename='shadow_uncorr')
# plt.plot_shadow(input='s9.npy', sh=True)
# plt.plot_shadow_zoom(input='s9.npy', sh=True)
# ==========================================================================