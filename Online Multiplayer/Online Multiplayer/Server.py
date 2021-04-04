#import socket
#from _thread import *
#import pickle
#from Game import Game

#server = "192.168.0.17"
#port = 5555

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#try:
#    s.bind((server, port))
#except socket.error as e:
#    str(e)

#s.listen(2)
#print("Waiting for a connection, Server Started")

#connected = set()
#games = {}
#idCount = 0


#def threaded_client(conn, p, gameId):
#    global idCount
#    conn.send(str.encode(str(p)))

#    reply = ""
#    while True:
#        try:
#            data = conn.recv(4096).decode()

#            if gameId in games:
#                game = games[gameId]

#                if not data:
#                    break
#                else:
#                    if data == "reset":
#                        game.resetWent()
#                    elif data != "get":
#                        game.play(p, data)

#                    conn.sendall(pickle.dumps(game))
#            else:
#                break
#        except:
#            break

#    print("Lost connection")
#    try:
#        del games[gameId]
#        print("Closing Game", gameId)
#    except:
#        pass
#    idCount -= 1
#    conn.close()



#while True:
#    conn, addr = s.accept()
#    print("Connected to:", addr)

#    idCount += 1
#    p = 0
#    gameId = (idCount - 1)//2
#    if idCount % 2 == 1:
#        games[gameId] = Game(gameId)
#        print("Creating a new game...")
#    else:
#        games[gameId].ready = True
#        p = 1


#    start_new_thread(threaded_client, (conn, p, gameId))

import pygame,sys
import numpy
import socket
import threading
import os
os.environ['SDL_VIDEO_WINDOW_POS']='200,100'
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

pygame.init()
ROW = 3
COLUMN =3
#display settings
WIDTH = 800
HEIGHT = WIDTH
ConstSize = WIDTH//COLUMN
ConstSize2 = ConstSize * 2
remainder =  ConstSize//2
#Circle properties
CRadius = ConstSize//3
CWidth = 15
CColor = (239,231,200)
#Cross
CrossWidth = 25
CrossSpace = ConstSize//4
CrossColor = (66,66,66)
# Colors
RED = (255,0,0)
BG = (28,170,156)
#Line Properties
LCOLOR = (23,145,135)
LWIDTH=15
GameOver = False
Window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
HOST = '127.0.0.1'
PORT = 65432
ConnectionMade = False
Conn,Addr = None,None
Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Socket.bind((HOST,PORT))
Socket.listen(2)
User = 1
running = True
turn = True
playing = 'True'
def ReceivedData():
    global turn
    while True:
        try:
            data = Conn.recv(1024).decode()
            data = data.split('-')
            x,y = int(data[0]),int(data[1])
            if data[2]=='yourturn':
                turn = True
            if data[3] == 'False':
                GameOver=True
            if FreeSpace(x,y):
                MarkSquare(x,y,1)
            print(data)
        except:
            print("Error in Server")

def WaitingforConnection():
    global ConnectionMade, Conn,Addr
    Conn,Addr = Socket.accept()
    print("client is connected")
    ConnectionMade = True
    ReceivedData()

create_thread(WaitingforConnection)

Window.fill(BG)
Board = numpy.zeros((ROW,COLUMN))



#pygame.draw.line(Window,RED,(10,10),(300,300),10)
def DrawLines():
    pygame.draw.line(Window,LCOLOR,(0,ConstSize),(WIDTH,ConstSize),LWIDTH)
    pygame.draw.line(Window,LCOLOR,(0,ConstSize2),(WIDTH,ConstSize2),LWIDTH)
    pygame.draw.line(Window,LCOLOR,(ConstSize,0),(ConstSize,HEIGHT),LWIDTH)
    pygame.draw.line(Window,LCOLOR,(ConstSize2,0),(ConstSize2,HEIGHT),LWIDTH)
def FreeSpace(row,col):
    if Board[row,col]==0:
        return True
    else:
        return False
def DrawObjects():

    for Rows in range(ROW):
        for Colums in range(COLUMN):
            if Board[Rows][Colums] ==1:
                pygame.draw.circle(Window,CColor,(int(Colums * ConstSize +remainder), int(Rows * ConstSize+remainder)), CRadius,CWidth)
            elif Board[Rows][Colums] ==2:
                pygame.draw.line(Window,CrossColor,(Colums * ConstSize + CrossSpace, Rows * ConstSize + ConstSize - CrossSpace), (Colums * ConstSize + ConstSize - CrossSpace, Rows * ConstSize + CrossSpace), CWidth)
                pygame.draw.line(Window,CrossColor,(Colums * ConstSize + CrossSpace, Rows * ConstSize + CrossSpace), (Colums * ConstSize + ConstSize - CrossSpace, Rows * ConstSize + ConstSize - CrossSpace), CWidth)

def MarkSquare(Row,Col,User):
    Board[Row][Col] = User

    #check if it is full
def CheckBoard():
    for Rows in range(ROW):
        for Columns in range(COLUMN):
            if Board[Rows][Columns] ==0:
                return False
    return True
def CheckIfWinner(User):
    for row in range(ROW):
        if Board[row][0] == User and Board[row][1] ==User and Board[row][2] ==User:
            DrawWinningHorizontalLine(Column,User)
            return True
    for Column in range(COLUMN):
        if Board[0][Column] == User and Board[1][Column] ==User and Board[2][Column] ==User:
            DrawWinningVerticalLine(Column,User)
            return True
    if Board[0][0] == User and Board[1][1] == User and Board[2][2] == User:
        drawDescendingDiagonal(User)
        return True
    elif Board[2][0] == User and Board[1][1] == User and Board[0][2] == User:
        drawAscendingDiagonal(User)
        return True
   
    return False

def DrawWinningVerticalLine(Column,User):
    X = Column * ConstSize + remainder
    if User == 1:
        color = CColor
    elif User == 2:
        color = CrossColor
    pygame.draw.line(Window,color,(X ,15),(X,HEIGHT -15),15)
    
def DrawWinningHorizontalLine(Column,User):
    Y = Column * ConstSize + remainder
    if User == 1:
        color = CColor
    elif User == 2:
        color = CrossColor
    pygame.draw.line(Window,color,(15 ,Y),(WIDTH-15,Y),15)

def drawAscendingDiagonal(User):
    if User == 1:
        color = CColor
    elif User == 2:
        color = CrossColor
    pygame.draw.line(Window,color,(15,HEIGHT-15),(WIDTH-15,15),15)


def drawDescendingDiagonal(User):
    if User == 1:
        color = CColor
    elif User == 2:
        color = CrossColor
    pygame.draw.line(Window,color,(15,15),(WIDTH-15,HEIGHT -15),15)

def restartGame():
    Window.fill(BG)
    DrawLines()
    User = 1
    for r in range(ROW):
        for c in range(COLUMN):
            Board[r][c]=0


#print(CheckBoard())
#for row in range(ROW):
#    for col in range(COLUMN):
#        if Board[row][col] ==0:
#            MarkSquare(row,col,1)
#print(CheckBoard())

DrawLines()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and ConnectionMade:
            if turn and not GameOver:
                XAxis = event.pos[0]
                YAxis = event.pos[1]
                #ClickRow and column
                CRow =int( YAxis//ConstSize)
                CCol=int(XAxis//ConstSize)
                if FreeSpace(CRow,CCol):
                    MarkSquare(CRow,CCol,1)
                    if CheckIfWinner(User):
                        GameOver = True
                if GameOver:
                    playing = 'False'
                try:
                    send_data = '{}-{}-{}-{}'.format(CCol,CRow,'yourturn',playing).encode()
                    Conn.send(send_data)
                    turn = False
                except:
                    pass
            #if FreeSpace(CRow,CCol):
            #    if User ==1:
            #        MarkSquare(CRow,CCol,1)
            #        if CheckIfWinner(User):
            #            GameOver = True
            #        User = 2 
            #    elif User ==2:
            #        MarkSquare(CRow,CCol,2)
            #        if CheckIfWinner(User):
            #            GameOver = True
            #        User = 1

                DrawObjects()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                restartGame()
                GameOver = False
                playing = 'True'
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                print("Goodbye")
    pygame.display.update()