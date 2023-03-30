from logging import exception
import socket
import time

IP = "192.168.31.116"
PORT = 8889 # Port to listen on (non-privileged ports are > 1023)
            
def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        try:
            s.connect((IP, PORT))
            s.sendall(b"[00619]: PASS") #PASS
            data = s.recv(1024)

            if data == b"Unlocked":
                print(f"Received {data!r}")
                return False
            else:
                time.sleep(0.5)
                return True
            
        except Exception:
            pass
    return True
        
while client():
    pass

print("UNLOCKED")