import socket
import threading
from threading import Thread # library for multi-threading

#HEADER = 64
#PORT = 5050
FORMAT = 'utf-8'
#SERVER = "10.42.0.21"#"127.0.1.1"
#ADDR = (SERVER, PORT)

DISCONNECT_MESSAGE = "!DISCONNECT"

class Client:
    def __init__(self, HEADER = 64, PORT = 5050, SERVER = "10.42.0.21"):
        self.mesg = "Hello!" # message to send to server
        self.HEADER = HEADER
        self.PORT = PORT
        self.SERVER = SERVER
        self.stopped = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # thread instantiation  
        #self.t = Thread(target=self.send, args=())
        #self.t.daemon = True # daemon threads run in background

    def start(self):
        ADDR = (self.SERVER, self.PORT)
        self.client.connect(ADDR)
        #self.t.start()
        self.send()

    def get_message(self, info):
        self.mesg = info
        self.send()

    def send(self):
        message = self.mesg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def stop(self):
        self.get_message(DISCONNECT_MESSAGE)
        print(self.client.recv(2048).decode(FORMAT))
        #self.t.join()


if __name__ == '__main__':
    check = Client(HEADER = 64, PORT = 5050, SERVER = "10.42.0.21")
    check.start()
    check.get_message("Hello World!")

    while True:

        mes = input()
        if mes == "q":
            check.get_message(DISCONNECT_MESSAGE)
            break
        else:
            check.get_message(mes)
