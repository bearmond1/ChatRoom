import socket as S
import threading as T
from queue import Queue
import sys


client = S.socket(S.AF_INET,S.SOCK_STREAM)
# expecting chat server address in command line arguments
if len(sys.argv) == 3:
    client.connect((sys.argv[1],sys.argv[2]))
else:
    client.connect(("localhost",8888))


nickname = input("Choose a nickname: ")

message_queue = Queue()


def recieve():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            #print(message)
            match message[:3]:
                # just regular message, print it
                case "MSG":
                    print(message[3:])
                # password requested
                case "PWD":
                    print("Password requiered to enter chat.\n Enter the password: ")
                    password = input()
                    message_queue.put(("PWD" + password).encode("ascii"))
                # nickname occupied
                case "NIC":
                    print("Nickname is occupied, please choose another one")
                    nickname = input()
                    message_queue.put(("NIC" + nickname).encode("ascii"))
                # we`re good, staring reading input
                case "SUC":
                    T.Thread(target=read_input).start()
                case other:
                    print("other type of message: " + message)
        except Exception as e:
            print(f"An error occured {e.__dict__}")
            client.close()
            break


# sending messages from queue
def send():
    client.send(("NIC" + nickname).encode("ascii"))
    while True:
        if not message_queue.empty():
            message = message_queue.get()
            client.send(message)


# reading user input
def read_input():
    while True:
        message = "MSG" + input()
        message_queue.put(message.encode("ascii"))


recieve_thread = T.Thread(target=recieve)
recieve_thread.start()

send_thread = T.Thread(target=send)
send_thread.start()