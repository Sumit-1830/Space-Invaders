import random 
import os
import math
import time
import sys 
import pygame
from pygame.locals import * 
from pygame import mixer
pygame.init()


# creating window
screen_width = 800
screen_height = 600
fps = 40

gameWindow = pygame.display.set_mode((screen_width,screen_height))
background = pygame.image.load('gallery/sprites/bg3.jpg')
background = pygame.transform.scale(background,(screen_width,screen_height)).convert_alpha()
clock=pygame.time.Clock()

# background music
pygame.mixer.music.load("gallery/sounds/start.mp3")
mixer.music.play(-1)

# score
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
def show_score(x,y):
    score= font.render("Score: "+str(score_value),True,(255,255,255))
    gameWindow.blit(score,(x,y))


# To show caption and icon/logo
pygame.display.set_caption("Space Invaders")
icon= pygame.image.load('gallery/sprites/aircraft1.png')
pygame.display.set_icon(icon)


# To display the player
# playerImg= pygame.image.load('gallery/sprites/sc2.png')
playerImg= pygame.image.load('gallery/sprites/aircraft1.png')

# To display the bullet
bulletImg= pygame.image.load('gallery/sprites/bullet.png')


def player(x,y):
    gameWindow.blit(playerImg,(x,y))

def enemy(x,y,i):
    gameWindow.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    gameWindow.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt( (math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)) )
    if distance< 27:
        return True
    else:
        return False

def gameOver():
    # writng the new highscore in file
    # print("high score value is: ",highscore)
    with open("highScore.txt","w") as f:
        f.write(str(highscore))

    gameWindow.blit(background,(0,0))
    # game_over = pygame.font.Font('freesansbold.ttf',64)
    game_over = font.render("GAME OVER",True,(255,255,255))
    gameWindow.blit(game_over,(320,200))

    mixer.music.play(-1)

    if flag:
        message1 = font.render("Congratulations! New High Score is : "+str(score_value),True,(255,255,255))
        gameWindow.blit(message1,(100,250))
    else:
        message1 = font.render("Your Score is :"+str(score_value),True,(255,255,255))
        gameWindow.blit(message1,(300,250))

    message2 = font.render("Press Enter/Tab To Play",True,(255,255,255))
    gameWindow.blit(message2,(240,300))

    gameWindow.blit(playerImg,(370,400))
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE:
                    welcome()

        pygame.display.update()


def welcome():
    gameWindow.fill((255,255,255))
    while True:
        gameWindow.fill((0,0,0))
        gameWindow.blit(background,(0,0))
        message1 = font.render("Welcome to Space Invaders",True,(255,255,255))
        gameWindow.blit(message1,(200,200))
        message2 = font.render("Press Enter/Tab To Play",True,(255,255,255))
        gameWindow.blit(message2,(240,250))
        gameWindow.blit(playerImg,(370,400))
            
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE:
                    gameLoop()
                    
        pygame.display.update()


# game loop
def gameLoop():
    global playerX_change
    global playerY_change
    global playerX
    global playerY

    global enemyImg
    global enemyX
    global enemyY
    global enemyX_change
    global enemyY_change

    global bulletX
    global bulletY
    global bulletX_change
    global bulletY_change
    global bullet_state

    global score_value
    global highscore
    global flag
    global num_of_enemies

    score_value=0
    flag=False
    startTime=time.time()
    # global elapsedTime

    playerX=370
    playerY=480
    playerX_change=0
    playerY_change=0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = 4
    enemyY_change = 30
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('gallery/sprites/alien.png'))
        enemyX.append(random.randint(0,735))
        enemyY.append(random.randint(50,150))
        enemyX_change.append(4)
        enemyY_change.append(30)

    bulletX=0
    bulletY=480
    bulletX_change=0
    bulletY_change=10
    bullet_state= "ready"


    # checking if highscore file exists or not
    if( not os.path.exists("highScore.txt")):
        with open("highScore.txt","w") as f:
            f.write("0")

    with open("highScore.txt","r") as f:
        highscore=f.read()
        
    while True:
        # gameWindow.fill((255,255,255))
        gameWindow.fill((0,0,0))
        gameWindow.blit(background,(0,0))

        HighScore= font.render("High-Score: "+ str(highscore),True,(255,255,255))
        gameWindow.blit(HighScore,(550,10))

        
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            # Pressing Key Event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerX_change= 5
                
                if event.key == pygame.K_LEFT:
                    playerX_change= -5
                    
                if event.key == pygame.K_UP:
                    playerY_change=-5
                
                if event.key == pygame.K_DOWN:
                    playerY_change= 5

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        # adding bullet fire music
                        bullet_sound = mixer.Sound("gallery/sounds/fire.wav")
                        bullet_sound.play()

                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)

            if event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    playerX_change= 0
                if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    playerY_change= 0

        playerX += playerX_change
        playerY += playerY_change
       
        # setting x-axis boundary
        if playerX <=0:
            playerX=0
        elif playerX >=737:
            playerX=737
        # setting y-axis boundary
        if playerY <=0:
            playerY =0
        elif playerY >= 540:
            playerY=540
            

        # enemy movement
        for i in range(num_of_enemies):
            # if player touches enemy then game over
            if (enemyY[i] >440)  or  (abs(enemyY[i]-playerY)<=50 and abs(enemyX[i]-playerX)<=50):
                gameOver_sound = mixer.Sound("gallery/sounds/die.mp3")
                gameOver_sound.play()
                mixer.music.stop()
                elapsedTime = int(time.time()-startTime)
                quotient= int(elapsedTime/60)
                remainder= elapsedTime%60
                elapsedTime=str(quotient)+"."+str(remainder)

                stopScreen=True
                for j in range(num_of_enemies):
                    gameWindow.blit(enemyImg[j],(enemyX[j],enemyY[j]))

                gameWindow.blit(playerImg,(playerX,playerY))
                game_over_text = font.render("GAME OVER",True,(255,255,255))
                gameWindow.blit(game_over_text,(320,200))

                game_over_time = font.render("Time Taken: "+str(elapsedTime)+" Sec",True,(255,255,255))
                gameWindow.blit(game_over_time,(10,10))
                pygame.display.update()

                while stopScreen:
                    for event in pygame.event.get():
                        # if user clicks on cross button, close the game
                        if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                            pygame.quit()
                            sys.exit()

                        if event.type == KEYDOWN:
                            if event.key == K_RETURN or event.key == K_SPACE:
                                stopScreen=False
                                break
                gameOver()


            enemyX[i] += enemyX_change[i]
            if enemyX[i] <=0:
                enemyX_change[i]=4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >=737:
                enemyX_change[i]=-4
                enemyY[i] += enemyY_change[i]

            # checking collision
            collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
            if collision:
                # adding exploison music
                exploison_sound = mixer.Sound("gallery/sounds/points.mp3")
                exploison_sound.play()
                
                bulletY = playerY
                bullet_state="ready"
                score_value +=1
                if score_value>int(highscore):
                    highscore=score_value
                    flag = True
                # print(score)
                enemyX[i]=random.randint(0,735)
                enemyY[i]=random.randint(50,150)
                
            enemy(enemyX[i],enemyY[i],i)
            

        # bullet movement
        if bulletY <=0:
            bullet_state="ready"
            bulletY= playerY
            # bulletY = 480
        if bullet_state == "fire":
            fire_bullet(bulletX,bulletY)
            bulletY -= bulletY_change


        player(playerX,playerY)
        show_score(textX,textY)
        pygame.display.update()
        clock.tick(fps)
    
welcome()