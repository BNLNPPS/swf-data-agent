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
parser.add_argument("-r", "--rse",      type=str,               help="RSE", default='BNL_PROD_DISK_1')
parser.add_argument("-d", "--did",      type=str,               help="target DID", default='')
parser.add_argument("-p", "--path",     type=str,               help="path to source file", default='')
parser.add_argument("-s", "--scope",    type=str,               help="scope", default='user.potekhin')
# ---
args        = parser.parse_args()
rse         = args.rse
did         = args.did
path        = args.path
scope       = args.scope
verbose     = args.verbose

print(f'*** Verbose mode is set to {verbose} ***')

if did == '':
    print('*** No DID specified, exiting... ***')
    exit(-1)

if path == '':
    print('*** No path specified, exiting... ***')
    exit(-1)

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


client          = Client()
upload_client   = UploadClient(client)

upload_spec = {
    'path':         path,
    'rse':          rse,
    'did_scope':    scope,
    'did_name':     did,
}

try:
    result = upload_client.upload([upload_spec])
except Exception as e:
    print(f'*** Exception during upload: {e} ***')
    exit(-1)

if result == 0:
    print("File uploaded successfully!")
else:
    print("File upload failed.")


exit(0)

