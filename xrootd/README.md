# The XRootD setup

## Useful commands

Configuration files are stored in the folder _/etc/xrootd/_. In this case, the file of interest is _xrootd-standalone.cfg_.
In particular, it specified the partition which is to be made accessible via XRootD.

Commands:

```bash
sudo service xrootd@standalone restart # restart (needs sudo)
service xrootd@standalone status # check status

# Test copying to the client's folder:
xrdcp root://pandaserver02.sdcc.bnl.gov:1094//data/DAQbuffer/test.txt .

# Checking the file in the working area
xrdfs root://dcintdoor.sdcc.bnl.gov:1094//pnfs ls -l /pnfs/sdcc.bnl.gov/eic/epic/disk/swf_test_bnl/group/daq/1d/49/myout.txt
```

## Rucio Storage Element organization (including the XRootD door access)

* One RSE to emulate the DAQ buffer, where DAQ/STF files will be copied to and registered with Rucio
   * DAQ_DISK_3, root://dcintdoor.sdcc.bnl.gov:1094//pnfs/sdcc.bnl.gov/eic/epic/disk/swfdaqtest/
* The following two RSEs are to emulate  the E1 RSEs. Rucio will replicate DAQ STF datasets from DAQ_DISK_3 to them,
and PanDA will read task input datasets from them, and save output to them as well.  
   * E1_BNL_DISK_1, root://dcintdoor.sdcc.bnl.gov:1094//pnfs/sdcc.bnl.gov/eic/epic/disk/swf_test_bnl/
   * E1_JLAB_DISK_1, root://dcintdoor.sdcc.bnl.gov:1094//pnfs/sdcc.bnl.gov/eic/epic/disk/swf_test_jlab/
