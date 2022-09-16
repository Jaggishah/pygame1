from tkinter import font
import pygame
import random
import math
from pygame import mixer


#intiliazation
pygame.init()

#display
screen = pygame.display.set_mode((800,600))
#caption and icon
pygame.display.set_caption("Jupitor")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
run =True 

#background sound
mixer.music.load('back.mp3')
mixer.music.play(-1)
#player
playIMG=pygame.image.load("spaceship.png")
playerX = 355
playerY = 470
playerX_change = 0

def player(x,y):
    screen.blit(playIMG,(x,y))

#enemy making
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6 
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(64,736))
    enemyY.append(random.randint(64,110))
    enemyX_change.append(0.2)
    enemyY_change.append(10)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

#background 

backIMG = pygame.image.load("background.png")

#bullet

bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 420
bulletY_change = 0.8
bullet_state = "ready"
 
def bullet_fire(x,y):
   
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x+5,y+11))

# -------------------------------------------------------------
# gameover text

overtext = pygame.font.Font("freeshipping.ttf",50)

def game_overtext():
    gameovertext = overtext.render("GAME OVER", True ,(255,255,255))
    screen.blit(gameovertext,(290,220))

#score
score_value = 0
font = pygame.font.Font("freeshipping.ttf",30)
textX = 10
textY = 10
#show text
def show_text(x,y):
    score = font.render("SCORE:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

# -------------------------------------------------
def is_collison(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#loop for continous running

while run:
    screen.fill((0,0,0))
    screen.blit(backIMG,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #when key is pressing player change its position
        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                #only fire when one bullet iteration is bullet
                if bullet_state is "ready":
                    shotsound = mixer.Sound('Gun.mp3')
                    shotsound.play()
    
                    bulletX = playerX
                    bullet_fire(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #bullet movemnt
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state is "fire":
        bulletY -=bulletY_change
        bullet_fire(bulletX,bulletY)

    
    #enemy movements
    for i in range(num_of_enemies):
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_overtext()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        collison = is_collison(enemyX[i],enemyY[i],bulletX,bulletY)
        if collison:
            exsound = mixer.Sound('explosion.wav')
            exsound.play()
            bulletY = 420
            bullet_state = "ready"
            score_value += 1
            # print(score_value)
            enemyX[i] = random.randint(64,736)
            enemyY[i] = random.randint(64,110)

        enemy(enemyX[i] ,enemyY[i] ,i)


    #player movements 
    playerX += playerX_change
    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # whenever collision  is occur
    


    show_text(textX,textY)

    player(playerX,playerY)
    
    
    pygame.display.update()