# Testing communications

## About 

This folder contains testing utilities, used in preparation of the full-fledged
agents, and contains two sections:
* MQ Communications
* Rucio Communitcations

## Rucio

An example of Rucio interaction, utilizing the *rucio_test* script:

```bash
#  file upload
./test/rucio_test.py -v -p ~/tst.txt -d tst2.txt -r BNL_PROD_DISK_1 -s group.daq -l tst

# attach a file to a dataset
./test/rucio_test.py -v -D swf1 -r BNL_PROD_DISK_1 -s group.daq -l tst3.txt

# obtain metadata
./test/rucio_test.py -v -M -s group.daq -D swf1

```

## Python API

An example: registration of an uploaded file.

```python
#!/usr/bin/env python3
"""
Example: Register an uploaded file on RSE using Rucio Python client
"""

from rucio.client.client import Client
from rucio.client.replicaclient import ReplicaClient
from rucio.client.didclient import DIDClient
from rucio.common.exception import DataIdentifierAlreadyExists, RSENotFound
import hashlib
import os

def calculate_file_checksum(filepath, algorithm='md5'):
    """Calculate checksum of a file"""
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def register_file_on_rse():
    """Register an uploaded file on RSE"""
    
    # Initialize Rucio client
    client = Client()
    replica_client = ReplicaClient()
    did_client = DIDClient()
    
    # File and RSE information
    scope = 'user.johndoe'  # Your Rucio scope
    filename = 'my_data_file.root'
    rse_name = 'CERN-PROD_DATADISK'  # Target RSE
    local_file_path = '/path/to/local/file.root'
    
    # Physical file name (DID - Data Identifier)
    did = {
        'scope': scope,
        'name': filename
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
            existing_did = did_client.get_did(scope, filename)
            print(f"DID already exists: {existing_did}")
        except:
            # DID doesn't exist, we'll create it
            print("DID doesn't exist yet, will create new one")
        
        # Step 3: Register the replica (the actual file location)
        replica_info = {
            'scope': scope,
            'name': filename,
            'rse': rse_name,
            'bytes': file_size,
            'md5': file_checksum,
            'pfn': f'root://eosuser.cern.ch//eos/user/j/johndoe/{filename}',  # Physical file name/path
            'meta': {
                'events': 1000000,  # Custom metadata
                'dataset': 'mc16_13TeV'
            }
        }
        
        # Register the replica
        replica_client.add_replica(
            rse=rse_name,
            scope=scope,
            name=filename,
            bytes=file_size,
            checksum={'md5': file_checksum},
            pfn=replica_info['pfn'],
            meta=replica_info.get('meta', {})
        )
        
        print(f"✓ Replica registered on RSE: {rse_name}")
        
        # Step 4: Create/update the DID entry
        try:
            did_client.add_did(
                scope=scope,
                name=filename,
                type='FILE',
                statuses=None,
                meta={
                    'project': 'physics_analysis',
                    'run_number': '12345',
                    'events': 1000000
                },
                rules=None,
                lifetime=None,
                dids=None,
                rse=rse_name
            )
            print(f"✓ DID created: {scope}:{filename}")
            
        except DataIdentifierAlreadyExists:
            print(f"DID already exists: {scope}:{filename}")
            # Update metadata if needed
            did_client.set_metadata(
                scope=scope,
                name=filename,
                key='updated_at',
                value=str(int(time.time()))
            )
        
        # Step 5: Verify the registration
        replicas = list(replica_client.list_replicas([did]))
        for replica in replicas:
            print(f"✓ Verified replica: {replica}")
            for rse, pfns in replica['rses'].items():
                print(f"  RSE: {rse}")
                for pfn in pfns:
                    print(f"  PFN: {pfn}")
        
        # Step 6: Optional - Create replication rule
        from rucio.client.ruleclient import RuleClient
        rule_client = RuleClient()
        
        # Create a rule to ensure the file is replicated to specific RSEs
        rule_id = rule_client.add_replication_rule(
            dids=[did],
            copies=1,
            rse_expression=rse_name,
            weight=None,
            lifetime=None,
            grouping='DATASET',
            account='johndoe',
            locked=False,
            notify='N',
            ignore_availability=False,
            comment='Manual file registration'
        )
        
        print(f"✓ Replication rule created: {rule_id[0]}")
        
        return True
        
    except RSENotFound:
        print(f"✗ Error: RSE '{rse_name}' not found")
        return False
    except Exception as e:
        print(f"✗ Error registering file: {str(e)}")
        return False

def register_multiple_files():
    """Register multiple files in batch"""
    
    replica_client = ReplicaClient()
    
    files_to_register = [
        {
            'scope': 'user.johndoe',
            'name': 'file1.root',
            'rse': 'CERN-PROD_DATADISK',
            'bytes': 1024000,
            'md5': 'abc123...',
            'pfn': 'root://eosuser.cern.ch//eos/user/j/johndoe/file1.root'
        },
        {
            'scope': 'user.johndoe', 
            'name': 'file2.root',
            'rse': 'CERN-PROD_DATADISK',
            'bytes': 2048000,
            'md5': 'def456...',
            'pfn': 'root://eosuser.cern.ch//eos/user/j/johndoe/file2.root'
        }
    ]
    
    # Batch registration
    for file_info in files_to_register:
        try:
            replica_client.add_replica(
                rse=file_info['rse'],
                scope=file_info['scope'],
                name=file_info['name'],
                bytes=file_info['bytes'],
                checksum={'md5': file_info['md5']},
                pfn=file_info['pfn']
            )
            print(f"✓ Registered: {file_info['scope']}:{file_info['name']}")
        except Exception as e:
            print(f"✗ Failed to register {file_info['name']}: {str(e)}")

def check_file_registration(scope, name):
    """Check if a file is properly registered"""
    
    replica_client = ReplicaClient()
    did_client = DIDClient()
    
    try:
        # Check DID exists
        did_info = did_client.get_did(scope, name)
        print(f"DID Info: {did_info}")
        
        # Check replicas
        replicas = list(replica_client.list_replicas([{'scope': scope, 'name': name}]))
        print(f"Replicas: {replicas}")
        
        # Check metadata
        metadata = did_client.get_metadata(scope, name)
        print(f"Metadata: {metadata}")
        
        return True
        
    except Exception as e:
        print(f"File not found or error: {str(e)}")
        return False

if __name__ == "__main__":
    import time
    
    print("=== Rucio File Registration Example ===")
    
    # Register single file
    print("\n1. Registering single file...")
    register_file_on_rse()
    
    # Register multiple files
    print("\n2. Registering multiple files...")
    register_multiple_files()
    
    # Check registration
    print("\n3. Checking file registration...")
    check_file_registration('user.johndoe', 'my_data_file.root')
    ```