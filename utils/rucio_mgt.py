#! /usr/bin/env python
#############################################

'''
This utility is used for managing Rucio items.
'''

import os, argparse, datetime, time, sys, json
from   datetime import datetime as dt
from   sys import exit

# ---
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")

parser.add_argument("-r", "--rse",      type=str,               help="RSE",                 default='BNL_PROD_DISK_1')
parser.add_argument("-d", "--did",      type=str,               help="target DID",          default=None)

parser.add_argument("-D", "--dataset",  type=str,               help="Dataset name",        default=None)
parser.add_argument("-L", "--lifetime", type=int,               help="Dataset lifetime",    default=None)

parser.add_argument("-J", "--kv",       type=str,               help="Keys/Values to set",        default=None)

parser.add_argument("-G", "--getmetadata", action='store_true', help="Get metadata", default=False)
parser.add_argument("-S", "--setmetadata", action='store_true', help="Set metadata", default=False)

parser.add_argument("-l", "--lfn",      type=str,               help="lfn", default=None)

parser.add_argument("-p", "--path",     type=str,               help="path to source file, for upload", default='')
parser.add_argument("-s", "--scope",    type=str,               help="scope", default='group.daq')

# ---
args        = parser.parse_args()
rse         = args.rse
did         = args.did

dataset     = args.dataset

getmetadata = args.getmetadata
setmetadata = args.setmetadata
kv          = args.kv

lifetime    = args.lifetime
lfn         = args.lfn

path        = args.path
scope       = args.scope
verbose     = args.verbose

if verbose: print(f'*** Verbose mode is set to {verbose} ***')

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


from rucio.client.didclient import DIDClient

# Initialize the DIDClient
did_client = DIDClient()


if dataset:
    if verbose: print(f'*** Dataset operation requested: {dataset} ***')
    if getmetadata:
        if verbose: print(f'''*** Attempting to fetch the metadata for scope/dataset: {scope}:{dataset} ***''')
        dataset_manager = DatasetManager()
        meta = dataset_manager.get_dataset_metadata(f'''{scope}:{dataset}''')
        if meta:
            if verbose:
                print(f'*** Metadata for the dataset {scope}:{dataset}: ***')
                sorted_dict = dict(sorted(meta.items()))
                # print(sorted_dict)
                for k, v in sorted_dict.items():
                    print(f"{k:<15}{v}")
                    # print(f'    {k}: {v}')
                
        else:
            if verbose: print(f'*** Failed to get metadata for the dataset {scope}:{dataset}, exiting... ***')
            exit(-1)
        exit(0)
    elif setmetadata:
        if kv is None:
            print('*** No key/value pairs provided for setting metadata, exiting... ***')
            exit(-1)
        try:
            kv_dict = json.loads(kv)
        except json.JSONDecodeError as e:
            print(f'*** Failed to parse the key/value pairs: {e}, exiting... ***')
            exit(-1)

        if verbose: print(f'''*** Setting the metadata for scope/dataset: {scope}:{dataset} to {kv_dict} ***''')
        for k, v in kv_dict.items():
            if verbose: print(f'''*** Setting the metadata key: {k} to value: {v} ***''')
            did_client.set_metadata(scope=scope, name=dataset, key=k, value=v)
        exit(0)
    elif lifetime:
        if verbose: print(f'''*** Setting the lifetime for scope/dataset: {scope}:{dataset} to {lifetime} days ***''')
        did_client.set_metadata(scope=scope, name=dataset, key='lifetime', value=lifetime)
        exit(0)

else:
    if did:
        if verbose: print(f'*** DID operation requested: {did} ***')
        if getmetadata:
            if verbose: print(f'''*** Attempting to fetch the metadata for scope/did: {scope}:{did} ***''')
            try:
                meta = did_client.get_metadata(scope=scope, name=did)
            except Exception as e:
                print(f'*** Failed to get metadata for the DID {scope}:{did}: {e}, exiting... ***')
                exit(-1)

            if meta:
                if verbose:
                    print(f'*** Metadata for the DID {scope}:{did}: ***')
                    sorted_dict = dict(sorted(meta.items()))
                    # print(sorted_dict)
                    for k, v in sorted_dict.items():
                        print(f"{k:<15}{v}")
                        # print(f'    {k}: {v}')
                    
            else:
                if verbose: print(f'*** No metadata found for the DID {scope}:{did}, exiting... ***')
                exit(-1)
            exit(0)
        elif setmetadata:
            if kv is None:
                print('*** No key/value pairs provided for setting metadata, exiting... ***')
                exit(-1)
            try:
                kv_dict = json.loads(kv)
            except json.JSONDecodeError as e:
                print(f'*** Failed to parse the key/value pairs: {e}, exiting... ***')
                exit(-1)

            if verbose: print(f'''*** Setting the metadata for scope/did: {scope}:{did} to {kv_dict} ***''')
            for k, v in kv_dict.items():
                if verbose: print(f'''*** Setting the metadata key: {k} to value: {v} ***''')
                did_client.set_metadata(scope=scope, name=did, key=k, value=v)
            exit(0)
        else:
            print('*** No operation specified for the DID, exiting... ***')
        exit(0)

    if path == '':
        print('*** No path specified, exiting... ***')
        exit(-1)

#for did in did_client.list_dids(scope=scope, filters={'type': 'FILE'}):
#    print(did)


exit(0)

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