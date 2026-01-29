import socket
import sys

def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} on {ip} is OPEN")
        else:
            print(f"Port {port} on {ip} is CLOSED (Code: {result})")
        sock.close()
    except Exception as e:
        print(f"Error checking {ip}:{port}: {e}")

print("Checking connectivity...")
check_port("100.115.17.68", 8765)  # igor-gaming-1
check_port("100.110.209.49", 8765) # unified-home-core-cloud
