import socket as S
import threading as T
from config import get_config



config = get_config()

server = S.socket(S.AF_INET,S.SOCK_STREAM)
server.bind((config.host,config.port))
server.listen()


clients = {} # Dict{ nickname: (client,address) }
lock = T.Lock()


# send message to all chat members
def broadcast(message):
    prefix = "MSG".encode("ascii")
    for client_info in clients.items():
        print(f"sending message to {client_info[0]}")
        client_info[1][0].send(prefix + message)


# recieve chat member message or handle his leave
def client_handler(client,nickname):
    global clients
    global lock
    print(f"client handler started, {nickname}, {client} ")
    while True:
        try:
            print(clients.keys())
            message = client.recv(1024).decode("ascii")
            match message[:3]:
                case "MSG":
                    print("MSG recieved " + message)
                    broadcast((nickname + ": " + message[3:]).encode("ascii"))
                case other:
                    print("other type recieved: " + message)
        except:
            # remove from global list and close connection
            with lock:
                clients.pop(nickname)
            client.close()
            broadcast(f"{nickname} jeft chat".encode('ascii'))
            break


# add user to the chat
def add_user(client,address,nickname):
    global clients
    global lock
    with lock:
        clients.update({nickname: (client,address)})

    broadcast(f"{nickname} joined the chat".encode("ascii"))
    client.send("SUC".encode("ascii"))
    thread = T.Thread(target=client_handler,args=[client,nickname])
    thread.start()


def check_password(client):
    if config.password == "":
        return True
    else:
        client.send("PWD".encode("ascii"))
        password = client.recv(1024).decode("ascii")
        match password[:3]:
            case "PWD":
                if password[3:] == config.password:
                    return True
                else:
                    return False


# check if we ready to let new user in
def join_request_handler(client,address):
    nickname = client.recv(1024).decode("ascii")
    match nickname[:3]:
        case "NIC":
            if nickname[3:] in clients:
                client.send(("NIC").encode("ascii"))
                join_request_handler(client,address)
            if not check_password(client):
                client.send("PWD".encode("ascii"))
                join_request_handler(client,address)
            add_user(client,address, nickname[3:])
        case other:
            client.send(("NIC").encode("ascii"))
            join_request_handler(client,address)



# handling incoming connections
def recieve_connection():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        join_request_handler(client,address)


# startup
print("Server is up")
recieve_connection()