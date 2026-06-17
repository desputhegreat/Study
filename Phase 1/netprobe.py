import socket

while True:
    try:
        domain = input("Enter the domain: ")
        domain_ip = socket.gethostbyname(domain)
        break
    except socket.gaierror:
        print("Please enter a valid domain.")

print(f"The IP Address for {domain} is {domain_ip}")