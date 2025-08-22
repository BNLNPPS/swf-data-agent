#! /usr/bin/env python

#############################################

import os, argparse, datetime, sys
from   sys import exit

# ---

def func(to_print):
    print(to_print) # a simple function to process received messages


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
parser.add_argument("-e", "--envtest",  action='store_true',    help="Test the environment variables and exit", default=False)

parser.add_argument("-S", "--send",     action='store_true',    help="Send messages to MQ",                     default=False)
parser.add_argument("-R", "--receive",  action='store_true',    help="Receive messages from MQ",                default=False)


args        = parser.parse_args()
verbose     = args.verbose
envtest     = args.envtest

send        = args.send
receive     = args.receive

if verbose:
    print(f'''*** Verbose mode is set to {verbose} ***''')
    print(f'''*** Send mode is set to {send}, receive more set to {receive} ***''')

# ---
DATASIM_PATH        = ''
MQ_COMMS_PATH       = ''
SWF_COMMON_LIB_PATH = ''

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


try:
    MQ_COMMS_PATH = os.environ['MQ_COMMS_PATH']
    if verbose: print(f'''*** The MQ_COMMS_PATH is defined in the environment: {MQ_COMMS_PATH}, will be added to sys.path ***''')
    if MQ_COMMS_PATH not in sys.path: sys.path.append(MQ_COMMS_PATH)
except:
    if verbose: print('*** The variable MQ_COMMS_PATH is undefined, will rely on PYTHONPATH ***')

if verbose:
    print(f'''*** Set the Python path: {sys.path} ***''')

# ---
try:
    from data import *
    if verbose:
        print(f'''*** PYTHONPATH contains the data package, will use it ***''')
except:
    print('*** Failed to load the data package from PYTHONPATH, exiting...***')
    exit(-1)


from rest_logging import setup_rest_logging

if envtest:
    print('*** Environment variables have been tested, exiting... ***')
    exit(0) 

sndr = None
rcvr = None

if send:
    try:
        from mq_comms import Sender
        if verbose: print(f'''*** Successfuly imported the Sender from mq_comms ***''')
    except:
        print('*** Failed to import the Sender from mq_comms, exiting...***')
        exit(-1)

    try:
        sndr = Sender(verbose=verbose)
        if verbose: print(f'''*** Successfully instantiated the Sender ***''')
        sndr.connect()
        if verbose: print(f'''*** Successfully connected the Sender to MQ ***''')
    except:
        print('*** Failed to instantiate the Sender, exiting...***')
        exit(-1)


if receive:
    try:
        from mq_comms import Receiver
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
