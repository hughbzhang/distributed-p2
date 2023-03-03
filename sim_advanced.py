import os
import random
import time
import socket
import multiprocessing


MIN_SPEED = 1
MAX_SPEED = 2
NUM_PROCESSERS = 3
PROCESSER_SPEED = [random.randint(MIN_SPEED, MAX_SPEED) for _ in range(NUM_PROCESSERS)]
DURATION = 60
MAX_ACTIONS = 10
FIRST = [1,2]
SECOND = [3,4]
BOTH = [5,6]
SEND = FIRST + SECOND + BOTH

HOST = "localhost"  
PORTS = [6543, 6542, 6541]


def get_action():
    
    # Generate random int between 1 and 10 inclusive
    action = random.randint(1, MAX_ACTIONS)
    return action




def write_to_log(processer_id, message, data, clock):
    with open("logs/{}.txt".format(processer_id), "a") as f:
        f.write(",".join([message, str(processer_id), str(data), str(clock), str(time.time())])+"\n")

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
            #print('a' + str(processer_id))
            # TODO: THE LINE BELOW THROWS EXCEPTIONS SOMETIMES
            Client, address = server_socket.accept()
            #print('b' + str(processer_id))
            #print('Connected received by {}, to: '.format(processer_id) + address[0] + ':' + str(address[1]))

            # Receive message from client
            with Client:
                while True:
                    data = Client.recv(2048)
                    if data:
                        queue.append(data.decode('utf-8').split(','))
                        break
            
        except Exception as e:
            #print(e)
            print("No incoming message")

        start = time.time()
        end = start + 1
        
         # loop over num_cycles    
        for _ in  range(PROCESSER_SPEED[processer_id]):
            if len(queue) > 0:
                new_clock = int(queue.pop(0)[-1])
                clock += 1
                clock = max(clock, new_clock)
                write_to_log(processer_id, "recv", len(queue), clock)
            
            else:
                action = get_action()
                if action in SEND:
                    
                    if action in FIRST:
                        first_socket = socket.socket()
                        first_socket.connect((HOST, PORTS[(processer_id+1)%3]))
                        first_socket.send(str.encode('{},{},{}'.format(action,processer_id,clock)))
                        first_socket.close()
                        clock+=1
                        write_to_log(processer_id, "sent", action , clock)
                    elif action in SECOND:
                        second_socket = socket.socket()
                        second_socket.connect((HOST, PORTS[(processer_id+2)%3]))
                        second_socket.send(str.encode('{},{},{}'.format(action,processer_id,clock)))
                        second_socket.close()
                        clock+=1
                        write_to_log(processer_id, "sent", action , clock)  
                    elif action in BOTH:
                        first_socket = socket.socket()
                        first_socket.connect((HOST, PORTS[(processer_id+1)%3]))
                        first_socket.send(str.encode('{},{},{}'.format(action,processer_id,clock)))
                        first_socket.close()
                        second_socket = socket.socket()
                        second_socket.connect((HOST, PORTS[(processer_id+2)%3]))
                        second_socket.send(str.encode('{},{},{}'.format(action,processer_id,clock)))
                        second_socket.close()
                        clock+=1
                        write_to_log(processer_id, "sent2", action , clock)  
                else:
                    clock+=1
                    write_to_log(processer_id, "internal", action , clock)
        
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

    print("starting vms, clock speeds: " + str(PROCESSER_SPEED))
    for vm in vms:
        vm.start()

    end = time.time() + DURATION
    while True:
        if time.time() > end:
            for vm in vms:
                vm.terminate()
                vm.join()
            break


