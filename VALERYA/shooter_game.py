#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
loste = 0
max_lost = 7
goal = 10
score = 0
win_width = 800
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load('background.jpg'), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font2 = font.SysFont('Arial', 45)
lost = font2.render('!!Ты проиграл!!',1,(255,0,0))
win = font2.render('!Победа!',1,(0,255,0))
 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,40,40,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global loste
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            loste = loste + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png',randint(80 ,win_width -80), -40,80,50,randint(1,5))
    monsters.add(monster)
ship = Player('playershooter.jpg',5,win_height-100,80,100,20)
bullets = sprite.Group()
finish = False
run = True
num_fire = 0
rel_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type ==KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire +1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time  == False:
                    last_time = timer()
                    rel_time  = True
    if not  finish :
        window.blit(background,(0, 0))
        text = font2.render('Убито:'+ str(score),1,(0,255,150))
        window.blit(text,(10,20))
        text_lose = font2.render('Пропущено:' + str(loste),1,(255,0,220))
        window.blit(text_lose,(10,50))
        ship.update()
        monsters.update()
        ship.reset()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                
                reload = font2.render('ждите,перезарядка...',1,(215,190,50))
                window.blit(reload,(100,230))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score = score+1
            monster = Enemy('ufo.png',randint(80 ,win_width -80), -40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or loste >= max_lost:
            finish = True
            window.blit(lost,(290,200)) 
        if score >= goal:
            finish = True
            window.blit(win,(290,200))


        display.update()
    time.delay(30)