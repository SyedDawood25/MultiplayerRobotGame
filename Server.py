import socket
import threading
import time
import json

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
HEADER = 4096
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECTED'

clients = []
clientNames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"Joined Successfully!, Incoming connection from {addr}...")

    try:
        send_str('[SERVER] Welcome to the server!', conn)
        connected = True
    except:
        connected = False
    setName = False
    while connected:
        try:
            if(clients):
                send_str(f'${len(clients)}', conn)
                send_str_ToOthers(f'${len(clients)}', conn)
            canSend_str = True
            canSend_pos = False
            canSend_state = False
            try:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if(msg_length):
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)

                    if(msg[0] == '!' and not setName):
                        setName = True
                        canSend_str = False
                        addr = msg[1:]
                        send_str_ToOthers(f'[SERVER] {addr} has joined!', conn)
                        clientNames.append(addr)
                        clients.append(conn)

                    if(msg == DISCONNECT_MESSAGE):
                        msg = f'[SERVER] {addr} HAS DISCONNECTED!'
                        send_str_ToOthers(msg, conn)
                        clients.remove(conn)
                        send_str_ToOthers(f'${len(clients)}', conn)
                        connected = False
                        canSend_str = False
                    
                    if(msg[0] == '['):
                        try:
                            array = json.loads(msg)
                            canSend_str = False
                            canSend_pos = True
                        except Exception as ex:
                            print(ex)
                    
                    if(msg[0] == '#'):
                        canSend_state = True

                    if(canSend_state):
                        send_str_ToOthers(msg, conn)
                        canSend_state = False

                    if(canSend_pos):
                        send_str_ToOthers(f'*{array}', conn)
                        canSend_pos = False

                    if(canSend_str):
                        msg = f'[{addr}] ' + msg
                        send_str_ToOthers(msg, conn)
            except Exception as ex:
                clients.remove(conn)
                send_str_ToOthers(f'${len(clients)}', conn)
                connected = False
        except:
            break

    conn.close()

def start():
    print(f"Starting server at {SERVER}:{PORT}...")
    time.sleep(1.5)
    server.listen()
    print('Started Server!, awaiting clients...')
    while True:
        conn, addr = server.accept()

        try:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"ACTIVE CONNECTIONS: {threading.activeCount() - 1}")
        except Exception as ex:
            pass


def send_str_ToOthers(msg, conn):
    for i in range(len(clients)):
        if(clients[i] != conn):
            send_str(msg, clients[i])


def send_str(msg, conn):
    message = msg.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

start()