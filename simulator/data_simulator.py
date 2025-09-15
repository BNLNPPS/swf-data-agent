#! /usr/bin/env python

#############################################
'''
This is a driver script for the data simulator.
It initializes the DATA class and starts the data management process.
'''

import os, argparse, datetime, sys
from   sys import exit

# ---
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
parser.add_argument("-e", "--envtest",  action='store_true',    help="Test the environment variables and exit", default=False)
parser.add_argument("-t", "--tst",      action='store_true',    help="Test mode")
parser.add_argument("-s", "--scope",    type=str,               help="Rucio scope for the data", default='group.daq')
parser.add_argument("-d", "--datadir",  type=str,               help="Data folder, from which to upload data", default='/tmp')
parser.add_argument("-r", "--rse",      type=str,               help="RSE to target for upload", default='DAQ_DISK_3')


args        = parser.parse_args()
verbose     = args.verbose
envtest     = args.envtest
scope       = args.scope
datadir     = args.datadir
rse         = args.rse
tst         = args.tst

if verbose:
    print(f'''*** Verbose mode is set to {verbose} ***''')
    print(f'''*** Rucio scope is set to {scope} ***''')
    print(f'''*** Data container (folder) is set to {datadir} ***''')
    print(f'''*** RSE to target for upload is set to {rse} ***''')
# ---
DATASIM_PATH        = ''

SWF_COMMON_LIB_PATH = ''
RUCIO_COMMS_PATH    = ''

try:
    RUCIO_COMMS_PATH = os.environ['RUCIO_COMMS_PATH']
    if verbose: print(f'''*** The RUCIO_COMMS_PATH is defined in the environment: {RUCIO_COMMS_PATH}, will be added to sys.path ***''')
    sys.path.append(RUCIO_COMMS_PATH)
except KeyError:
    if verbose: print('*** The variable RUCIO_COMMS_PATH is undefined, will rely on PYTHONPATH ***')


try:
    SWF_COMMON_LIB_PATH = os.environ['SWF_COMMON_LIB_PATH']
    if verbose: print(f'''*** The SWF_COMMON_LIB_PATH is defined in the environment: {SWF_COMMON_LIB_PATH}, will be added to sys.path ***''')
    if SWF_COMMON_LIB_PATH not in sys.path: sys.path.append(SWF_COMMON_LIB_PATH)
    src_path = SWF_COMMON_LIB_PATH + '/src/swf_common_lib'
    if src_path not in sys.path:
        sys.path.append(src_path)
        if verbose: print(f'''*** Added {src_path} to sys.path ***''')
    else:
        if verbose: print(f'''*** {src_path} is already in sys.path ***''')
except:
    if verbose: print('*** The variable SWF_COMMON_LIB_PATH is undefined, will rely on PYTHONPATH ***')

try:
    DATASIM_PATH=os.environ['DATASIM_PATH']
    if verbose: print(f'''*** The DATASIM_PATH is defined in the environment: {DATASIM_PATH}, will be added to sys.path ***''')
    sys.path.append(DATASIM_PATH)
except:
    if verbose: print('*** The variable DATASIM_PATH is undefined, will rely on PYTHONPATH and ../ ***')
    DATASIM_PATH = '../'  # Add parent to path, to enable running locally (also for data)
    sys.path.append(DATASIM_PATH)

if verbose: print(f'''*** Set the Python path: {sys.path} ***''')

# ---
try:
    from data import *
    if verbose: print(f'''*** Successful import of the data package ***''')
except:
    if verbose: print('*** Failed to load the data package from PYTHONPATH, exiting...***')
    exit(-1)


from rest_logging import setup_rest_logging

if envtest:
    print('*** Environment variables have been tested, exiting... ***')
    exit(0)

# ---

data = DATA(verbose=verbose, rucio_scope=scope, data_container=datadir, rse=rse)

data.run()

exit(0)
