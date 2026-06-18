import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5000))
server.listen()

print("Server listening on port 5000...")

def receiver(user_socket):
    while True:
        try:    
            msg = user_socket.recv(1024)
            print(f"User: {msg.decode()}")
            if msg:
                user_socket.send(msg)
            else:
                user_socket.close()
                print("User disconnected")
                break
        except ConnectionResetError:
            user_socket.close()
            print("User disconnected")
            break

def accept_user():
    while True:
        user_socket, user_adr = server.accept()
        print(f"New connection from {user_adr}")
        thread1 = threading.Thread(target=receiver, args=(user_socket,))
        thread1.start()

accept_user()
