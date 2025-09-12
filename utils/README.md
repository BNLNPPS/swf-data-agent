# Utility scripts

```bash
# Get metadata for a dataset
./rucio_mgt.py -v -s group.daq -D swf.xintest.dataset_6 -G
# Set metadata for a dataset
./rucio_mgt.py -v -s group.daq -D swf.xintest.dataset_6 -S -J '{"transient":true}'

# Same, for a file
./rucio_mgt.py -v -s group.daq -d swf.20250825.211008.836032.no_beam.calib.stf -G
./rucio_mgt.py -v -s group.daq -d swf.20250825.211008.836032.no_beam.calib.stf -S -J '{"transient":false}'
```

The metadata update is specified in the JSON format. For a list of available
attributes, please see the listing below.


Example of an output of the command querying the metadata:
```bash
*** Metadata for the DID group.daq:swf.20250825.211008.836032.no_beam.calib.stf: ***
access_cnt     None
accessed_at    None
account        swf
adler32        0e50326d
availability   AVAILABLE
bytes          193
campaign       None
closed_at      None
complete       None
constituent    None
created_at     2025-08-26 01:10:08
datatype       stf
deleted_at     None
did_type       FILE
eol_at         2019-01-02 00:07:00
events         None
expired_at     None
guid           19f1d955ab7843bd8b379e8c57cf9775
hidden         False
is_archive     None
is_new         False
is_open        None
length         None
lumiblocknr    None
md5            d9101fcd030ed1ad4fca659cf5abb69a
monotonic      False
name           swf.20250825.211008.836032.no_beam.calib.stf
obsolete       False
panda_id       None
phys_group     None
prod_step      None
project        None
provenance     None
purge_replicas True
run_number     100000000
scope          group.daq
stream_name    None
suppressed     False
task_id        None
transient      False
updated_at     2025-09-04 16:42:18
version        1
```