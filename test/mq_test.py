#! /usr/bin/env python
#############################################
'''
This utility is used to test the mq_comms package.
It can be used to send or receive messages.
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


if not send and not receive:
    print('*** Please specify either -s/--send or -r/--receive ***')
    exit(-1)

if send and receive:
    print('*** Please specify either -s/--send or -r/--receive, not both ***')
    exit(-1)

if verbose:
    print(f'''*** Verbose mode is set to {verbose} ***''')
    if send:    print('*** Send mode is set ***')
    if receive: print('*** Receive mode is set ***')    

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
    from mq_comms import *
    if verbose: print(f'''*** Successfully imported classes from mq_comms ***''')
except:
    print('*** Failed to import the classes from mq_comms, exiting...***')
    exit(-1)

# ---
if send:
    try:
        sender = Sender(verbose=verbose)  # instantiate the Sender
        if verbose: print(f'''*** Successfully instantiated the Sender ***''')
    except:
        print('*** Failed to instantiate the Sender, exiting...***')
        exit(-1)

    try:
        sender.connect()  # connect to MQ
        if verbose: print(f'''*** Successfully connected the Sender to MQ ***''')
    except:
        print('*** Failed to connect the Sender, exiting...***')
        exit(-1)

    # ---
    cnt = 0
    while cnt < number:
        cnt += 1
        if verbose: print(f'''*** Sending message {cnt} of {number} ***''')
        try:
            ts = dt.now().strftime("%Y%m%d%H%M%S")
            to_send = f'{ts} {message}'
            if verbose: print(f'''*** Sending the message: {to_send} ***''')
            # Send the message to the 'epictopic' topic
            sender.send(destination='epictopic', body=to_send, headers={'persistent': 'true'})
            if verbose: print(f'''*** Successfully sent the message: {to_send} ***''')
        except:
            print('*** Failed to send the message, exiting...***')
            exit(-1)

# ---
if receive:
    try:
        rcvr = Receiver(verbose=verbose, processor=func) # a function to process received messages
        rcvr.connect()
        if verbose: print(f'''*** Successfully instantiated and connected the Receiver, will receive messages from MQ ***''')
    except:
        print('*** Failed to instantiate the Receiver, exiting...***')
        exit(-1)

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting…")
        rcvr.disconnect()

if verbose:
    print(f'''*** Exiting the script after processing ***''')
    if send:    print('*** Send mode completed ***')
    if receive: print('*** Receive mode completed ***')

exit(0)

