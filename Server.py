import socket
import threading

HOST = "127.0.0.1" 
PORT = 65432  

clients = []
usernames = []

clients_lock = threading.Lock()
usernames_lock = threading.Lock()

def handle_client(conn, addr):
    username = None
    try:
        with conn:
            while True:
                name = conn.recv(1024).strip()
                if not name:
                    return                     
                if not IsUserNameUnique(name):
                    conn.sendall(b"That username is already taken. Please pick another.")
                else:
                    break
            username = name
            with usernames_lock:
                usernames.append(username)
            with clients_lock:
                clients.append(conn)
            broadcast_newUSER(conn, username)
            print(f"Connected by {addr}")

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                if data.decode().strip().upper() == "QUIT":
                    try:
                        conn.sendall(b"QUIT")
                    except OSError:
                        pass
                    break
                broadcast(data, conn, username)
    except OSError:
        pass
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        if username is not None:
            with usernames_lock:
                if username in usernames:
                    usernames.remove(username)
            broadcast_QUIT(username)
        print("Disconnected a Client") 

def broadcast(message, sender_conn, username):
    with clients_lock:
        client_targets = [c for c in clients if c is not sender_conn]
    if client_targets is not None: 
        for conn in client_targets:
            if message.decode() == "QUIT": break
            conn.sendall(username + b": " + message)

def broadcast_QUIT(username):
    with clients_lock:
        for conn in clients:
            conn.sendall(username + b" has left the chat.")

def broadcast_newUSER(sender_conn, username):
    with clients_lock:
        client_targets = [c for c in clients if c is not sender_conn]
    for conn in client_targets:
         conn.sendall(username + b" has entered the chat.")

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