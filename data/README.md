# The Data Agent


## Table of Contents
- [Overview](#overview)
- [Python Interface](#Python)
- [Prerequisite setup](#Setup)

## Overview

The _Data Agent_ package is responsible for the following aspects of the Streaming Workflow
operation:

- listen to MQ messages produced by the _daqsim_, which signal the start and end of runs,
and the creation of _STFs_.
- interact with Rucio to properly register the datasets and STFs.

It uses the **DATA** class for core operations. In case the Rucio _scope_ is not
set, no Rucio operations will be performed.


## Python

An example of using the Rucio package.

```python
from rucio.client import Client
from rucio.client.uploadclient import UploadClient

# Initialize a Rucio client
# You might need to configure Rucio_host, auth_host, account, auth_type and creds
# based on your Rucio setup and authentication method.
client = Client()

# Initialize the UploadClient
upload_client = UploadClient(client)

# Define the upload specification
#  'path': The path to the file you want to upload
#  'rse': The Rucio Storage Element (RSE) where the file should be uploaded
#  'did_scope': The scope of the Data Identifier (DID) for the uploaded file
#  'did_name': The name of the DID for the uploaded file
upload_spec = {
    'path': '/path/to/your/local/file.txt',
    'rse': 'YOUR_RSE_NAME',
    'did_scope': 'YOUR_SCOPE_NAME',
    'did_name': 'your_file_name.txt',
}

# Upload the file
# The upload method returns 0 on success.
result = upload_client.upload([upload_spec])

if result == 0:
    print("File uploaded successfully!")
else:
    print("File upload failed.")
```

## Setup

One has to initialize the Rusio environment as per the "startip PanDA quide",
and perform the _voms-proxy-init_ prior to any Rucio operations, including operating
the Python client. The test script will attempt to load the "comms" package
so it needs to locate it, and this is done via an environment variable i.e.

```bash
export RUCIO_COMMS_PATH=/eic/u/eicmax/testbed/swf-common-lib/
```

