import socket
import ssl
import threading


AUTH_PASSWORD = "securepass123"  

host = '0.0.0.0'
port = 12345

# Create TCP socket and wrap with SSL
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"[+] Listening securely on port {port}...")

# wrapping socket in TLS
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="ssl/cert.pem", keyfile="ssl/key.pem")
secure_socket = context.wrap_socket(server_socket, server_side=True)

client_socket, addr = secure_socket.accept()
print(f"[+] Client connected from {addr}")

# Authenticatication
client_socket.sendall("Password: ".encode())
password = client_socket.recv(1024).decode().strip()

if password != AUTH_PASSWORD:
    client_socket.sendall("Authentication failed. Disconnecting.\n".encode())
    print("[-] Client failed to authenticate.")
    client_socket.close()
    exit()

client_socket.sendall("Authentication successful. Welcome!\n".encode())
print("[+] Client authenticated successfully.")

# recieving
def receive():
    while True:
        try:
            data = client_socket.recv(1024).decode().strip()
            if data:
                print(f"[Client]: {data}")
        except:
            print("[-] Connection closed.")
            client_socket.close()
            break

# outward
def send():
    while True:
        try:
            message = input()
            client_socket.sendall((message + "\n").encode())
        except:
            print("[-] Could not send message.")
            break

threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=send).start()
