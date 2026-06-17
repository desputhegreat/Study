import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try: server.connect(("localhost",5000))
except ConnectionRefusedError: 
    print("Server Closed") 
    exit()
while True:
    msg = input("You: ").strip().encode()
    try:    
        server.send(msg)
        reply = server.recv(1024).decode()
        print(f"Server: {reply}")
    except ConnectionResetError:
        server.close()
        print("Server Closed")  

