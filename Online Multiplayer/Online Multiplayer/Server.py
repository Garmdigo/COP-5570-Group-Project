
import socket
from _thread import *
import pickle
import sys

server = "192.168.0.17"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection")

def threaded_client(conn):
    conn.send(str.encode("connected"))
    #global idCount
    #conn.send(str.encode(str(p)))
    Multiply = 1
    reply = ""
    while True:
        try:
            data = conn.recv(2048*Multiply)
            reply= data.decode("utf-8")

            #if gameId in games:
            #    game = games[gameId]

            if not data:
                print("Disconencted")
                break
            else:
                print( "Received : ",reply)
                print( "Sent : ",reply)

                #if data == "reset":
                #    game.resetWent()
                #elif data != "get":
                #    game.play(p, data)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()
    #try:
    #    del games[gameId]
    #    print("Closing Game", gameId)
    #except:
    #    pass
    #idCount -= 1
    #conn.close()


#connected = set()
#games = {}
#idCount = 0


while True:
    conn= s.accept()
    addr = s.accept()
    print("Connected to:", addr)
    #idCount += 1
    #p = 0
    #gameId = (idCount - 1)//2
    #if idCount % 2 == 1:
    #    games[gameId] = Game(gameId)
    #    print("Creating a new game...")
    #else:
    #    games[gameId].ready = True
    #    p = 1


    start_new_thread(threaded_client,(conn,))