# Testing communications

This is currently work in progress, and the code contains two sections:
* MQ Communications
* Rucio Communitcations


An example of Rucio interaction (upload):
```bash
./test/rucio_test.py -v -p /eic/u/eicmax/testbed/swf-data-agent/test.txt -d t8.txt -r BNL_PROD_DISK_1 -s group.daq
```