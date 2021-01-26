#!/usr/bin/env python
# coding: utf-8

# # Projekt
# # Ihor Kostiuk 255915

# In[5]:


import pygame
import time
from pygame.locals import *
import os.path
import sys

#-----------------------------------------------------------------------
# Parametry programu
#-----------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
I = 1
WHITE = (255,255,255)
GREENYELLOW = (143,245,34)
DARKGREY = (93,94,94)

#-----------------------------------------------------------------------
# Funkcje pomocnicze
#-----------------------------------------------------------------------
def loadImage(name, useColorKey=False):
    """ Załaduj obraz i przekształć go w powierzchnię.

    Funkcja ładuje obraz z pliku i konwertuje jego piksele 
    na format pikseli ekranu. Jeśli flaga useColorKey jest 
    ustawiona na True, kolor znajdujący się w pikselu (0,0)
    obrazu będzie traktowany jako przezroczysty (przydatne w 
    przypadku ładowania obrazów statków kosmicznych)
    """
    fullname = os.path.join("data",name)
    image = pygame.image.load(fullname)  #plik -> płaszczyzna
    image = image.convert() #przekonwertuj na format pikseli ekranu
    if useColorKey is True:
        colorkey = image.get_at((0,0)) #odczytaj kolor w punkcie (0,0)
        image.set_colorkey(colorkey,RLEACCEL) # ustaw kolor jako przezroczysty
    return image

def loadSound(name):
    """
    Funkcja pobiera audio
    Args:
    -name - śćieżka do audio
    """
    fullname = os.path.join("data",name)
    sound = pygame.mixer.Sound(fullname)
    return sound

#-----------------------------------------------------------------------------
# Klasy obiektów
#-----------------------------------------------------------------------------
class MyHelicopter(pygame.sprite.Sprite):
    def __init__(self):
        # Inicjalizuje klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("C://Users//DellUsers//Desktop//Programowanie//Projekt//helicopter.jpg",True)
        self.rect = self.image.get_rect() #rozmiar rysunku
        self.rect.center = (SCREEN_WIDTH/7,0.05*SCREEN_HEIGHT) #gdzie wstawić?
        self.x_velocity = 0
        self.y_velocity = 0
        self.shoot = True
    #wspomagające funkcje
    def ready_to_shoot(self): 
        self.shoot = True
    
    def reloading(self):
        self.shoot = False
    
    def shouting_condition(self):
        return self.shoot

    def update(self):
        self.rect.move_ip((self.x_velocity,self.y_velocity)) #move in-place
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH: 
            self.rect.right = SCREEN_WIDTH/100 
            self.rect.top = self.rect.top + SCREEN_HEIGHT/20 #obniża helikopter
            self.shoot = True #daje bombę
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


#-------------------------
# Klasa MyFighterLaser
#-------------------------
class MyHelicopterBomb(pygame.sprite.Sprite):

    def __init__(self,startpos):
        #inicjalizuje klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("C://Users//DellUsers//Desktop//Programowanie//Projekt//bomb.jpg",True)
        self.rect = self.image.get_rect()
        self.rect.center = startpos
    
    def update(self):
        if self.rect.bottom <= 0:
            self.kill()
        else:
            self.rect.move_ip((0,2)) #move bomb
            
#--------------------
# Klasa EnemyFighter
#--------------------

class House_box(pygame.sprite.Sprite):
    def __init__(self,startx, starty):
        #inicjalizuje klasę bazową
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("C://Users//DellUsers//Desktop//Programowanie//Projekt//1_box.jpg", True)
        self.x_1 = startx
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        
#-------------------------------
# Klasa ScoreBoard
#------------------------------        
class House(pygame.sprite.Sprite):
    def __init__(self,startx, n):
        self.n_flor = n
        self.xstart = startx
        self.hose1 = []
        for i in range(self.n_flor):
            self.hose1.append(House_box(self.xstart, 540 + i*300))

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self):
        #inicjalizuj klasę bazową
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.text = "Hits: %4d" % self.score #wyświetla score
        self.font = pygame.font.SysFont(None,50)
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.score += 1
        self.text = "Hits: %4d" % self.score 
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = self.image.get_rect()
    
    def give_score(self):
        return self.score


## MENU

def draw_text(surface, text, size, x, y, color):
    """rysuje tekst na tle"""
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

    
def menu():
    """Funkcja wyświetla menu glówne"""
    background = pygame.image.load('C://Users//DellUsers//Desktop//Programowanie//Projekt//bg.jpg').convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
    draw_text(screen, "PRESS [ENTER] TO BEGIN", 35, SCREEN_WIDTH/2, SCREEN_WIDTH/9, DARKGREY)
    draw_text(screen, "PRESS [Q] TO QUIT", 35, SCREEN_WIDTH/2, (SCREEN_WIDTH/8) + 50, DARKGREY)
    draw_text(screen,"In the game. Player will control 1 helicopter to drop bombs at the building below in city"
              ,20, SCREEN_WIDTH/2, SCREEN_WIDTH/2.7, DARKGREY)
    draw_text(screen,"you have to plan where to drop the bomb or you'll hit them soon!"
              ,20, SCREEN_WIDTH/2, SCREEN_WIDTH/2.5, DARKGREY)
    draw_text(screen,"Your helicopter gradually approaches the ground every time it moves across the screen."
              ,20, SCREEN_WIDTH/2, SCREEN_WIDTH/2.3, DARKGREY)
    draw_text(screen,"Drop bombs on the buildings before you crash into them. Bombs can only be dropped one at a time."
              ,20, SCREEN_WIDTH/2, SCREEN_WIDTH/2.1, DARKGREY)
    draw_text(screen,"Kostiuk Ihor (255915)"
              ,25, SCREEN_WIDTH/2, SCREEN_WIDTH/2, DARKGREY)
    draw_text(screen, "SHOOT: PRESS [SPACE] ", 35, SCREEN_WIDTH/2, (SCREEN_WIDTH/5.8) + 50, DARKGREY)
    pygame.display.update()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()   
def win_window():
    """Funkcja wyświetla menu kiedy gracz wygrywa"""
    background = pygame.image.load('C://Users//DellUsers//Desktop//Programowanie//Projekt//bg.jpg').convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
    draw_text(screen, "Game Over: You have successfully completed the first level!", 35, 
              SCREEN_WIDTH/2, SCREEN_WIDTH/10, DARKGREY)
    draw_text(screen, "PRESS [Q] TO QUIT", 35, SCREEN_WIDTH/2, (SCREEN_WIDTH/7) + 50, DARKGREY)
    draw_text(screen, "Your score:%4d" % score_board.give_score(), 35, SCREEN_WIDTH/2, (SCREEN_WIDTH/10) + 50, DARKGREY)
    pygame.display.update()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit() 
def lose_window():
    """Funkcja wyświetla menu kiedy gracz przegrywa"""
    background = pygame.image.load('C://Users//DellUsers//Desktop//Programowanie//Projekt//bg.jpg').convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
    draw_text(screen, "Game Over: You lost", 35, SCREEN_WIDTH/2, SCREEN_WIDTH/10, DARKGREY)
    draw_text(screen, "Your score:%4d" % score_board.give_score(), 35, SCREEN_WIDTH/2, (SCREEN_WIDTH/10) + 50, DARKGREY)
    draw_text(screen, "PRESS [Q] TO QUIT", 35, SCREEN_WIDTH/2, (SCREEN_WIDTH/7) + 50, DARKGREY)
    pygame.display.update()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit() 
    


#------------------------------------------------------------------------
# Właściwy program
#-----------------------------------------------------------------------
# Inicjalizacja PyGame

pygame.init()

# Stwórz okno 
screen = pygame.display.set_mode(SCREEN_SIZE) 
pygame.display.set_caption("Best shooter ever")

# Załaduj plik z tłem
background_image = loadImage("C://Users//DellUsers//Desktop//Programowanie//Projekt//bg.jpg")
screen.blit(background_image,(0,0))

# Załaduj pliki audio
myhelicopterShotFX = loadSound("C://Users//DellUsers//Desktop//Programowanie//Projekt//bomb.wav")
explodeFX = loadSound("C://Users//DellUsers//Desktop//Programowanie//Projekt//boom.wav")
endFx = loadSound("C://Users//DellUsers//Desktop//Programowanie//Projekt//End.wav")
winFx = loadSound("C://Users//DellUsers//Desktop//Programowanie//Projekt//win.wav")
pygame.mixer.music.load("C://Users//DellUsers//Desktop//Programowanie//Projekt//helicopter.wav") 



# Inicjalizuj statek gracza
myhelicopterSprite = pygame.sprite.RenderClear() #kontener na helikopter gracza
myhelicopter = MyHelicopter()                       #stwórz helikopter
myhelicopterSprite.add(myhelicopter)                #dodaj go do grupy
myhelicopterBombSprites = pygame.sprite.RenderClear() #kontener dla bomb

HouseBoxSprites = pygame.sprite.RenderClear() #kontener dla helikopterów


# Inicjalizuj licznik trafień
scoreboardSprite = pygame.sprite.RenderClear()
score_board = ScoreBoard()
scoreboardSprite.add(score_board)
scoreboardSprite.draw(screen)
pygame.display.flip()


#dodawanie domów o różnych piętrach
for i in range(3):
    HouseBoxSprites.add(House_box(250, 540 - i*50))
    HouseBoxSprites.add(House_box(450, 540 - i*50))
    HouseBoxSprites.add(House_box(650, 540 - i*50))
for i in range(1):
    HouseBoxSprites.add(House_box(150, 540 - i*50))
for i in range(1):
    HouseBoxSprites.add(House_box(350, 540 - i*50))
for i in range(2):
    HouseBoxSprites.add(House_box(550, 540 - i*50))


# Inicjalizuj zmienne kontrolne

clock = pygame.time.Clock()
addhouseCounter = 0
score = 0


show_menu = True 
running = True
while running:
    if show_menu:
        menu() #pokaż menu
        pygame.time.delay(1500)
        show_menu = False #zamknij menu
        screen.blit(background_image,(0,0)) #stwórz screen
        draw_text(screen, "Lives : 1", 35, SCREEN_WIDTH/10, (SCREEN_WIDTH/25) + 50, DARKGREY) #dodaję ilość żyć
    pygame.mixer.music.play(1,0.0) #włącz audio helikoptera
    myhelicopter.x_velocity = 3 #szybkość helikoptera
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and myhelicopter.shouting_condition(): #po naciśnięciu przycisku zrzuć bombę
                myhelicopterBombSprites.add(MyHelicopterBomb(myhelicopter.rect.midtop))
                myhelicopter.reloading() #tylko jedna bomba
                myhelicopterShotFX.play()
        if score_board.give_score() == 13:
            screen.blit(background_image,(0,0))
            winFx.play()
            win_window() #otwórz menu kiedy gracz wygrywa
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                myhelicopter.x_velocity = 0 
            elif event.key == K_RIGHT:
                myhelicopter.x_velocity = 0
            elif event.key == K_UP:
                myhelicopter.y_velocity = 0
            elif event.key == K_DOWN:
                myhelicopter.y_velocity = 0
    time.sleep(0.01)

    #Aktualizuj wszystkie sprite'y
    myhelicopterSprite.update()
    myhelicopterBombSprites.update()
    HouseBoxSprites.update()

    

    #Sprawdź, czy domy zostały trafione
    for hit in pygame.sprite.groupcollide(HouseBoxSprites,myhelicopterBombSprites,1,1):
        explodeFX.play()
        score += 1
        scoreboardSprite.update()
        scoreboardSprite.clear(screen, background_image)
        scoreboardSprite.draw(screen)
        pygame.display.flip()
    
    #Sprawdź, czy helikopter gracza został trafiony
    for hit in pygame.sprite.groupcollide(myhelicopterSprite,HouseBoxSprites,1,1):
        explodeFX.play()
        screen.blit(background_image,(0,0))
        pygame.mixer.music.stop()
        endFx.play()
        print("Koniec gry")
        lose_window()
    #Nie niszcz licznika
    for hit in pygame.sprite.groupcollide(scoreboardSprite,myhelicopterBombSprites,0,1):
        pass

    for hit in pygame.sprite.groupcollide(HouseBoxSprites,scoreboardSprite,0,0):
        hit.x_velocity = -hit.x_velocity
        hit.y_velocity = -hit.y_velocity
    

    #Wyczyść ekran
    myhelicopterBombSprites.clear(screen, background_image)
    myhelicopterSprite.clear(screen, background_image)
    HouseBoxSprites.clear(screen, background_image)


    #Rysuj sprite'y na ekranie
    myhelicopterBombSprites.draw(screen) 
    myhelicopterSprite.draw(screen)
    HouseBoxSprites.draw(screen)


    pygame.display.flip()


# In[ ]:




