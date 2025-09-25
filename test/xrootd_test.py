#! /usr/bin/env python
#############################################
'''
This utility is used to test the XRootD package.
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

parser.add_argument("-D", "--dataset",  type=str,               help="Dataset name, if one is to be created", default=None)
parser.add_argument("-L", "--lifetime", type=int,               help="Dataset lifetime", default=1000)
parser.add_argument("-M", "--metadata", action='store_true',    help="Get metadata of the dataset", default=False)

parser.add_argument("-l", "--lfn",      type=str,               help="lfn", default=None)

parser.add_argument("-p", "--path",     type=str,               help="path to source file, for upload", default='')
parser.add_argument("-s", "--scope",    type=str,               help="scope", default='user.potekhin')

# ---
args        = parser.parse_args()
rse         = args.rse
did         = args.did

dataset     = args.dataset
metadata    = args.metadata
lifetime    = args.lifetime
lfn         = args.lfn

path        = args.path
scope       = args.scope
verbose     = args.verbose

print(f'*** Verbose mode is set to {verbose} ***')


from XRootD import client

myclient = client.FileSystem('root://dcintdoor.sdcc.bnl.gov:1094/')
status = myclient.copy('/eic/u/eicmax/testbed/swf-data-agent/test/README.md', '/pnfs/sdcc.bnl.gov/eic/epic/disk/swfdaqtest/', force=True)
print(status)

exit(0)

