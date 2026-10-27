import socket
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def receiving_loop(s):
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(data.decode())
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        threading.Thread(target=receiving_loop, args=(s,), daemon=True).start()
        data = None
        while True:
            message = input()
            s.sendall(message.encode())


if __name__ == "__main__":
    main()