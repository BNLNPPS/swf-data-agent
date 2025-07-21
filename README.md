# swf-data-agent

## About

This repository is for development of the _swf-data-agent_, which is 
the central data handling agent within the _swf_ testbed. This is currently
work in progress.

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
* The user needs a grid certificate and the key, with which to run _voms-proxy-init_.
* Access can be confirmed by using the command `rucio whoami`.
* An example of a simple command listing Rucio items for a user: `rucio list-dids --filter 'type=all' user.potekhin:*`



### Setting up Rucio

```bash
source /cvmfs/eic.opensciencegrid.org/rucio-clients/alrb_setup.sh
```
There will be error/warning messages that can be ignored in most cases. Specifying
a valid user ID is important, however -- there will be a prompt for that.


## XRootD

_XRootD_ is a high-performance, scalable, and fault-tolerant data access framework widely used in scientific computing, especially in high-energy physics. An XRootD server provides remote access to files and datasets over the network using the XRootD protocol. It supports efficient data transfers, authentication, authorization, and can be configured as a standalone server or as part of a distributed cluster for load balancing and redundancy. It is the data transport mechanism used in the test bed, and is actuated
by the _FTS_ system used for data distribution in Rucio.

The XRootD service been installed on the host _pandaserver02.sdcc.bnl.gov_ in a standard type
of a "standalone" configuration, meaning it's not a cluster. More information is contained in the **README** file
in the _xrootd_ folder.



