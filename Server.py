import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

clients = []

clients_lock = threading.Lock()
usernames_lock = threading.Lock()

def handle_client(conn, addr, username):
    with clients_lock:
        clients.append(conn)
    try:
        with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    broadcast(data, conn, username)
    except OSError:
        pass
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
                
    print("Disconnected a Client") 

def broadcast(message, sender_conn, username):
    with clients_lock:
        client_targets = [c for c in clients if c is not sender_conn]
    for conn in client_targets:
         print(username)
         print(username.decode())
         conn.sendall(username + b": " + message)
  
    
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                username = conn.recv(1024)
                threading.Thread(target=handle_client, args=(conn, addr, username), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()