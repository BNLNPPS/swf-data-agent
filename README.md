# swf-data-agent

This repository is for development of the _swf-data-agent_.
* Purpose: The central data handling agent within the testbed.
* Details: It will listen to the swf-daqsim-agent, manage Rucio STF subscriptions, create new run datasets, and send messages to the swf-processing-agent for run processing and to the swf-fastmon-agent for new STF availability. It will also have a 'watcher' role to identify and report stalls or anomalie