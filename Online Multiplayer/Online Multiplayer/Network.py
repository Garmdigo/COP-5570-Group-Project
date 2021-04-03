
import socket
import pickle as P


class Network:
    def __init__(self):
        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Server =  "192.168.0.17"
        self.Port = 5555
        self.Addr = (self.Server, self.Port)
        self.ID = self.connect()
        print(self.ID)
    #def getP(self):
    #    return self.p

    def connect(self):
        try:
            self.Client.connect(self.Addr)
            return self.Client.recv(2048).decode()
        except:
            pass

    #def send(self, data):
    #    try:
    #        self.Client.send(str.encode(data))
    #        Multiply = 2
    #        return P.loads(self.Client.recv(2048* Multiply))
    #    except socket.error as e:
            #print(e)
n = Network()

