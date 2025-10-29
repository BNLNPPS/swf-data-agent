# The DATA Class

The DATA class is the main data management class.
It receives messages from the DAQ simulator and handles them.

Main functionality is to create Rucio datasets and register files to
these datasets. Then, to notify the processing agent that the data is ready.

It uses the mq_comms and rucio_comms packages for MQ and Rucio operations.
Both packages are located in the swf-common repository.

Datasets are created upon receiving the run_imminent message.
This is the only run-related message that the DATA class processes, other
are placeholders.

* Files are registered upon receiving the stf_gen message.
* The run_id and dataset name are extracted from the run_imminent message.
* The data folder is defined globally.
* The Rucio scope and RSE are defined globally.
* The file is attached to the dataset after it is uploaded to Rucio.
* The file metadata is set upon registration.
* The file is registered under the provided Rucio scope.
* The dataset is created under the provided Rucio scope.

Operations specific to XRootD upload mode are marked in the code.

