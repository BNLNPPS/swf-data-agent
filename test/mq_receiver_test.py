#! /usr/bin/env python
#############################################

import os
import sys
from   sys import exit
import argparse
import datetime

##############################################
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
parser.add_argument("-m", "--mq", action='store_true',          help="Send messages to MQ",               default=False)
parser.add_argument("-s", "--schedule", type=str,               help='Path to the schedule (YAML)',             default='')

parser.add_argument("-f", "--factor",   type=float,             help='Time factor',                             default=1.0)
parser.add_argument("-u", "--until",    type=float,             help='The limit, if undefined: end of schedule',default=None) #  required=False, nargs='?')
parser.add_argument("-c", "--clock",    type=float,             help='Scheduler clock freq(seconds)',           default=1.0)

parser.add_argument("-d", "--destination", type=str,            help='Path to the destination folder, if empty do not output data',  default='')

parser.add_argument("-L", "--low",      type=float,             help='The "low" time limit on STF production',  default=1.0)
parser.add_argument("-H", "--high",     type=float,             help='The "high" time limit on STF production', default=2.0)

args        = parser.parse_args()
verbose     = args.verbose
mq    = args.mq

if verbose: print(f'''*** Verbose mode is set to {verbose} ***''')
if verbose: print(f'''*** MQ mode is set to {mq} ***''')

schedule    = args.schedule
destination = args.destination

factor      = args.factor
until       = args.until
clock       = args.clock

low         = args.low
high        = args.high

# ---
data_path=''
try:
    data_path=os.environ['DATA_PATH']
    if verbose: print(f'''*** The DATA_PATH is defined in the environment: {data_path}, will be added to sys.path ***''')
    sys.path.append(data_path)
except:
    if verbose: print('*** The variable DATA_PATH is undefined, will rely on PYTHONPATH and ../ ***')
    data_path = '../'
    sys.path.append(data_path)  # Add parent to path, to enable running locally (also for data)
      
if verbose:
    print(f'''*** Set the Python path: {sys.path} ***''')


# ---
# try:
#     from daq import *
#     if verbose:
#         print(f'''*** PYTHONPATH contains the daq package, will use it ***''')
# except:
#     print('*** Failed to load the daq package from PYTHONPATH, exiting...***')
#     exit(-1)

# try:
#     from comms import *
#     if verbose:
#         print(f'''*** PYTHONPATH contains the comms package, will use it ***''')
# except:
#     print('*** Failed to load the comms package from PYTHONPATH, exiting...***')
#     exit(-1)

# messenger = None




