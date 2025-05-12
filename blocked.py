import socket
import ssl

host = '172.184.138.111'  # Azure VM IP
port = 12345

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket = context.wrap_socket(client_socket)

try:
    print(f"[~] Trying to connect to {host}:{port}...")
    secure_socket.settimeout(5)
    secure_socket.connect((host, port))

    # If connection succeeds, read server response
    response = secure_socket.recv(1024).decode()
    print(f"[!] Unexpected access: server responded with: {response}")

except Exception as e:
    print(f"[✔️] Access denied or blocked by firewall. Exception caught:\n{e}")
finally:
    secure_socket.close()
