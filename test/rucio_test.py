#! /usr/bin/env python
#############################################
'''
This utility is used to test the rucio_comms package.
WORK IN PROGRESS!
'''

import os, argparse, datetime, time, sys
from   datetime import datetime as dt
from   sys import exit

# ---

def func(to_print):
    print(to_print) # a simple function to process received messages
# ---
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
parser.add_argument("-s", "--send",     action='store_true',    help="Send mode")
parser.add_argument("-r", "--receive",  action='store_true',    help="Receive mode")
parser.add_argument("-m", "--message",  type=str,               help="Test message", default='test')
parser.add_argument("-n", "--number",   type=int,               help="How many times to send", default=1)

# ---
args        = parser.parse_args()
send        = args.send
receive     = args.receive
message     = args.message
number      = args.number
verbose     = args.verbose

print(f'*** Verbose mode is set to {verbose} ***')

# ---
rucio_comms_path=''
try:
    rucio_comms_path = os.environ['RUCIO_COMMS_PATH']
    if verbose: print(f'''*** The rucio_comms_path is defined in the environment: {rucio_comms_path}, will be added to sys.path ***''')
    sys.path.append(rucio_comms_path)
except KeyError:
    if verbose: print('*** The variable RUCIO_COMMS_PATH is undefined, will rely on PYTHONPATH ***')

if verbose:
    print(f'''*** Set the Python path: {sys.path} ***''')


try:
    from rucio_comms import *
    if verbose: print(f'''*** Successfully imported classes from rucio_comms ***''')
except:
    print('*** Failed to import the classes from rucio_comms, exiting...***')
    exit(-1)


print("work in progress, nothing to do yet")

exit(0)

