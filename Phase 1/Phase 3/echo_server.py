import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5000))
server.listen()
clients = []
lock = threading.Lock()

print("Server listening on port 5000...")
def remove_client(user_socket):
    user_socket.close()
    print("User disconnected")
    with lock:
        clients.remove(user_socket)

def receiver(user_socket):
    while True:
        try:    
            msg = user_socket.recv(1024)
            if msg:
                print(f"User: {msg.decode()}")
                with lock:    
                    targets = clients.copy()
                for client in targets:
                    if client != user_socket: client.send(msg)
            else:
                remove_client(user_socket)
                break
        except ConnectionResetError:
            remove_client(user_socket)
            break

def accept_user():
    while True:
        user_socket, user_adr = server.accept()
        print(f"New connection from {user_adr}")
        with lock: clients.append(user_socket)
        thread1 = threading.Thread(target=receiver, args=(user_socket,))
        thread1.start()

accept_user()
