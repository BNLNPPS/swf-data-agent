#! /usr/bin/env python
#############################################
'''
This utility is used to test the rucio_comms package.
It allows for creating datasets, uploading files, and managing metadata.
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


if dataset is not None:
    print(f'*** Dataset operation requested: {dataset} ***')
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

# ---
try:
    from rucio_comms import *
    if verbose: print(f'''*** Successfully imported classes from rucio_comms ***''')
except:
    print('*** Failed to import the classes from rucio_comms, exiting...***')
    exit(-1)


# Client will be needed for any operation with Rucio
if verbose: print(f'''*** Instantiating the RucioClient ***''')
try:
    client = RucioClient()
    if verbose: print(f'''*** Successfully instantiated the RucioClient ***''')
except Exception as e:
    print(f'*** Failed to instantiate the RucioClient: {e}, exiting... ***')
    exit(-1)

# ---
if lfn is not None: # Attach file to the open dataset
    if verbose: print(f'''*** Adding a file with lfn: {lfn} to the scope/dataset: {scope}:{dataset} ***''')
    file_manager    = FileManager(rucio_client = client)
    # Register the file replica, using the lfn
    attachment_success = file_manager.add_files_to_dataset([f'''{scope}:{lfn}'''], f'''{scope}:{dataset}''')
    if verbose: print(f"*** File attached to dataset: {attachment_success} ***")

    exit(0)

# ---
if dataset:
    if metadata:
        if verbose: print(f'''*** Attempting to fetch the metadata for scope/dataset: {scope}:{dataset} ***''')
        dataset_manager = DatasetManager()
        meta = dataset_manager.get_dataset_metadata(f'''{scope}:{dataset}''')
        if meta:
            print(f'*** Metadata for the dataset {scope}:{dataset}: {meta} ***')
        else:
            print(f'*** Failed to get metadata for the dataset {scope}:{dataset}, exiting... ***')
            exit(-1)

        exit(0)

    # Create a new dataset
    if verbose: print(f'''*** Creating a new dataset with name: {scope}:{dataset} ***''')
    
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

################## ATTIC ##########################
# Attaching files to a dataset
# ---
    # try:
    #     metadata = client.get_metadata(scope, lfn) # may need metadata to register the file, keep for later
    # except:
    #     pass
    
    # e.g. print(metadata['bytes'], metadata['adler32'], metadata['md5'], metadata['created_at'])
    # if verbose: print(f'''*** Metadata for the file {scope}:{lfn}: {metadata} ***''')
  

    # Alternatively, we can use the FileInfo class to create a file info object
    # file_info       = FileInfo(
    #     lfn=lfn,
    #     pfn="root://test.com:1094/testpath/testdir/t1.txt", # not used
    #     size=metadata['bytes'],
    #     checksum="ad:"+metadata['adler32'],
    #     scope=scope
    # )
    # Alternatively, we can use the add_files_to_dataset method with FileInfo objects
    # attachment_success = file_manager.add_files_to_dataset([file_info], f'''{scope}:{dataset}''')