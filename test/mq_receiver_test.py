#! /usr/bin/env python

#############################################

import os, argparse, datetime, time, sys
from   sys import exit

# ---

def func(to_print):
    print(to_print) # a simple function to process received messages
# ---
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")

args        = parser.parse_args()
verbose     = args.verbose

if verbose: print(f'''*** Verbose mode is set to {verbose} ***''')

# ---
daqsim_path=''

try:
    daqsim_path=os.environ['DAQSIM_PATH']
    if verbose: print(f'''*** The DAQSIM_PATH is defined in the environment: {daqsim_path}, will be added to sys.path ***''')
    sys.path.append(daqsim_path)
except:
    if verbose: print('*** The variable DAQSIM_PATH is undefined, will rely on PYTHONPATH and ../ ***')
    daqsim_path = '../'
    sys.path.append(daqsim_path)  # Add parent to path, to enable running locally (also for data)
      
if verbose:
    print(f'''*** Set the Python path: {sys.path} ***''')

# ---
try:
    from daq import *
    if verbose:
        print(f'''*** PYTHONPATH contains the daq package, will use it ***''')
except:
    print('*** Failed to load the daq package from PYTHONPATH, exiting...***')
    exit(-1)


rcvr = None

try:
    from comms import Receiver
    if verbose: print(f'''*** Successfully imported the Receiver from comms ***''')
except:
    print('*** Failed to import the Receiver from comms, exiting...***')
    exit(-1)


try:
    rcvr = Receiver(verbose=verbose, processor=func) # a function to process received messages
    rcvr.connect()
    if verbose: print(f'''*** Successfully instantiated and connected the Receiver, will receive messages from MQ ***''')
except:
    print('*** Failed to instantiate the Receiver, exiting...***')
    exit(-1)

# ---

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting…")
    rcvr.disconnect()

print('---')

exit(0)

