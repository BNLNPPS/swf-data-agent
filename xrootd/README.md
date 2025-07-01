# The XRootD setup

Configuration files are stored in the folder _/etc/xrootd/_. In this case, the file of interest is _xrootd-standalone.cfg_.
In particular, it specified the partition which is to be made accessible via XRootD.

Commands:

```bash
sudo service xrootd@standalone restart # restart (needs sudo)
service xrootd@standalone status # check status

# Test copying to the client's folder:
xrdcp root://pandaserver02.sdcc.bnl.gov:1094//data/DAQbuffer/test.txt .
```