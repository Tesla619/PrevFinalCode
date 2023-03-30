import socket

SHOST = ''  # Standard loopback interface address (localhost)
#SHOST = socket.gethostbyname(socket.gethostname())
PORT = 8888  # Port to listen on (non-privileged ports are > 1023)

CHOST = "192.168.31.116"#"127.0.0.1"  # The server's hostname or IP address

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SHOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
            
def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CHOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)

    print(f"Received {data!r}")
    
while True:
    server()
#client()