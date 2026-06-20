import json
import struct
import socket
import threading

user = "adi"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def server_closed():
    print("Server closed.")
    server.close()
    exit()


def sender():
    while True:
        msg = input("You: ")
        if not msg:
            continue
        if msg == "quit":
            server_closed()
        data = {'user': user, 'msg': msg}
        json_text = json.dumps(data)
        raw_bytes = json_text.encode('utf-8')
        length = struct.pack('>I', len(raw_bytes))
        try:
            server.sendall(length + raw_bytes)
        except (ConnectionResetError, OSError):
            server_closed()


def read_n(sock, n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            return None
        data += chunk
    return data


def receiver():
    while True:
        try:
            raw_length = read_n(server, 4)
            if not raw_length:
                continue
            length = struct.unpack(">I", raw_length)[0]
            msg = read_n(server, length)
            
            final_msg = json.loads(msg.decode('utf-8'))
            print(f"\n{final_msg['user']}: {final_msg['msg']}\nYou: ", end="", flush=True)
        except (ConnectionResetError, OSError):
            print("Server closed.")
            server.close()
            break


try:
    server.connect(('127.0.0.1', 5000))
except (ConnectionRefusedError):
    server_closed()

thread = threading.Thread(target=receiver, args=())
thread.start()

sender()
