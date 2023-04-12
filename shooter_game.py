from pygame import *
from random import randint
from time import time as timer

finish = False
scht = 0
lost = 0
max_lost = 10
num_fire = 0
rel_time = False
lost_time = 0
now_time = 0
healthe = 5

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
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
        keys_pressed = key.get_pressed()    
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 450:
            self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.x = randint(0, 650)
            self.rect.y = -60
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 450:
            self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.x = randint(0, 700)
            self.rect.y = -60

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

#Приложение
window = display.set_mode((700, 500))
display.set_caption("galaxy.jpg")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

#Текст
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 50)
win = font2.render('YOU WIN!', True, (255, 215, 0))
loze = font2.render('YOU LOSE!', True, (180, 0, 0))
res = font2.render('Resault!', True, (255, 255, 0))

#Музыка
mixer.init()
mixer.music.load("space.ogg")
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#Спрайты

sp_Player = Player('rocket.png', 320, 420, 65, 65, 10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(1,4):
    monster = Enemy('ufo.png', randint(0, 650), -40, 65, 65, randint(3, 4))
    monsters.add(monster)

for i in range(1,3 ):
    asteroid = Asteroid('asteroid.png', randint(0, 650), -40, 65, 65, randint(3, 4))
    asteroids.add(asteroid)

#Игровой цикл
game = True
Clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    fire_sound.play()
                    sp_Player.fire()
                    num_fire = num_fire + 1

                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    lost_time = timer()
                    
    if not finish:
        window.blit(background, (0,0))
        coldes = sprite.groupcollide(monsters, bullets, True, True)
        for i in coldes:
            scht = scht + 1
            monster = Enemy('ufo.png', randint(0, 600), -40, 65, 65, randint(3, 6))
            monsters.add(monster)
        
        if sprite.spritecollide(sp_Player, monsters, True):
            monster = Enemy('ufo.png', randint(0, 600), -40, 65, 65, randint(3, 6))
            monsters.add(monster)
            healthe = healthe - 1

        if sprite.spritecollide(sp_Player, asteroids, True):
            asteroid = Asteroid('asteroid.png', randint(0, 650), -40, 65, 65, randint(3, 4))
            asteroids.add(asteroid)

            healthe = healthe - 1
        healthe_sch = font1.render('Жизни:' + str(healthe), 1, (255, 255, 255))
        window.blit(healthe_sch, (550, 20))
            
        if lost >= max_lost or healthe == 0:
            finish = True
            window.blit(loze, (200, 200))

        if scht >= 15:
            finish = True
            window.blit(win, (200, 200))

        if rel_time == True:
            now_time = timer()
            if now_time - lost_time <0.5:
                window.blit(res, (200, 200))
            else:
                
                rel_time = False
                num_fire = 0

        bullets.update()
        bullets.draw(window)
       
        text_scht = font1.render('Счёт:' + str(scht), 1, (255,255,255))
        window.blit(text_scht, (10,20))
        text_lost = font1.render('Пропущенно:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        sp_Player.update()
        sp_Player.reset()

        monsters.update()
        monsters.draw(window)

        asteroids.update()
        asteroids.draw(window)

        display.update()
        Clock.tick(60)