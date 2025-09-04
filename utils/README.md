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

