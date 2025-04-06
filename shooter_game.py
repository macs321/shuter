#Створи власний Шутер!
import  random 
import pygame 
import time


WIDTH = 1200
HEIGHT = 600
SIZE = (WIDTH,HEIGHT)
FPS = 60

score = 0
lost = 0
lives = 5
perezarad = 3
time1 = 5


win = pygame.display.set_mode(SIZE)

backgoround = pygame.transform.scale(
                pygame.image.load("galaxy.jpg"),
                SIZE
)

pygame.display.set_caption("Другий рівень підвалу порошенка,"
"він послав свої космічні цукерки по вас")
clock = pygame.time.Clock()



pygame.mixer.init()
#  pygame.mixer_music.load("space.ogg")
# pygame.mixer_music.play()

bullets = pygame.sprite.Group()
fire_sound = pygame.mixer.Sound("fire.ogg")


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename:str, size:tuple[int,int], coords:tuple[int,int], speed:int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename),size)
        self.rect =self.image.get_rect(center=coords)
        self.speed = speed
    
    def reset(self, window:pygame.Surface):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_UP] and self.rect.y >=0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.y <= HEIGHT - self.rect.height:
            self.rect.y += 5
        if keys[pygame.K_RIGHT]and self.rect.x <= WIDTH - self.rect.width:
            self.rect.x += 10
        if keys[pygame.K_LEFT]and self.rect.x >= 0:
            self.rect.x -= 10
    def fire(self):
        new_bullet = Bullet("bullet.png",
                             (15,20),
                             (self.rect.centerx,self.rect.top),
                             20
                             )
        bullets.add(new_bullet)
        fire_sound.play()


    def fire_3(self):
        bullets.add(
            (
                Bullet("bullet.png",(20,25),self.rect.topleft,15),
                Bullet("bullet.png",(20,25),(self.rect.centerx,self.rect.right),15),
                Bullet("bullet.png",(20,25),(self.rect.topright),15)
            )
        )
        global perezarad
        perezarad -=1
        
        

        fire_sound.play()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(50,WIDTH-50)
            global lost
            lost += 1

 # if self.rect.y = self.bullets and self.rect.x = self.bullets:


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

pygame.font.init()

medium_font = pygame.font.SysFont("Helvetica", 24)
big_font = pygame.font.SysFont("Impact",24)
perez_font = pygame.font.SysFont("Helvetica",24)

player =Player("rocket.png",(50,70),(HEIGHT//2,WIDTH//2),10)

enemies = pygame.sprite.Group()
enemies_num = 3

for i in range(enemies_num):
    n = random.randint(1,1000)
    if n >200:
        new_enemy = Enemy("ufo.png",
                    (70,50),
                    (random.randint(50,WIDTH-50),0),
                    random.randint(7,13)
                    )
    else:
        new_enemy =Enemy("asteroid.png",
                        (70,50),
                        (random.randint(50,WIDTH-50),0),
                        random.randint(7,13)
                        )
    enemies.add(new_enemy)

game = True
finish = False
restart = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key ==  pygame.K_SPACE:
                player.fire()
            if event.key == pygame.K_r and finish:
                restart = True
            if event.key == pygame.K_LSHIFT:
                if perezarad > 0:
                    player.fire_3()
                
                    





    if not finish and not restart:
        win.blit(backgoround,(0,0))

        lost_text = medium_font.render("пропущено зелених:" + str(lost), True, (255,255,255))
        win.blit(lost_text,(0,0))

        score_text = medium_font.render("Збито зелених:" + str(score), True, (255,255,255))
        win.blit(score_text,(0,25))

        lives_text = medium_font.render("життя" + str(lives), True, (255,25,55))
        win.blit(lives_text,(WIDTH-100,0))

        if perezarad <= 0:
            perez_text = perez_font.render("Зачекайте,перезарядка нерошенних цукерок",True,(255,0,0))
            win.blit(perez_text,(WIDTH//2-180,HEIGHT-100))
            

        player.update()
        player.reset(win)
        enemies.update()
        enemies.draw(win)
        bullets.update()
        bullets.draw(win)

        

        collided = pygame.sprite.groupcollide(enemies,bullets,True,True)
        for dead_enemy in collided:
            score += 1
            n = random.randint(1,1000)
            if n >200:
                new_enemy = Enemy("ufo.png",
                                (70,50),
                            (random.randint(50,WIDTH-50),0),
                            random.randint(7,13)
                            )
            else:
                new_enemy =Enemy("asteroid.png",
                                (70,50),
                                (random.randint(50,WIDTH-50),0),
                                random.randint(7,13)
                                )
            enemies.add(new_enemy)
            

        if score >= 11:
            finish = True
            win_text = big_font.render("Ти переміг ти втік від Порошенка",True,(0,255,0))
            win.blit(win_text,(WIDTH//2-200,HEIGHT//2))

            
        if  lost >= 20 or lives <= 0:
            finish = True
            lodt_text = big_font.render("Порошенко і його цукерки догнали тебе,не ростраюйся",True,(255,0,0))
            win.blit(lodt_text,(WIDTH//2-250,HEIGHT//2))

        collided = pygame.sprite.spritecollide(player,enemies, True)
        for enemy in collided:
            lives -= 1
            n = random.randint(1,1000)
            if n >200:
                new_enemy = Enemy("ufo.png",
                                (70,50),
                            (random.randint(50,WIDTH-50),0),
                            random.randint(7,13)
                            )
            else:
                new_enemy =Enemy("asteroid.png",
                                (70,50),
                                (random.randint(50,WIDTH-50),0),
                                random.randint(7,13)
                                )
            enemies.add(new_enemy)
    if restart:
        score = 0
        lost = 0 
        lives = 5
        enemies.empty()
        bullets.empty
        finish = False
        restart = False

        for i in range(enemies_num):
            n = random.randint(1,1000)
            if n >200:
                new_enemy = Enemy("ufo.png",
                            (70,50),
                            (random.randint(50,WIDTH-50),0),
                            random.randint(7,13)
                            )
            else:
                new_enemy =Enemy("asteroid.png",
                                (70,50),
                                (random.randint(50,WIDTH-50),0),
                                random.randint(7,13)
                                )
            enemies.add(new_enemy)

    

 

    pygame.display.update()

    clock.tick(FPS)