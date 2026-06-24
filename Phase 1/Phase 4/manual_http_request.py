import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('example.com', 80))

request = (
    "GET / HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "Connection: close\r\n"
    "\r\n"
)
sock.sendall(request.encode('utf-8'))

response = b''
while True:
    chunk = sock.recv(4096)
    if not chunk:
        break
    response += chunk

print(response.decode('utf-8', errors='ignore'))
sock.close()
