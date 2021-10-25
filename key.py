import keyboard
import time
import sys

import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def turn(key, s):
    if key == 'w':
        m1, m2, m3, m4 = 'f', 'f', 'f', 'f'
    if key == 'a':
        m1, m2, m3, m4 = 'r', 'r', 'f', 'f'
    if key == 's':
        m1, m2, m3, m4 = 'r', 'r', 'r', 'r'
    if key == 'd':
        m1, m2, m3, m4 = 'f', 'f', 'r', 'r'
    
    return f"[{m1}{s}][{m2}{s}][{m3}{s}][{m4}{s}]"

while True:
    key = keyboard.read_key()
    if key == 'esc':
        send(DISCONNECT_MESSAGE)
        sys.exit()
    if key in ['1', '2', '3', '4', '5']:
        time.sleep(0.25)
        send(f'Your speed is now set to {key}')
        s = str(int(key)*51)
    if key in ['w', 'a', 's', 'd']:
        time.sleep(0.25)
        message = turn(key, s)
        send(message)
