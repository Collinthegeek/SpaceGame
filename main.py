import pygame, sys, random
from pygame.locals import *
from fractions import Fraction

#Setup
pygame.init()
pygame.mixer.init()
pygame.font.init
screen = pygame.display.set_mode((550, 800))
health=5
kills=0
deaths=0
bshoot=0
enbx=0
enby=0
enemytimer = 0 
bigenemytimer = 0
chesttimer = 0
difficulty = 1
gun=[0]
font = pygame.font.SysFont("monospace", 55)
pygame.display.set_caption('Space Game')
explosion=pygame.image.load("data/explosion.png")
explosionsnd = pygame.mixer.Sound('data/explosion.wav')
laser=pygame.mixer.Sound("data/laser.wav")
bell = pygame.mixer.Sound("data/bell.wav")
background = pygame.image.load("data/back.png")
healthlabel = font.render(str(health), 1, (255,255,255))

#Player
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.type = "player"
		self.shots = 0
		self.image = pygame.image.load('data/ship.png').convert()
		self.rect = self.image.get_rect(center=(275,700))
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
		self.shots+=1
		laser.play()
		for i in gun:
			new_bullet = Bullet(i, "player")
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
		
#Powerups
class Chest(pygame.sprite.Sprite):
	def __init__(self):
		super(Chest, self).__init__()
		self.type = "chest"
		self.image = pygame.image.load('data/chest.png').convert()
		self.rect = self.image.get_rect(
			center=(random.randint(0,550-32),0))
	def update(self):
		self.rect.move_ip(0, 2)
		if self.rect.bottom > 700:
			self.kill()

#Small Enemies
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.type = "enemy"
		self.image = pygame.image.load('data/enemy.png').convert()
		self.rect = self.image.get_rect(center=(random.randint(0,550-32),0))
	def update(self):
		global health
		global deaths
		self.rect.move_ip(0, 2)
		if self.rect.bottom > 700:
			self.kill()
			player.kill()

#Big Enemies
class BigEnemy(pygame.sprite.Sprite):
	def __init__(self):
		super(BigEnemy, self).__init__()
		self.type = "enemy"
		self.health = 1
		self.image = pygame.image.load('data/enemy2.png').convert()
		self.rect = self.image.get_rect(
			center=(random.randint(0,550-32),0))
	def update(self):
		global health
		global deaths
		global enbx
		global enby
		self.rect.move_ip(0, 1)
		if self.rect.bottom > 700:
			self.kill()
			player.kill()
		bshoot = random.randint(0,50)
		if bshoot == 1 & self.health == 1:
			enbx = self.rect.x
			enby = self.rect.y
			laser.play()
			new_enbullet = Bullet(0, "bigenemy")
			enbullets.add(new_enbullet)
			all_sprites.add(new_enbullet)
	def damage(self):
		if self.health==1:
			self.image = pygame.image.load('data/enemy2dmg.png').convert()
			explosionsnd.play()
			screen.blit(explosion, (self.rect.x+25,self.rect.y+70))
			pygame.display.flip()		
			pygame.time.delay(100)	
			self.health=0
		else:
			self.kill()

#Bullets
class Bullet(pygame.sprite.Sprite):
	def __init__(self, trajectory, source):
		super(Bullet, self).__init__()
		if source == "player":
			self.direction = -9
			self.center = player.rect.x+8,player.rect.y+8
		else:
			self.direction = 9
			self.center = enbx+42,enby+128
		self.type = "bullet"
		self.trajectory = trajectory
		self.image = pygame.image.load('data/bullet.png').convert()
		self.rect = self.image.get_rect(center=self.center)
	def update(self):
		self.rect.move_ip(self.trajectory, self.direction)
		if self.rect.right < 0:
			self.kill()

#Sprite groups for collision
player = Player()
players = pygame.sprite.Group()
players.add(player)
enemies = pygame.sprite.Group()
bigenemies = pygame.sprite.Group()
chests = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enbullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Main loop
while True:
	pygame.time.delay(20)
	
	#Controls
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				sys.exit()
			elif event.key == K_SPACE:
				player.shoot()
			elif event.key == K_o:
				new_bigenemy = BigEnemy()
				bigenemies.add(new_bigenemy)
				all_sprites.add(new_bigenemy)
			elif event.key == K_p:
				new_enemy = Enemy()
				enemies.add(new_enemy)
				all_sprites.add(new_enemy)
		elif event.type == QUIT:
			sys.exit()

	#Timers
	enemytimer+=1
	bigenemytimer+=1
	chesttimer+=1
	print "kills: " + str(kills)
	print "difficulty: " + str(difficulty)
	print "chest time: " + str(1200-chesttimer)
	print ""
	
	#Difficulty
	difficulty = 80-kills*(1.5-gun[0])
	if difficulty<4:
		difficulty=4

	#Enemy spawning
	if enemytimer>difficulty:
		new_enemy = Enemy()
		enemies.add(new_enemy)
		all_sprites.add(new_enemy)
		enemytimer = 0
	if bigenemytimer>difficulty*15:
		new_bigenemy = BigEnemy()
		bigenemies.add(new_bigenemy)
		all_sprites.add(new_bigenemy)
		bigenemytimer=0

	#Powerup spawning
	if chesttimer==1200:
		if gun!=[-2, -1, 0, 1, 2]:
			new_chest = Chest()
			chests.add(new_chest)
			all_sprites.add(new_chest)
		chesttimer=0

	#Collision	
	if pygame.sprite.groupcollide(bullets, enemies, True, True, collided = None):
		kills+=1
	for i in pygame.sprite.groupcollide(bigenemies, bullets, False, True, collided = None):
		i.damage()
		kills+=1
	if pygame.sprite.groupcollide(enbullets, players, True, False, collided = None):
		player.kill()
	if pygame.sprite.groupcollide(bullets, chests, True, True, collided = None):
		bell.play()
		if gun==[0]:
			gun = [-1, 1]
		elif gun==[-1, 1]:
			gun =[-2, 0, 2]
		elif gun==[-2, 0, 2]:
			gun = [-2, -1, 0, 1, 2]

	#Update sprites
	enemies.update()
	bigenemies.update()
	bullets.update()
	enbullets.update()
	chests.update()
	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys)

	#Scoring
	if player.shots-kills>0:
		score = kills-deaths+(kills/(player.shots-kills))
	else:
		score = 0
	healthlabel = font.render("Life: " + str(health), 1, (255,255,255))
	scorelabel = font.render("Score: " + str(score), 1, (255,255,255))
	screen.blit(background, (0, 0))
	screen.blit(healthlabel, (420, 750))
	screen.blit(scorelabel, (10, 750))
	for entity in all_sprites:
		screen.blit(entity.image, entity.rect)
	
	#Endgame
	if health==1:
		scorefile = open("data/hiscore", "r")
		for hi in scorefile.read().split():
			hiscore = int(hi)
		scorefile.close()

		finscorelabel = font.render("Score: "+str(score), 1, (255,255,255))
		hiscorelabel = font.render("Hi-Score: "+str(hiscore), 1, (255,255,255))
		screen.blit(background, (0,0))
		if score>hiscore:
			scorefile = open("data/hiscore", "w")
			screen.blit(font.render("New High Score!", 1, (255,255,255)), (50,150))
			screen.blit(finscorelabel, (50,250))
			screen.blit(hiscorelabel, (50,300))
			pygame.display.flip()
			scorefile.write(str(score))
			scorefile.close()
			pygame.time.delay(5000)
		else:
			screen.blit(font.render("Game Over :(", 1, (255,255,255)), (50,150))
			screen.blit(finscorelabel, (50,250))
			screen.blit(hiscorelabel, (50,300))
			pygame.display.flip()
			pygame.time.delay(5000)

		sys.exit()	
	pygame.display.flip()

