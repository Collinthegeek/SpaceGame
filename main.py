import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode([550,600])
left = False
right = False
shipx = 250+32
shipy = 500
mtck = 0
eny=0
bullety=500
fired=False
bullets = []
enemies = []
back = pygame.image.load("img/back.png")
ship = pygame.image.load("img/ship.png")

while True:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([shipx,500])
                fired=True
    mtck = 0
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if mtck == 0:
            mtck = 10
            shipx -= 8
        if shipx < -1:
            shipx = 0
    if keys[pygame.K_RIGHT]:
        if mtck == 0:
            mtck = 10
            shipx+= 8
        if shipx > 550:
            shipx = 550-32

    if mtck > 0:
        mtck -= 1
    screen.blit(back, [0, 0])
    eny+=1

    enemies.append(random.randint(0,550))
    for enemy in enemies :
        screen.blit(ship, [enemy, eny])

    if fired == True:
        bullety-=1
        for bullet in bullets :
            bullet[1]-=8
            screen.blit(ship, [bullet[0], bullet[1]])

    screen.blit(ship, [shipx, shipy])

    pygame.display.flip()
