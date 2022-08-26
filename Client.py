import socket
import threading
import json
import random

class Player:

    def __init__(self) -> None:
        self.position = [random.randint(0, 750), random.randint(0, 550)]
        self.rotation = 'right'
        self.state = 'Idle'
        self.canPlay = False
        self.canPlayAnim = True

    def setPosition(self, _position):
        self.position = _position

    def getPosition(self):
        return self.position

    def set_rotation(self, rotation):
        self.rotation = rotation
    
    def get_rotation(self):
        return self.rotation

    def set_state(self, _state):
        self.state = _state

    def get_state(self):
        return self.state
    
    def set_animPlayable(self, state):
        self.canPlayAnim = state

    def get_animPlayable(self):
        return self.canPlayAnim

    def setPlayableState(self, state):
        self.canPlay = state

    def getPlayableState(self):
        return self.canPlay

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
HEADER = 4096
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECTED'
MAX_PLAYERS = 2
  
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

player = Player()

count = [0]

def send_str():
    connected = True
    while connected:
        try:
            message = input()
            if(message):
                send_msg(message)
            else:
                send_msg(DISCONNECT_MESSAGE)
                print('You have disconnected!')
                connected = False
        except:
            print('Disconnected from server!')
            connected = False
            break
    client.close()

def receive_str():
    connected = True
    while connected:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if(msg_length):
                try:
                    msg_length = int(msg_length)
                except Exception as ex:
                    print(ex)
                recv_msg = client.recv(msg_length).decode(FORMAT)
                if(recv_msg == DISCONNECT_MESSAGE):
                    connected = False
                elif(recv_msg[0] == '$'):
                    recv_msg = recv_msg[1:]
                    count[0] = int(recv_msg)
                elif(recv_msg[0] == '*'):
                    array = json.loads(recv_msg[1:])
                    player.setPosition(array)
                elif(recv_msg[0] == '#'):
                    recv_msg = recv_msg[1:]
                    player.set_state(recv_msg)
                    player.set_animPlayable(True)
                elif(recv_msg[0] != '$' and recv_msg[0] != '*' and recv_msg[0] != '#'):
                    print(recv_msg)
        except Exception as ex:
            print('Disconnected from server!')
            print('Press enter to terminate!')
            connected = False
            break
    client.close()

def send_position(pos):
    try:
        send_pos(pos)
    except:
        print('Disconnected from server!')
        print('Press enter to terminate!')
        client.close()

def send_msg(msg):
    message = msg.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def send_pos(pos):
    position = json.dumps(pos).encode(FORMAT)
    pos_length = len(position)
    send_length = str(pos_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(position)


def connect_to_server():
    clientName = str(input("Please enter your name: "))
    clientName = "!" + clientName

    print('Connecting...')
    try:
        client.connect(ADDR)
        send_msg(clientName)
        player.setPlayableState(True)
        receive_thread = threading.Thread(target=receive_str)
        receive_thread.start()

        send_thread = threading.Thread(target=send_str)
        send_thread.start()
    except Exception as ex:
        print(f'Couldn\'t connect you to the server: {ex}')

def close_connection():
    client.close()