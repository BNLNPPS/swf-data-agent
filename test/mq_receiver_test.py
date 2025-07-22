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
mq_comms_path=''


try:
    mq_comms_path = os.environ['MQ_COMMS_PATH']
    if verbose: print(f'''*** The mq_comms_path is defined in the environment: {mq_comms_path}, will be added to sys.path ***''')
    sys.path.append(mq_comms_path)
except:
    if verbose: print('*** The variable MQ_COMMS_PATH is undefined, will rely on PYTHONPATH and ../ ***')
    mq_comms_path = '../'
    sys.path.append(mq_comms_path)  # Add parent to path, to enable running locally (also for data)
      
if verbose:
    print(f'''*** Set the Python path: {sys.path} ***''')

rcvr = None

try:
    from mq_comms import Receiver
    if verbose: print(f'''*** Successfully imported the Receiver from mq_comms ***''')
except:
    print('*** Failed to import the Receiver from mq_comms, exiting...***')
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

