# Multi-Client Chat Application (TCP Sockets, Python)

Assignment 3, COMP 3670

A chat room built with Python's `socket` and `threading` modules only. Clients connect to one server, pick a unique username, and the server forwards each message to every other connected client. Clients never talk to each other directly.

## Files

- `server.py`: the chat server
- `client.py`: the chat client (run one copy per user)

## How to Run

Requires Python 3. The server listens on `127.0.0.1:65432`. Use a separate terminal for the server and for each client.

1. Start the server first: `python server.py`
2. In other terminals, start as many clients as you like: `python client.py`
3. Enter a username. If it is already taken, the server says so and you enter another.
4. Type messages and press Enter. Other clients see them as `username: message`.
5. Type `QUIT` to leave. The other clients are notified.
6. Stop the server with `Ctrl+C`.

## Design Overview

**Architecture.** Client-server model: every message goes client, then server, then the other clients.

**Server.**
- The main thread loops on `accept()` and starts a new daemon thread (`handle_client`) for each connection, so many clients can be served at once.
- Two shared lists, `clients` (sockets) and `usernames`, are each protected by a `threading.Lock`.
- A client's first message is its username. If it is already in `usernames`, the server replies that it is taken and waits for another. Once accepted, the name and socket are stored.
- `broadcast` sends a message to every client except the sender. `broadcast_newUSER` and `broadcast_QUIT` announce joins and leaves.
- A client leaves by typing `QUIT`, or by closing its window (detected by an empty `recv()` or an `OSError`). Both are handled in a `finally` block: the socket and username are removed, the others are notified, and the socket is closed. The username can then be reused.

**Client.**
- The main thread always waits on `input()` and sends each line to the server. Typing `QUIT` sends it and closes the socket.
- A second daemon thread (`receiving_loop`) runs `recv()` and prints incoming messages immediately, even while the user is typing. It stops when the server replies `QUIT` or the socket closes.

## Screenshots

Included in the submission: multiple clients connected, messages between two clients with the server output, and a client disconnecting (with the other clients notified and the server's disconnect message).
