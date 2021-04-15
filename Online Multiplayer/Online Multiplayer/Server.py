import pygame,sys
import numpy
import socket
import threading
import os
import time
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
CrossColor = (31, 46, 46)
# Colors
BG = (102, 102, 255)
#Line Properties
LCOLOR = (128, 32, 0)
LWIDTH=15
GameOver = False
title = "TIC TAC TOE"
Window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(title)
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
            y,x = int(data[0]),int(data[1])
            if data[2]=='switch':
                turn = True
            if data[3] == 'False':
                GameOver=True
            if FreeSpace(x,y):
                MarkSquare(x,y,2)
                DrawObjects()
            print(data)
        except:
            print("Error in client")
            print("Error: Press the top right Exit command")
            time.sleep(2)

def WaitingforConnection():
    global ConnectionMade, Conn,Addr
    Conn,Addr = Socket.accept()
    print("client is connected")
    ConnectionMade = True
    ReceivedData()

create_thread(WaitingforConnection)

Window.fill(BG)
Board = numpy.zeros((ROW,COLUMN))



# drawing grid
def DrawLines():
    ConstVal = 0 
    pygame.draw.line(Window,LCOLOR,(ConstVal,ConstSize),(WIDTH,ConstSize),LWIDTH)
    pygame.draw.line(Window,LCOLOR,(ConstVal,ConstSize2),(WIDTH,ConstSize2),LWIDTH)
    pygame.draw.line(Window,LCOLOR,(ConstSize,ConstVal),(ConstSize,HEIGHT),LWIDTH)
    pygame.draw.line(Window,LCOLOR,(ConstSize2,ConstVal),(ConstSize2,HEIGHT),LWIDTH)

#check if the space selected is free.
def FreeSpace(row,col):
    empty = 0
    if Board[row,col]==empty:
        return True
    else:
        return False
def DrawObjects():

    for Rows in range(ROW):
        User1 = 1
        User2 = 2
        for Colums in range(COLUMN):
            MathEq = Colums * ConstSize + CrossSpace
            MathEq2 =Rows * ConstSize + ConstSize - CrossSpace
            MathEq3 = Colums * ConstSize + ConstSize - CrossSpace
            MathEq4=Rows * ConstSize + CrossSpace
            if Board[Rows][Colums] ==User2:
                pygame.draw.line(Window,CrossColor,(MathEq, MathEq2), (MathEq3, MathEq4), CWidth)
                pygame.draw.line(Window,CrossColor,(MathEq, MathEq4), (MathEq3, MathEq2), CWidth)
            elif Board[Rows][Colums] ==User1:
                MathEq5 = Colums * ConstSize +remainder
                MathEq6=Rows * ConstSize+remainder
                pygame.draw.circle(Window,CColor,(int(MathEq5), int(MathEq6)), CRadius,CWidth)  

def MarkSquare(Row,Col,User):
    Board[Row][Col] = User

    #check if it is full
def CheckBoard():
    empty = 0
    for Rows in range(ROW):
        for Columns in range(COLUMN):
            if Board[Rows][Columns] == empty:
                return False
    return True
def CheckIfWinner(User):
    for row in range(ROW):
        Matheq1 = Board[row][0] == User and Board[row][1] ==User and Board[row][2] ==User
        if Matheq1:
            DrawWinningHorizontalLine(row,User)
            return True
    for Column in range(COLUMN):
        Matheq2 = Board[0][Column] == User and Board[1][Column] ==User and Board[2][Column] ==User
        if Matheq2:
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
    Player1 = 1
    Player2 = 2
    Space = 15

    HEIGHTDIFF = HEIGHT - Space
    if User == Player1:
        color = CColor
    elif User == Player2:
        color = CrossColor
    pygame.draw.line(Window,color,(X ,Space),(X,HEIGHTDIFF),Space)

def DrawWinningHorizontalLine(Column,User):
    Y = Column * ConstSize + remainder
    Player1 = 1
    Player2 = 2
    Space = 15
    WIDTHDIFF = WIDTH - Space
    if User == 1:
        color = CColor
    elif User == 2:
        color = CrossColor
    pygame.draw.line(Window,color,(Space ,Y),(WIDTHDIFF,Y),Space)

def drawAscendingDiagonal(User):
    Player1 = 1
    Player2 = 2
    WIDTHDIFF = WIDTH - 15
    HEIGHTDIFF = HEIGHT - 15
    Space = 15
    if User == Player1:
        color = CColor
    elif User == Player2:
        color = CrossColor
    pygame.draw.line(Window,color,(Space,HEIGHTDIFF),(WIDTHDIFF,Space),Space)


def drawDescendingDiagonal(User):
    Player1 = 1
    Player2 = 2
    Space = 15
    WIDTHDIFF = WIDTH - Space
    HEIGHTDIFF = HEIGHT - Space
    if User == Player1:
        color = CColor
    elif User == Player2:
        color = CrossColor
    pygame.draw.line(Window,color,(Space,Space),(WIDTHDIFF,HEIGHTDIFF),Space)

def restartGame():
    Window.fill(BG)
    DrawLines()
    User = 1
    for r in range(ROW):
        for c in range(COLUMN):
            Board[r][c]=0



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
                    send_data = '{}-{}-{}-{}'.format(CCol,CRow,'switch',playing).encode()
                    Conn.send(send_data)
                    turn = False
                except:
                    pass


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
exit(0)