import socket
import time


def int_converter(var):
    while True:
        try:
            x = int(input(f"Enter the {var}: "))
            break
        except ValueError:
            print(f"Please enter a valid {var}.")
    return x

def domain_resolve():
    try:
        domain_ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return None    
    return domain_ip

def latency_calc(ip, port, attempt):
    if not ip:
        return None
    try:
        for _ in range(attempt):
            times = []
            
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.settimeout(3)
            
            start = time.perf_counter()
            server.connect((ip, port))
            end = time.perf_counter()
            server.close()
            
            times.append((end-start) * 1000)
    except (ConnectionRefusedError, socket.timeout):
        pass
    if time:
        return round(sum(times)/len(times), 2)
    return None


domain = input("Enter the domain: ")
port = int_converter("port")
attempt = int_converter("attempts")

resolved_ip = domain_resolve()
latency = latency_calc(resolved_ip, port, attempt)

print(f"Domain: {domain}")
print(f"DNS Lookup: {resolved_ip}")
print(f"Port: {port}")
print(f"Latency: {latency}")