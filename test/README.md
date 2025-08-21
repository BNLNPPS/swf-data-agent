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