import socket
import threading

host = 'localhost'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []

def broadcast(message, _client):
    for client in clients:
        if client is not _client:
            client.send(message)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except Exception as e:
            print(f"{e}")
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"Chatbot: {username} disconnected".encode('utf-8'))
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024)

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with address {address}")

        message = f"Chatbot: {username} joined the chat".encode("utf-8")
        broadcast(message, client)

        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()