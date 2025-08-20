# swf-data-agent

## About

This repository is for development of the _swf-data-agent_, which is 
the central data handling agent within the _swf_ testbed.

Functionality:
*  It receives the MQ messages from the _swf-daqsim-agent_ and takes actions
according to the messages.
* With respect to Rucio, it created new run datasets,
and manages Rucio STF subscriptions in general.
* It sends messages to the _swf-processing-agent_ for data processing and
to the _swf-fastmon-agent_ to signal new STF availability.
* It will eventually also have a 'watcher' role to identify and report stalls or anomalies.

## Data Transport

The agent does not normally actuates the data transfer by itself. It instead
relies on Rucio for that function, and Rucio in turn operates the **FTS** system
to move data. The transport layer for the FTS is **XRootD**.

## Rucio

Useful information for setting up the components such as Rucio can be found in the
[Startup Guide for NP PanDA & Rucio at BNL](https://docs.google.com/document/d/1zxtpDb44yNmd3qMW6CS7bXCtqZk-li2gPwIwnBfMNNI/edit?tab=t.0).

Quick summary:
* Set up is done using CVMFS (hence it must be mounted on the host)
* Setting up: `source /cvmfs/eic.opensciencegrid.org/rucio-clients/alrb_setup.sh`
* There will be error/warning messages during the setup that can be ignored in most cases.
* Specifying a valid Rucio user ID is important, there will be a prompt for that.
* The user needs a grid certificate and the key, with which to run `voms-proxy-init`.
* Access can be confirmed by using the command `rucio whoami`.
* `$RUCIO_ACCOUNT` contains the current user ID for Rucio.
* An example of a simple command listing Rucio items for a user: `rucio list-dids --filter 'type=all' user.potekhin:*`

Useful examples can be found on the official [Rucio documentation pages](https://rucio.github.io/documentation/user/using_the_client).

The example below lists the available RSEs:
```bash
$ rucio list-rses
BNL_PROD_DISK_1
BNL_TEST_TAPE
DAQ_DISK_1
E1_BNL_DISK_1
E1_JLAB_DISK_1
JLAB_DISK_1
```


More examples:
```bash
rucio --help # a useful CLI help is available
rucio add-dataset user.potekhin:test # add dataset
rucio upload --rse BNL_PROD_DISK_1 --scope user.potekhin ./README.md # upload to a storage endpoint
rucio download user.potekhin:user.potekhin.74311a67-6e47-467d-b44a-244eac13c8be.log # download a container
rucio list-dids --filter 'type=FILE' user.potekhin:*
# This needs to be used prior to deleting rules, if unsure -
rucio list-rules --account my_account
# get useful info about an item:
rucio list-file-replicas user.potekhin:t1.txt
# Will erase a dataset after the 24hrs grace period, is irreversible.
rucio erase user.potekhin:mydataset
```

The way to delete files in Rucio is to delete associated rules.

```bash
# NB. Not every user has the privilege to do this, some accounts do e.g. swf.
rucio update-rule 680886366a584dcfb79b79c3f47af12d   --lifetime -1
# NB. The change won't be instantaneous.
```

Currently the CLI commands need to be run with the local Rucio imports deactivated, because
of the clash with the global ATLAS-based setup.


For running tests and other Python functions which depend on the common SWF packages, please use a setting
similar to this one:

```bash
export RUCIO_COMMS_PATH=/eic/u/eicmax/testbed/swf-common-lib/
```
And,
```bash
voms-proxy-init --cert ./mycert.pem --key ./mykey.pem
```


## Rules

```bash
eicmax@pandaserver02:~ $ rucio-admin subscription add  --account swf --priority 1 testsub   '{"pattern": "swf*", "did_type": ["DATASET"], "scope": ["group.daq"]}'   '[{"copies": 2, "rse_expression": "E1_BNL_DISK_1|E1_JLAB_DISK_1", "activity": "T0 Export", "grouping": "DATASET"}]' 'Test of teh SWF system'
Subscription added b9bb14d2ebff463581c64a16546c245b

```

## XRootD

_XRootD_ is a high-performance, scalable, and fault-tolerant data access framework widely used in scientific computing, especially in high-energy physics. An XRootD server provides remote access to files and datasets over the network using the XRootD protocol. It supports efficient data transfers, authentication, authorization, and can be configured as a standalone server or as part of a distributed cluster for load balancing and redundancy. It is the data transport mechanism used in the test bed, and is actuated
by the _FTS_ system used for data distribution in Rucio.

The XRootD service been installed on the host _pandaserver02.sdcc.bnl.gov_ in a standard type
of a "standalone" configuration, meaning it's not a cluster. More information is contained in the **README** file
in the _xrootd_ folder.



