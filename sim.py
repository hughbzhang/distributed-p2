import os
import random
import time

PROCESSER_SPEED = [1, 5, 10]
NUM_PROCESSERS = len(PROCESSER_SPEED)
INTERNAL_CLOCK = [0] * NUM_PROCESSERS
MESSAGE_QUEUE = [[]] * NUM_PROCESSERS

def get_action():
    
    # Generate random int between 1 and 10 inclusive
    action = random.randint(1, 10)
    return action



def execute(processer_id):
    INTERNAL_CLOCK[processer_id] += 1

    if len(MESSAGE_QUEUE[processer_id]) > 0:
        _, _, new_clock = MESSAGE_QUEUE[processer_id].pop(0)
        INTERNAL_CLOCK[processer_id] = max(INTERNAL_CLOCK[processer_id], new_clock)
        write_to_log(processer_id, "Received message at time {}".format(INTERNAL_CLOCK[processer_id]))

    action = get_action()

    if action in [1, 2, 3]:
        if action == 1 or action == 3:
            MESSAGE_QUEUE[(processer_id+1)%3].append(("send", processer_id, INTERNAL_CLOCK[processer_id]))
        if action == 2 or action == 3:
            MESSAGE_QUEUE[(processer_id+2)%3].append(("send", processer_id, INTERNAL_CLOCK[processer_id]))

        write_to_log(processer_id, "Sent message {} at time {}".format(action, INTERNAL_CLOCK[processer_id]))
    else:
        write_to_log(processer_id, "No external action taken at time {}".format(INTERNAL_CLOCK[processer_id]))

def write_to_log(processer_id, message):
    with open("logs/{}.txt".format(processer_id), "a") as f:
        f.write(message + " " + str(time.time()) + "\n")

def run():
    # Processer speed is how often a processer will check for new instructions

    # Delete all log files
    if not os.path.exists("logs"):
        os.mkdir("logs")
    else:
        for f in os.listdir("logs"):
            os.remove(os.path.join("logs", f))
        

    real_timestamp = 0

    while True:
        real_timestamp += 1
        for i, processer_speed in enumerate(PROCESSER_SPEED):
            if real_timestamp % processer_speed == 0:
                execute(i)



if __name__ == '__main__':
    run()
