
#Создай собственный Шутер!
from time import time as timer
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, image_file, x, y, speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(image_file),(size_x, size_y))
        self.speed = speed
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - 85:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 7, self.rect.top, -15, 15, 20)
        bullets.add(bullet)




class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed


        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = -50
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self. rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

    

width =  700
height = 500
window = display.set_mode((width, height))
display.set_caption("СУПЕР УЛЬТРА ПУПЕР ДУПЕР МЕГА СУПЕР ШУТЕР 3Д 28КККК 300000")

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy1 = "1624095552183994239.png"
img_enemy2 = "asteroid.png"
img_bullet = "bullet.png"

background = transform.scale(image.load(img_back), (width, height))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg") 
  
   
finish = False

game = True

reload_bullets = False


score = 0
lost = 0
max_lost = 10
max_score = 20
life = 3
max_bullets = 5
num_bullet = 0


font.init()
font1 = font.SysFont("Arial", 20)
font2 = font.SysFont("Arial", 40)
win = font2.render("ТЫ ПАБЕДИЛ ПОПУСК!!!!", True, (255, 45, 69) )
lose = font2.render('ХАХАХАХААХХА, ТЫ ПРОИГРАЛ, ПОПУСК', True, (46, 72, 23))


clock = time.Clock()
FPS = 60
ship = Player(img_hero, width/2, height - 100, 10, 80, 100)


monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy1, randint(80, width - 80), -40, randint(1,5), 70, 70)
    monsters.add(monster)



asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(img_enemy2, randint(0, width - 50), -40, randint(1,7), 50, 50,)
    asteroids.add(asteroid)





bullets = sprite.Group()




while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_bullet < 5 and reload_bullets == False:
                    fire_sound.play()
                    ship.fire()
                    num_bullet += 1
                if num_bullet >= 5 and reload_bullets == False:
                    last_time = timer()
                    reload_bullets = True


    if finish != True:
        window.blit(background, (0,0))

        text = font1.render("Счет: " + str(score), True, (255, 150, 67)) 

        window.blit(text, (10,20))
        text_lose = font1.render("Попущено: " + str(lost), True, (255, 150, 67)) 

        window.blit(text_lose, (10,50))



        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)


        if reload_bullets == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font2.render("Жди попуск", True, (150,0,0))
                window.blit(reload_text, (260, 460))
            else:
                num_bullet = 0
                reload_bullets = False

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy1, randint(80, width - 80), -40, randint(1,5), 70, 70)
            monsters.add(monster)

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= max_score:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0,150,0)
        elif life == 2:
            life_color = (150,150,0)
        elif life == 1:
            life_color = (150,0,0)
        life_text = font2.render(str(life), True, life_color)
        window.blit(life_text, (650, 10))

    else:
        finish = False
        score = 0
        lost = 0
        num_bullet = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for a in asteroids:
            a.kill()
        for i in range(5):
            monster = Enemy(img_enemy1, randint(80, width - 80), -40, randint(1,5), 70, 70)
            monsters.add(monster)
        for i in range(3):
            asteroid = Enemy(img_enemy2, randint(0, width - 50), -40, randint(1,7), 50, 50,)
            asteroids.add(asteroid)
        
    display.update()
    clock.tick(FPS)




















































