import pygame
Width = 500
Height = 500
Window = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Client")
NumOfClients = 0

class User():
    def __init__(self, X,Y,Width,Height,Color):
        self.x = X
        self.y = Y
        self.Width = Width
        self.Height= Height
        self.Color = Color
        self.Rectangle = (X,Y,Width,Height)
        self.vel = 3

    def Draw(self,Window):
        pygame.draw.rect(Window,self.Color,self.Rectangle)

    def Move(self):
        Input = pygame.key.get_pressed()
        if Input[pygame.K_LEFT]:
            self.x -=self.vel

        elif Input[pygame.K_RIGHT]:
            self.x += self.vel

        elif Input[pygame.K_UP]:
            self.y -= self.vel

        elif Input[pygame.K_DOWN]:
            self.y += self.vel
        self.Rectangle = (self.x,self.y,self.Width,self.Height)

def RedrawWindow(Window,User):
    Window.fill((255,255,255))
    User.Draw(Window)
    pygame.display.update()

def main():
    Run = True
    User1 = User(50,50,100,100,(0,255,0))
    

    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
                pygame.quit()
        User1.Move()
        RedrawWindow(Window,User1)
main()
