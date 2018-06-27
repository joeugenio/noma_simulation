#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 07/05/2018
# Last update: 08/05/2018
# Version: 0.1

# Main Python Script for NOMA communications simulations
# Case study with 2 users per cell

import nomalib.simulator as sim
import logzero
from logzero import logger
import __main__ as main

# set file name for logs and outputs files
file_name = main.__file__[2:-3:]

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/'+file_name+'.log', mode='a', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

# create simulation
#s = sim.Simulator(n_ue_cell=10, coeff_pwr=0.8, coeff_bw=0.8, thr_target=80e6, n_cdf_arg=2, filename=file_name)
s = sim.Simulator(n_ue_cell=10, n_snap=1, filename=file_name)
# create scenario
s.scenario_generator()
# run simulator
s.run()