import socket

HOST = '127.0.0.1'  # localhost — only your own machine can connect
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on {HOST}:{PORT}")

conn, addr = server.accept()         # blocks here — waiting
print(f"Connected: {addr}")

while True:
    data = conn.recv(1024)           # receive up to 1024 bytes
    if not data:                     # empty = client disconnected
        break
    print(f"Received: {data.decode()}")
    conn.send(data)                  # echo it straight back

conn.close()
server.close()
print("Connection closed.")
