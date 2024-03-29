import socket
import threading

username = input("Enter your username: ")

host = 'localhost'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)

        except Exception as e:
            print("An error has ocurred")
            print(f"{e}")
            client.close()
            break

def write_messages():
    while True:
        message = f"{username}:{input('')}"
        client.send(message.encode("utf-8"))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()