# Testing communications

This is currently work in progress, and the code contains two sections:
* MQ Communications
* Rucio Communitcations


An example of Rucio interaction:
```bash
#  file upload
./test/rucio_test.py -v -p ~/tst.txt -d tst2.txt -r BNL_PROD_DISK_1 -s group.daq -l tst

# attach a file to a dataset
./test/rucio_test.py -v -D swf1 -r BNL_PROD_DISK_1 -s group.daq -l tst3.txt
```