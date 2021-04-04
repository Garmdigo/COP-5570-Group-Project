import pygame,sys
import numpy 
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
User = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and not GameOver:
            XAxis = event.pos[0]
            YAxis = event.pos[1]
            #ClickRow and column
            CRow =int( YAxis//ConstSize)
            CCol=int(XAxis//ConstSize)
            if FreeSpace(CRow,CCol):
                if User ==1:
                    MarkSquare(CRow,CCol,1)
                    if CheckIfWinner(User):
                        GameOver = True
                    User = 2 
                elif User ==2:
                    MarkSquare(CRow,CCol,2)
                    if CheckIfWinner(User):
                        GameOver = True
                    User = 1
                DrawObjects()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                restartGame()
                GameOver = False
    pygame.display.update()