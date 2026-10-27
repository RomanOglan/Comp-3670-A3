import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

clients = []
usernames = []

clients_lock = threading.Lock()
usernames_lock = threading.Lock()

def handle_client(conn, addr):
    with clients_lock:
        clients.append(conn)
    while True:
        username = conn.recv(1024)
        if IsUserNameUnique(username) == False:
            conn.sendall(b"That username is already Taken. Please pick another.")
        else:
            break
                  
    with usernames_lock:
        usernames.append(username)

    try:
        with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if data.decode() == "QUIT":
                        conn.sendall(b"QUIT")
                        
                        with clients_lock:
                            if conn in clients:
                                clients.remove(conn)

                        with usernames_lock:
                            if username in usernames:
                                usernames.remove(username)
                        broadcast_QUIT(username)
                        break
                    if not data:
                        break
                    broadcast(data, conn, username)
    except OSError:
        pass
              
    print("Disconnected a Client") 

def broadcast(message, sender_conn, username):
    with clients_lock:
        client_targets = [c for c in clients if c is not sender_conn]
    for conn in client_targets:
         conn.sendall(username + b": " + message)

def broadcast_QUIT(username):
    with clients_lock:
        for conn in clients:
            conn.sendall(username + b"has left the chat")

def IsUserNameUnique(username):
    with usernames_lock:
        for us in usernames:
            if us == username:
                return False
        return True
    
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()    
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()