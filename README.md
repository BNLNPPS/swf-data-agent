# swf-data-agent

## About

This repository is for development of the _swf-data-agent_.
* Purpose: The central data handling agent within the testbed.
* Details: It will listen to the swf-daqsim-agent, manage Rucio STF subscriptions, create new run datasets, and send messages to the swf-processing-agent for run processing and to the swf-fastmon-agent for new STF availability. It will also have a 'watcher' role to identify and report stalls or anomalie

## XRootD

##

_XRootD_ is a high-performance, scalable, and fault-tolerant data access framework widely used in scientific computing, especially in high-energy physics. An XRootD server provides remote access to files and datasets over the network using the XRootD protocol. It supports efficient data transfers, authentication, authorization, and can be configured as a standalone server or as part of a distributed cluster for load balancing and redundancy. It is the data transport mechanism used in the test bed, and is actuated
by the _FTS_ system used for data distribution in Rucio.

The XRootD service been installed on the host _pandaserver02.sdcc.bnl.gov_ in a standard type
of a "standalone" configuration, meaning it's not a cluster.
