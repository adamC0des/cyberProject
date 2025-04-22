import socket
import ssl
import threading

host = '172.184.138.111'  # Your Azure VM's public IP
port = 12345
password = "securepass123"  # Must match the server

# Set up SSL context to trust the self-signed cert
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # ⚠️ Dev mode: no cert validation

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket = context.wrap_socket(client_socket)

secure_socket.connect((host, port))
print(f"[+] Connected securely to {host}:{port}")

# Handle authentication prompt
prompt = secure_socket.recv(1024).decode()
print(prompt, end='')  # Print 'Password: ' from server
secure_socket.sendall((password + "\n").encode())

auth_response = secure_socket.recv(1024).decode()
print(auth_response)

if "failed" in auth_response.lower():
    secure_socket.close()
    exit()

# Receive thread
def receive():
    while True:
        try:
            data = secure_socket.recv(1024).decode().strip()
            if data:
                print(f"[Server]: {data}")
        except:
            print("[-] Connection closed.")
            break

# Send thread
def send():
    while True:
        try:
            message = input()
            secure_socket.sendall((message + "\n").encode())
        except:
            print("[-] Could not send message.")
            break

threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=send).start()
