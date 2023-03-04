# CS262 Spring 2023: Design Exercise 2

Authors: Prayaag Venkat, Hugh Zhang

## Description

A model of a small, asynchronous distributed system. It contains three model machines, each running at different clock speeds. The machines send messages to each other at random and maintain logical clocks.

## Setup

Dependencies:
- Python 3
- os
- random
- time
- socket
- multiprocessing

## Running the simulation

1. Make sure you have dependencies.
2. Run sim_advanced.py. It will print some status messages as well as the randomly chosen clock speeds for the three machines.
3. The results are stored in a folder called logs.

## Interpreting the log files

Each time sim_advanced.py is run, the logs folder is deleted and re-created fresh. The logs folder contains 3 files: 0.txt, 1.txt, 2.txt which store the logged information from Machines 0, 1, 2, respectively.

The individual log files are formatted as follows:
- Each line corresponds to an event (e.g. send, receive message, internal action)
- Each line contains the following information about an event, comma-separated:
    - Event type (send message, receive message, or internal event)
    - The id of the machine on which the event took place. This value is 0, 1 or 2.
    - A piece of "data". 
        - If the event was a received message, "data" is the number of remaining events in the queue.
        - If the event was send a message or internal event, "data" is an int drawn uniformly at random from [1,10] whose meaning is specificied in the project description.
    - The value of the logical clock for that event on that machine
    - The global system time of the event

### Jupyter notebook

We also created a jupyter notebook (labeled analyze-data.ipynb) that provides some tools for visualizing the data from the logs. sim_advanced.py should be run first to generate the data in the logs folder.