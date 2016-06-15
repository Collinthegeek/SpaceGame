import pygame, sys, random
from pygame.locals import *
pygame.font.init
pygame.init()
screen = pygame.display.set_mode((550, 600))
health=5
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 550)
font = pygame.font.SysFont("monospace", 55)
pygame.display.set_caption('Space Game')
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
healthlabel = font.render(str(health), 1, (255,255,255))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('img/ship.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(275,500))
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-6, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('img/enemy.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(random.randint(0,550-32),0))
    def update(self):
        self.rect.move_ip(0, 2)
        if self.rect.bottom > 500:
            self.kill()
            health-=1
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('img/bullet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(player.rect.x+8,player.rect.y+8))
    def update(self):
        self.rect.move_ip(0, -8)
        if self.rect.right < 0:
            self.kill()
player = Player()
enemies = pygame.sprite.Group()
bullets=pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while True:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_SPACE:
                new_bullet = Bullet()
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        elif event.type == QUIT:
            sys.exit()
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.blit(background, (0, 0))
    screen.blit(healthlabel, (500, 10))
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    bullets.update()
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    if pygame.sprite.spritecollideany(player, enemies):
        health-=1
    if pygame.sprite.groupcollide(bullets, enemies, True, True, collided = None):
        pass
    if health==0:
        sys.exit()

    pygame.display.flip()
