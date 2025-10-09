#! /usr/bin/env python
#############################################
'''
This utility is used to test the XRootD package.
Pardon the dust, comments and changes are frequent.
'''

import os, argparse, datetime, time, sys, zlib
from   datetime import datetime as dt
from   sys import exit

# Rucio imports
from rucio.client.client import Client
from rucio.client.replicaclient import ReplicaClient
from rucio.client.didclient import DIDClient
from rucio.common.exception import DataIdentifierAlreadyExists, RSENotFound
import hashlib

# ---
xrd         = 'root://dcintdoor.sdcc.bnl.gov:1094/'
scope       = 'group.daq'
filename    = '/eic/u/eicmax/testbed/swf-data-agent/test/README.md'
name        = os.path.basename(filename) # 'README.md'
rse_name    = 'DAQ_DISK_3'  # Target RSE

def calculate_file_checksum(filepath, algorithm='md5'):
    """Calculate checksum of a file"""
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# ---
def calculate_adler32_from_file(file_path, chunk_size=4096):
    """
    Calculates the Adler-32 checksum of a file.

    Args:
        filepath (str): The path to the file.
        chunk_size (int): The size of chunks to read from the file.

    Returns:
        int: The Adler-32 checksum of the file.
    """
    adler32_checksum = 1  # Initial Adler-32 value

    try:
        with open(file_path, 'rb') as f:
            # print(f"Calculating Adler-32 checksum for file: {file_path}")
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                adler32_checksum = zlib.adler32(chunk, adler32_checksum)
        return adler32_checksum & 0xffffffff  # Ensure 32-bit unsigned result
    except:
        print(f"Problem with file {file_path}")
        exit(-2)

# ---
def register_file_on_rse():
    """Register an uploaded file on RSE"""
    
    adler = calculate_adler32_from_file(filename)
    print(f"Adler32 checksum of the file {filename}: {adler}")
    
    # Initialize Rucio client
    client = Client()
    replica_client = ReplicaClient()
    did_client = DIDClient()
    
    # File and RSE information
    # scope     = 'user.johndoe'  # - Rucio scope defined globally
    # filename  = 'my_data_file.root' # defined globally
    # rse_name  = 'CERN-PROD_DATADISK'  # Target RSE defined globally
    local_file_path = filename  # Local path to the file to be registered
    
    # Physical file name (DID - Data Identifier)
    # FIXME: Use the actual filename instead of hardcoded 'f'
    name = 'f'  
    did = {
        'scope':    scope,
        'name':     name
    }
    
    try:
        # Step 1: Get file metadata
        file_size = os.path.getsize(local_file_path)
        file_checksum = calculate_file_checksum(local_file_path, 'md5')
        
        print(f"File: {filename}")
        print(f"Size: {file_size} bytes")
        print(f"MD5: {file_checksum}")

      
        # Step 2: Check if DID already exists
        try:
            existing_did = did_client.get_did(scope, name)
            print(f"DID already exists: {existing_did}")
        except:
            # DID doesn't exist, we'll create it
            print("DID doesn't exist yet, will create new one")
        
        # Step 3: Create the replica info
        replica_info = {
            'scope': scope,
            'name': name,
            'rse': rse_name,
            'size': file_size,
            'md5': file_checksum,
            'pfn': f'root://dcintdoor.sdcc.bnl.gov:1094//pnfs/sdcc.bnl.gov/eic/epic/disk/swfdaqtest/potekhintest/dir1/f',  # Physical file name/path
            'meta': {
                'events': 10,  # Custom metadata
                'dataset': 'swf.100113.run'
            }
        }
        
        # Register the replica
        replica_client.add_replica(
            rse=rse_name,
            scope=scope,
            name=name,
            bytes_=file_size,
            adler32=f'{adler:x}',
            pfn = f'root://dcintdoor.sdcc.bnl.gov:1094/pnfs/sdcc.bnl.gov/eic/epic/disk/swfdaqtest/potekhintest/dir1/f'
            )
        
        print(f"✓ Replica registered on RSE: {rse_name}")
        
        # # Step 4: Create/update the DID entry
        # try:
        #     did_client.add_did(
        #         scope=scope,
        #         name=filename,
        #         type='FILE',
        #         statuses=None,
        #         meta={
        #             'project': 'physics_analysis',
        #             'run_number': '12345',
        #             'events': 1000000
        #         },
        #         rules=None,
        #         lifetime=None,
        #         dids=None,
        #         rse=rse_name
        #     )
        #     print(f"✓ DID created: {scope}:{filename}")
            
        # except DataIdentifierAlreadyExists:
        #     print(f"DID already exists: {scope}:{filename}")
        #     # Update metadata if needed
        #     did_client.set_metadata(
        #         scope=scope,
        #         name=filename,
        #         key='updated_at',
        #         value=str(int(time.time()))
        #     )
        
        # # Step 5: Verify the registration
        # replicas = list(replica_client.list_replicas([did]))
        # for replica in replicas:
        #     print(f"✓ Verified replica: {replica}")
        #     for rse, pfns in replica['rses'].items():
        #         print(f"  RSE: {rse}")
        #         for pfn in pfns:
        #             print(f"  PFN: {pfn}")
        
        # # Step 6: Optional - Create replication rule
        # from rucio.client.ruleclient import RuleClient
        # rule_client = RuleClient()
        
        # # Create a rule to ensure the file is replicated to specific RSEs
        # rule_id = rule_client.add_replication_rule(
        #     dids=[did],
        #     copies=1,
        #     rse_expression=rse_name,
        #     weight=None,
        #     lifetime=None,
        #     grouping='DATASET',
        #     account='johndoe',
        #     locked=False,
        #     notify='N',
        #     ignore_availability=False,
        #     comment='Manual file registration'
        # )
        
        # print(f"✓ Replication rule created: {rule_id[0]}")
        
        return True
        
    except RSENotFound:
        print(f"✗ Error: RSE '{rse_name}' not found")
        return False
    except Exception as e:
        print(f"✗ Error registering file: {str(e)}")
        return False


# main
# ---
parser      = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")

args        = parser.parse_args()
verbose     = args.verbose

print(f'*** Verbose mode is set to {verbose} ***')

from XRootD import client

fs = client.FileSystem(xrd)

# This also works in the origin URI, as prefix -- file://

# Register single file
print("\n1. Registering single file...")
register_file_on_rse()

#status = fs.copy(filename, 'root://dcintdoor.sdcc.bnl.gov:1094//pnfs/sdcc.bnl.gov/eic/epic/disk/swfdaqtest/potekhintest/dir1/f', force=False)
#print(status)


exit(0)

# ATTIC
# NB. This code below works, kept for reference
# ---
# fs.mkdir('/pnfs/sdcc.bnl.gov/eic/epic/disk/swfdaqtest/potekhintest/dir1')
# status, entries = fs.dirlist("/pnfs/sdcc.bnl.gov/eic/epic/disk/swfdaqtest")

# if status.ok:
#     for entry in entries:
#         print(f"Name: {entry}")
# else:
#     print(f"Error listing directory: {status.message}")

# CLI options for later:
# parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
# parser.add_argument("-r", "--rse",      type=str,               help="RSE", default='BNL_PROD_DISK_1')
# parser.add_argument("-d", "--did",      type=str,               help="target DID", default='')

# parser.add_argument("-D", "--dataset",  type=str,               help="Dataset name, if one is to be created", default=None)
# parser.add_argument("-L", "--lifetime", type=int,               help="Dataset lifetime", default=1000)
# parser.add_argument("-M", "--metadata", action='store_true',    help="Get metadata of the dataset", default=False)

# parser.add_argument("-l", "--lfn",      type=str,               help="lfn", default=None)

# parser.add_argument("-p", "--path",     type=str,               help="path to source file, for upload", default='')
# parser.add_argument("-s", "--scope",    type=str,               help="scope", default='user.potekhin')

# # ---
# args        = parser.parse_args()
# rse         = args.rse
# did         = args.did

# dataset     = args.dataset
# metadata    = args.metadata
# lifetime    = args.lifetime
# lfn         = args.lfn

# path        = args.path
# scope       = args.scope