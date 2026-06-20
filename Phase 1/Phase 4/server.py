import socket
import struct
import json
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = "localhost"
port = 5000
clients = []
lock = threading.Lock()

server.bind((address, port))
server.listen()
print(f"Server listening on {address}:{port}")

def accepter():
    while True:
        user_socket, user_addr = server.accept()
        print(f"New connection from {user_addr}")
        thread = threading.Thread(target=receiver, args=(user_socket, ))
        thread.start()
        with lock: clients.append(user_socket)

def read_n(sock, n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n-len(data))
        if not chunk: return None
        data += chunk
    return data
    
def receiver(user_socket):
    while True:    
        try:    
            length_raw = read_n(user_socket, 4)
            if not length_raw: 
                remove_user(user_socket)
                break
            
            length = struct.unpack('>I', length_raw)[0]
            msg = read_n(user_socket, length)
            
            if not msg:
                remove_user(user_socket)
                break
            data = json.loads(msg.decode('utf-8'))
        except (ConnectionResetError, OSError):
            remove_user(user_socket)
            break
        broadcaster(user_socket, data)

def remove_user(user_socket):
    user_socket.close()
    print("User disconnected.")
    with lock:
        clients.remove(user_socket)

def broadcaster(sender, data):  
    json_text = json.dumps(data)
    raw_bytes = json_text.encode('utf-8')
    length = struct.pack('>I', len(raw_bytes))

    with lock: 
        targets = [client for client in clients if client != sender]
    try:   
        for target in targets:
            target.sendall(length + raw_bytes)   
    except (ConnectionResetError, OSError):
        remove_user(target)

accepter()