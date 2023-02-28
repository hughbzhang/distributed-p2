# distributed-p2


# TODO
- The (virtual) machine should listen on one or more sockets for such messages. Each of your virtual machines should connect to each of the other virtual machines so that messages can be passed between them
- How to get global time?

- Then, run the scale model at least 5 times
- drift in the values of the local logical clocks in the different machines (you can get a god’s eye view because of the system time)
- Collect in list and plot:
    - size of the jumps in the values for the logical clocks
    - drift in the values of the local logical clocks in the different machines
    - the impact different timings on such things as gaps in the logical clock values and length of the message queue.
-  try running it with a smaller variation in the clock cycles