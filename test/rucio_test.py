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

parser.add_argument("-D", "--dataset",  type=str,               help="Dataset name, if one is to be created", default=None)
parser.add_argument("-L", "--lifetime", type=int,               help="Dataset lifetime", default=1000)
parser.add_argument("-l", "--lfn",      type=str,               help="lfn", default=None)


parser.add_argument("-p", "--path",     type=str,               help="path to source file", default='')
parser.add_argument("-s", "--scope",    type=str,               help="scope", default='user.potekhin')
# ---
args        = parser.parse_args()
rse         = args.rse
did         = args.did

dataset     = args.dataset
lifetime    = args.lifetime
lfn         = args.lfn

path        = args.path
scope       = args.scope
verbose     = args.verbose

print(f'*** Verbose mode is set to {verbose} ***')


if dataset is not None:
    print(f'*** Dataset creation requested: {dataset} ***')
else:
    if did == '':
        print('*** No DID specified, exiting... ***')
        exit(-1)

    if path == '':
        print('*** No path specified, exiting... ***')
        exit(-1)


###################################################################
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




if lfn is None:
    # Attach file to the open dataset

    file_manager = FileManager()

    file_info = FileInfo(
        lfn=lfn,
        pfn="root://test.com:1094/testpath/testdir/t1.txt",
        size=2,
        checksum="ad:006e003c",
        scope=scope
    )

    # Register the file replica
    attachment_success = file_manager.add_files_to_dataset([file_info], f'''{scope}:{dataset}''')
    print(f"File attached to dataset: {attachment_success}")

    exit(0)




if dataset:
    dataset_manager = DatasetManager()
    result = dataset_manager.create_dataset(dataset_name=f'''{scope}:{dataset}''', lifetime_days=lifetime, open_dataset=True)
    if verbose:
        print(f'''*** Dataset creation result: {result} ***''')
    if not result:
        print('*** Dataset creation failed, exiting... ***')
        exit(-1)
    else:
        print(f'*** Dataset {result["scope"]}:{result["name"]} created successfully with DUID: {result["duid"]} ***')

    exit(0)

client          = RucioClient()
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

