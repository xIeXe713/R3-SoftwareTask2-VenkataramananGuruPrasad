import socket 
import threading

# constants to make it easier to change certain things
HEADER = 64 # Header length to be sent/received, can be changed as per requirements.
PORT = 5050 # Specifies Port to try and connect to
SERVER = socket.gethostbyname(socket.gethostname()) # IP of server
ADDR = (SERVER, PORT) # full address with both server and port
FORMAT = 'utf-8' # encode/decode format for converting bits to text and vice versa
DISCONNECT_MESSAGE = "!DISCONNECT" # static message to disconnect so server doesnt get overloaded

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize server
server.bind(ADDR) # Bind this address to the server - means that this is the server

def handle_client(conn, addr): # function that receives and prints data
    print(f"[NEW CONNECTION] {addr} connected.") # To show when connections have been added etc.

    connected = True # loop variable
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # receives Header containing number of bytes in actual message
        if msg_length: # handling exception if it is empty
            msg_length = int(msg_length) # int conversion
            msg = conn.recv(msg_length).decode(FORMAT) # receiving message from connected client
            if msg == DISCONNECT_MESSAGE:
                connected = False # handling disconnection

            print(f"{msg}") # print message

    conn.close() # close connection fully
        

def start(): # starting server
    server.listen() # listening for connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() # accepts client requests
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() # threading allows for multiple clients to connect and continue their work
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") 


print("[STARTING] server is starting...")
start()