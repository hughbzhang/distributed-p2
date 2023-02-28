import os
import random
import time
import socket
import multiprocessing
import asyncio

PROCESSER_SPEED = [1, 5, 10]
NUM_PROCESSERS = len(PROCESSER_SPEED)
INTERNAL_CLOCK = [0] * NUM_PROCESSERS
MESSAGE_QUEUE = [[]] * NUM_PROCESSERS
DURATION = 6

HOST = "localhost"  # Standard loopback interface address (localhost)
PORTS = [65432, 65433, 65434]


def get_action():
    
    # Generate random int between 1 and 10 inclusive
    action = random.randint(1, 10)
    return action



def execute(processer_id):
    

    if len(MESSAGE_QUEUE[processer_id]) > 0:
        _, _, new_clock = MESSAGE_QUEUE[processer_id].pop(0)
        INTERNAL_CLOCK[processer_id] += 1

        INTERNAL_CLOCK[processer_id] = max(INTERNAL_CLOCK[processer_id], new_clock)
        write_to_log(processer_id, "Received message at local time {}, queue length {}".format(INTERNAL_CLOCK[processer_id], len(MESSAGE_QUEUE[processer_id])))
    else:
        action = get_action()

        
        if action == 1:
            MESSAGE_QUEUE[(processer_id+1)%3].append(("send", processer_id, INTERNAL_CLOCK[processer_id]))
            INTERNAL_CLOCK[processer_id] += 1
            write_to_log(processer_id, "Sent message {} at local time {}".format(action, INTERNAL_CLOCK[processer_id]))
        elif action == 2:
            MESSAGE_QUEUE[(processer_id+2)%3].append(("send", processer_id, INTERNAL_CLOCK[processer_id]))
            INTERNAL_CLOCK[processer_id] += 1
            write_to_log(processer_id, "Sent message {} at local time {}".format(action, INTERNAL_CLOCK[processer_id]))
        elif action == 3:    
            MESSAGE_QUEUE[(processer_id+1)%3].append(("send", processer_id, INTERNAL_CLOCK[processer_id]))
            MESSAGE_QUEUE[(processer_id+2)%3].append(("send", processer_id, INTERNAL_CLOCK[processer_id]))
            INTERNAL_CLOCK[processer_id] += 1
            write_to_log(processer_id, "Sent double message {} at local time {}".format(action, INTERNAL_CLOCK[processer_id]))
        else:
            INTERNAL_CLOCK[processer_id] += 1
            write_to_log(processer_id, "Internal action at local time {}".format(INTERNAL_CLOCK[processer_id]))

def write_to_log(processer_id, message):
    with open("logs/{}.txt".format(processer_id), "a") as f:
        f.write(message + " " + str(time.time()) + "\n")

def run_vm(processer_id):
    # Create a socket to listen to
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORTS[processer_id])
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    time.sleep(1)

    while True:
        try:
            Client, address = server_socket.accept()
            print('Connected received by {}, to: '.format(processer_id) + address[0] + ':' + str(address[1]))

            # Receive message from client
            data = Client.recv(2048)
            
            if data:
                response = 'In process {} received '.format(processer_id) + data.decode('utf-8')
                print(response)
            Client.close()
        except:
            pass

        # Send out messages
        first_socket = socket.socket()
        first_socket.connect((HOST, PORTS[(processer_id+1)%3]))
        second_socket = socket.socket()
        second_socket.connect((HOST, PORTS[(processer_id+2)%3]))

        first_socket.send(str.encode('Msgfrom {}'.format(processer_id)))
        second_socket.send(str.encode('Msgfrom {}'.format(processer_id)))
        

        first_socket.close()
        second_socket.close()

    
    server_socket.close()
    





if __name__ == '__main__':
    vms = [multiprocessing.Process(target=run_vm, args=(i,)) for i in range(3)]

    for vm in vms:
        vm.start()

    end = time.time() + DURATION
    while True:
        if time.time() > end:
            for vm in vms:
                vm.terminate()
                vm.join()
            break


