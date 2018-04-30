from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys
import requests

class RPIClient:
    def receive(self):
        """ Handles receiving messages. """
        while True:
            try:
                msg = self.sock.recv(1024).decode("utf-8")
                print(msg,'\n')
            except OSError:  # Possibly client has left the chat.
                break

    def send(self,msg):
        """ Handles sending messages. """
        self.sock.sendall(msg.encode()+'\r\n'.encode())
        if msg == "!!@@quit":
            self.sock.close()
            self.connect()
        print('sent:',msg,'\n')

    def connect(self):
        ip='193.106.55.107'
        port = 5000
        ADDR=(ip,port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(ADDR)

        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        print('Connected to server: ',ip,':',port,'successfully')
        self.sock.sendall('elad@gmail.com 123 rasp'.encode()+'\r\n'.encode())

s=RPIClient()
s.connect()
        
        
