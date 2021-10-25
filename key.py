import keyboard
import time
import sys

import socket

# constants to make it easier to change certain things
HEADER = 64 # Header length to be sent/received, can be changed as per requirements.
PORT = 5050 # Specifies Port to try and connect to
SERVER = socket.gethostbyname(socket.gethostname()) # IP of server
ADDR = (SERVER, PORT) # full address with both server and port
FORMAT = 'utf-8' # encode/decode format for converting bits to text and vice versa
DISCONNECT_MESSAGE = "!DISCONNECT" # static message to disconnect so server doesnt get overloaded

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initializing client
client.connect(ADDR) # connecting to server

def send(msg): # function to encode and send messages to server
    message = msg.encode(FORMAT) # encoding with UTF-8
    msg_length = len(message) # for header
    send_length = str(msg_length).encode(FORMAT) # encoding header
    send_length += b' ' * (HEADER - len(send_length)) # padding header to hit HEADER amount of bytes
    client.send(send_length)
    client.send(message)

# to handle directions
def turn(key, s):
    if key == 'w': 
        m1, m2, m3, m4 = 'f', 'f', 'f', 'f' # forward
    if key == 'a':
        m1, m2, m3, m4 = 'r', 'r', 'f', 'f' # left
    if key == 's':
        m1, m2, m3, m4 = 'r', 'r', 'r', 'r' # reverse
    if key == 'd':
        m1, m2, m3, m4 = 'f', 'f', 'r', 'r' # right
    
    return f"[{m1}{s}][{m2}{s}][{m3}{s}][{m4}{s}]" # return fstring which is the required message to send

while True:
    key = keyboard.read_key() # listening for input
    if key == 'esc':
        send(DISCONNECT_MESSAGE)
        sys.exit() # exiting
    if key in ['1', '2', '3', '4', '5']:
        time.sleep(0.25) # this is used to ensure that multiple key presses and multiple calls aren't recorded to reduce clutter
        send(f'Your speed is now set to {key}') # message when speed is changed
        s = str(int(key)*51) # converting using PWM
    if key in ['w', 'a', 's', 'd']:
        time.sleep(0.25) # this is used to ensure that multiple key presses and multiple calls aren't recorded to reduce clutter
        message = turn(key, s) # storing result
        send(message) # sending to server
