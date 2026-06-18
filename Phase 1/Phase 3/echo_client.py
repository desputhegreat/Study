import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: server.connect(("localhost",5000))
except (ConnectionRefusedError, OSError): 
    print("Server Closed") 
    exit()

def receiver():
    while True:  
        try:
            msg = server.recv(1024).decode()
            print(f"\nUser: {msg}\nYou: ", end="", flush=True)
        except (ConnectionResetError, OSError):
            break

thread = threading.Thread(target=receiver, args=())
thread.daemon = True
thread.start()

while True:
    msg = input("You: ")
    if not msg: continue
    if msg.lower() == 'quit':
        server.close()
        break
    try:
        server.send(msg.encode())
    except ConnectionResetError:
        print("Server closed")
        server.close()
        break         

