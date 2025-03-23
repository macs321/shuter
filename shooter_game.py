#Створи власний Шутер!
import  random 
import pygame 

WIDTH = 1200
HEIGHT = 600
SIZE = (WIDTH,HEIGHT)
FPS = 60

score = 0
lost = 0



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
            self.rect.x += 7
        if keys[pygame.K_LEFT]and self.rect.x >= 0:
            self.rect.x -= 7
    def fire(self):
        new_bullet = Bullet("bullet.png",
                             (15,20),
                             (self.rect.centerx,self.rect.top),
                             20
                             )
        bullets.add(new_bullet)
        fire_sound.play()



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(50,WIDTH-50)
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

pygame.font.init()

medium_font = pygame.font.SysFont("Helvetica", 24)


player =Player("rocket.png",(50,70),(HEIGHT//2,WIDTH//2),10)

enemies = pygame.sprite.Group()
enemies_num = 3

for i in range(enemies_num):
    new_enemy = Enemy("ufo.png",
                       (70,50),
                       (random.randint(50,WIDTH-50),0),
                       random.randint(7,13)
                       )
    enemies.add(new_enemy)

game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key ==  pygame.K_SPACE:
                player.fire()



    if not finish:
        win.blit(backgoround,(0,0))

        lost_text = medium_font.render("пропущено зелених:" + str(lost), True, (255,255,255))
        win.blit(lost_text,(0,0))

        score = medium_font.render("Збито зелених:" + str(0), True, (255,255,255))
        win.blit(score,(0,25))

        player.update()
        player.reset(win)
        enemies.update()
        enemies.draw(win)
        bullets.update()
        bullets.draw(win)


    pygame.display.update()

    clock.tick(FPS)