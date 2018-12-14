import pygame, sys, random
from pygame.locals import *
from fractions import Fraction

pygame.init()
pygame.mixer.init()
pygame.font.init
screen = pygame.display.set_mode((550, 800))
health=5
shots=0
misses=0
kills=0
deaths=0
bshoot=0
enbx=0
enby=0
gun=[0]
enemytimer=900
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, enemytimer)
ADDBIGENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBIGENEMY, 2550)
ADDCHEST = pygame.USEREVENT + 3
pygame.time.set_timer(ADDCHEST, 5100)
font = pygame.font.SysFont("monospace", 55)
pygame.display.set_caption('Space Game')
explosion=pygame.image.load("img/explosion.png")
explosionsnd = pygame.mixer.Sound('img/explosion.wav')
laser=pygame.mixer.Sound("img/laser.wav")
background = pygame.image.load("img/back.png")
healthlabel = font.render(str(health), 1, (255,255,255))

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.type = "player"
		self.image = pygame.image.load('img/ship.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(
			center=(275,750))
	def update(self, pressed_keys):
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-8, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(8, 0)
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > 550:
			self.rect.right = 550
	def shoot(self):
		laser.play()
		for i in gun:
			new_bullet = Bullet(i)
			bullets.add(new_bullet)
			all_sprites.add(new_bullet)
	def kill(self):
		global health
		global deaths
		explosionsnd.play()
		for entity in enemies:
			screen.blit(entity.image, entity.rect)
		screen.blit(explosion, (player.rect.x-4,player.rect.y))
		pygame.display.flip()
		pygame.time.delay(500)
		for sprite in all_sprites:
			if sprite.type!="player":
				sprite.kill()
		health-=1
		deaths+=1
		
			
class Chest(pygame.sprite.Sprite):
	def __init__(self):
		super(Chest, self).__init__()
		self.type = "chest"
		self.image = pygame.image.load('img/chest.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(
			center=(random.randint(0,550-32),0))
	def update(self):
		self.rect.move_ip(0, 2)
		if self.rect.bottom > 750:
			self.kill()


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.type = "enemy"
		self.image = pygame.image.load('img/enemy.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(
			center=(random.randint(0,550-32),0))
	def update(self):
		global health
		global deaths
		self.rect.move_ip(0, 2)
		if self.rect.bottom > 750:
			self.kill()
			player.kill()

class BigEnemy(pygame.sprite.Sprite):
	def __init__(self):
		super(BigEnemy, self).__init__()
		self.type = "enemy"
		self.image = pygame.image.load('img/enemy2.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(
			center=(random.randint(0,550-32),0))
	def update(self):
		global health
		global deaths
		global enbx
		global enby
		self.rect.move_ip(0, 1)
		if self.rect.bottom > 750:
			self.kill()
			player.kill()
		bshoot = random.randint(0,50)
		if bshoot == 1:
			enbx = self.rect.x
			enby = self.rect.y
			laser.play()
			new_enbullet = EnBullet()
			enbullets.add(new_enbullet)
			all_sprites.add(new_enbullet)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, trajectory):
		super(Bullet, self).__init__()
		self.type = "bullet"
		self.trajectory = trajectory
		self.image = pygame.image.load('img/bullet.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(player.rect.x+8,player.rect.y+8))
	def update(self):
		self.rect.move_ip(self.trajectory, -9)
		if self.rect.right < 0:
			self.kill()

class EnBullet(pygame.sprite.Sprite):
	def __init__(self):
		super(EnBullet, self).__init__()
		self.type = "bullet"
		self.image = pygame.image.load('img/bullet.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(enbx+42,enby+128))
	def update(self):
		self.rect.move_ip(0, 9)
		if self.rect.right < 0:
			self.kill()

player = Player()
players = pygame.sprite.Group()
players.add(player)
enemies = pygame.sprite.Group()
chests = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enbullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while True:
	pygame.time.delay(20)
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				sys.exit()
			elif event.key == K_SPACE:
				player.shoot()
			elif event.type == QUIT:
				sys.exit()
		elif event.type == ADDENEMY:
			new_enemy = Enemy()
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)
		elif event.type == ADDBIGENEMY:
			new_bigenemy = BigEnemy()
			enemies.add(new_bigenemy)
			all_sprites.add(new_bigenemy)
		elif event.type == ADDCHEST:
			new_chest = Chest()
			chests.add(new_chest)
			all_sprites.add(new_chest)
	
	healthlabel = font.render(str(health), 1, (255,255,255))
	enemies.update()
	bullets.update()
	enbullets.update()
	chests.update()
	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys)


	screen.blit(background, (0, 0))
	screen.blit(healthlabel, (500, 10))
	for entity in all_sprites:
		screen.blit(entity.image, entity.rect)
	
	if pygame.sprite.groupcollide(bullets, enemies, True, True, collided = None):
		kills+=1
		#if random.randint(0,1) == 1:
		#	gun+=1
	
	if pygame.sprite.groupcollide(enbullets, players, True, False, collided = None):
		player.kill()
	if pygame.sprite.groupcollide(bullets, chests, True, True, collided = None):
		if gun==[0]:
			gun = [-2, 0, 2]		
		elif gun==[-2, 0, 2]:
			gun = [-3, -1, 0, 1, 3]
		elif gun==[-3, -1, 0, 1, 3]:
			gun = [-4, -2, -1, 0, 1, 2, 4]
	if health==0:
		if shots != 0 & deaths != 0:
			kdr = Fraction(kills, deaths)
			hmr = Fraction(kills, shots-kills)
		else:
			kdr = Fraction(1,1)
			hmr = Fraction(1,1)

		kdrlabel = font.render("KDR - "+str(kdr.numerator)+":"+str(kdr.denominator), 1, (255,255,255))
		hmrlabel = font.render("HMR - "+str(hmr.numerator)+":"+str(hmr.denominator), 1, (255,255,255))		
		screen.blit(background, (0,0))
		screen.blit(font.render("You Failed", 1, (255,255,255)), (50,150))
		screen.blit(kdrlabel, (50,250))
		screen.blit(hmrlabel, (50,350))
		pygame.display.flip()
		pygame.time.delay(5000)
		sys.exit()

	pygame.display.flip()

