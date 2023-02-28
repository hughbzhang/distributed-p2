import os
import random
import time
import socket
import multiprocessing
import asyncio

PROCESSER_SPEED = [1, 5, 10]
NUM_PROCESSERS = len(PROCESSER_SPEED)
DURATION = 6

HOST = "localhost"  # Standard loopback interface address (localhost)
PORTS = [65432, 65433, 65434]


def get_action():
    
    # Generate random int between 1 and 10 inclusive
    action = random.randint(1, 10)
    return action




def write_to_log(processer_id, message):
    with open("logs/{}.txt".format(processer_id), "a") as f:
        f.write(message + " " + str(time.time()) + "\n")

def run_vm(processer_id):
    queue = []
    clock = 0

    # Create a socket to listen to
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORTS[processer_id])
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    print("VM {} online, will begin sending and receiving in 1 second".format(processer_id))
    time.sleep(1)

    while True:
        try:
            Client, address = server_socket.accept()
            #print('Connected received by {}, to: '.format(processer_id) + address[0] + ':' + str(address[1]))

            # Receive message from client
            data = Client.recv(2048)
            
            if data:
                #response = 'In process {} received '.format(processer_id) + data.decode('utf-8')
                #print(response)
                
                queue.append(data.decode('utf-8').split(','))
            Client.close()
        except:
            pass

        start = time.time()
        end = start + 1
        
         # loop over num_cycles    
        for _ in  range(PROCESSER_SPEED[processer_id]):
            if len(queue) > 0:
                new_clock = int(queue.pop(0)[-1])
                clock += 1
                clock = max(clock, new_clock)
                write_to_log(processer_id, "Received message at local time {}, queue length {}".format(clock, len(queue)))
            
            else:
                action = get_action()
                if action in [1,2,3]:
                    
                    if action == 1:
                        first_socket = socket.socket()
                        first_socket.connect((HOST, PORTS[(processer_id+1)%3]))
                        first_socket.send(str.encode('{},{},{}'.format(action,processer_id,clock)))
                        first_socket.close()
                        clock+=1
                        write_to_log(processer_id, "Sent message {} at local time {}".format(action, clock))
                    elif action == 2:
                        second_socket = socket.socket()
                        second_socket.connect((HOST, PORTS[(processer_id+2)%3]))
                        second_socket.send(str.encode('{},{},{}'.format(action,processer_id,clock)))
                        second_socket.close()
                        clock+=1
                        write_to_log(processer_id, "Sent message {} at local time {}".format(action, clock))  
                    elif action == 3:
                        first_socket = socket.socket()
                        first_socket.connect((HOST, PORTS[(processer_id+1)%3]))
                        first_socket.send(str.encode('{},{},{}'.format(action,processer_id,clock)))
                        first_socket.close()
                        second_socket = socket.socket()
                        second_socket.connect((HOST, PORTS[(processer_id+2)%3]))
                        second_socket.send(str.encode('{},{},{}'.format(action,processer_id,clock)))
                        second_socket.close()
                        clock+=1
                        write_to_log(processer_id, "Sent double message {} at local time {}".format(action, clock))  
                    else:
                        clock+=1
                        write_to_log(processer_id, "Internal action at local time {}".format(clock))
        
        if time.time() < end:
            time.sleep(end - time.time())   
    server_socket.close()
    





if __name__ == '__main__':
    # Delete all log files
    
    if not os.path.exists("logs"):
        os.mkdir("logs")
    else:
        for f in os.listdir("logs"):
            os.remove(os.path.join("logs", f))
    
    vms = [multiprocessing.Process(target=run_vm, args=(i,)) for i in range(3)]

    print("starting vms")
    for vm in vms:
        vm.start()

    end = time.time() + DURATION
    while True:
        if time.time() > end:
            for vm in vms:
                vm.terminate()
                vm.join()
            break


