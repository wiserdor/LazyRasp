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
        ip='54.154.33.168'
        port = 5000
        ADDR=(ip,port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(ADDR)

        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        print('Connected to server: ',ip,':',port,'successfully')
        self.sock.sendall('Popcorn 1234 rasp'.encode()+'\r\n'.encode())

##    def register(self):
##        url="http://34.242.225.193:8080/sign"
##        f=requests.post(url,data={'username':'dor','password':'1234','enabled':'1'})
##        print(f)
  

        
        
