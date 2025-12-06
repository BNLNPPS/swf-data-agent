# The DATA Class


## The role of the class

The DATA class is the main data management class.
It receives messages from the DAQ simulator and handles them.

Main functionality is to create Rucio datasets and register files to
these datasets. Then, to notify the processing agent that the data is ready.

It uses the mq_comms and rucio_comms packages for MQ and Rucio operations.
Both packages are located in the swf-common repository.

Datasets are created upon receiving the **run_imminent** message.
This is the only _run-related message_ that the DATA class processes, other
are placeholders.

## Details of message processing

* The run_id and dataset name are extracted from the run_imminent message.
* The dataset for the run is created under the provided Rucio scope.
* Files are registered upon receiving the **stf_gen** message.
* The data folder, the Rucio scope and RSE are defined globally.
* The file is attached to the dataset after _it is uploaded to Rucio._
* The file is registered under the provided Rucio scope, and its metadata is set upon registration.


## Upload

There are two modes of data upload, Rucio/FTS and XRootD. In the former case, Rucio will handle
metadata. In the latter, this needs to be added in the application code (which is done).

Operations specific to XRootD upload mode are marked in the code.


