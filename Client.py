import socket
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def receiving_loop(s):
    while True:
        try:
            data = s.recv(1024)
            if data.decode() == "QUIT":
                break
        except OSError:
            break
        if not data:
            break
        print(data.decode())


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        username = input("Welcome! What is your username?\n")
        s.sendall(username.encode())
        threading.Thread(target=receiving_loop, args=(s,), daemon=True).start()
        while True:
            message = input()
            s.sendall(message.encode())
            if message == "QUIT":
                s.close()
                break


if __name__ == "__main__":
    main()