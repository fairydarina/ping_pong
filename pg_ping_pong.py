import pygame
import os
import time
import sys

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
score_user = 0
score_comp = 0
score_end = 3

pygame.display.set_caption('Ping Pong')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    
    return image


class Pole:
    def __init__(self, wigth, height):
        self.wigth = wigth
        self.height = height
        self.linewigth = 5
        
    def draw(self, screen):
        pygame.draw.rect(screen, (8,232,222), (0, 0, self.wigth // 2, self.height), self.linewigth)
        pygame.draw.rect(screen, (8,232,222), (self.wigth // 2, 0, self.wigth // 2, self.height), self.linewigth)
        
        font = pygame.font.Font(None, 100)
        
        text = font.render(str(score_comp), 1, (8,232,222))
        screen.blit(text, (self.wigth // 2 - 100, 60))
        
        text = font.render(str(score_user), 1, (8,232,222))
        screen.blit(text, (self.wigth // 2 + 60, 60))

    
class Ball(pygame.sprite.Sprite):
    image = load_image('ball.png')
    
    def __init__(self, group, pole_width, pole_height):
        super().__init__(group)
        self.image = Ball.image
        self.speed = 3.0
        self.rect = self.image.get_rect()
        self.pos_x = pole_width / 2
        self.pos_y = pole_height / 2
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
        self.v_x = -self.speed
        self.v_y = self.speed
        self.pole_width = pole_width
        self.pole_height = pole_height
    
    def set_Pos(self, x, y, v_x, v_y):
        self.rect.x = x
        self.rect.y = y
        self.v_x = v_x
        self.v_y = v_y
    
    def calc(self):
        global score_user, score_comp
        self.pos_x += self.v_x
        self.pos_y += self.v_y
        
        if self.pos_y < 0 or self.pos_y > self.pole_height - self.rect.height: 
            self.v_y *= -1
        if self.pos_x < 0: 
            self.v_x *= -1
            score_user += 1
        elif self.pos_x > self.pole_width - self.rect.width:
            self.v_x *= -1
            score_comp += 1

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
            
        return (self.rect.x, self.rect.y)     
    

class RocketComp(pygame.sprite.Sprite):
    image = load_image('rocket.png')
    def __init__(self, group, pole_width, pole_height):
        super().__init__(group)
        self.image = RocketUser.image
        self.rect = self.image.get_rect()
        self.pole_width = pole_width
        self.pole_height = pole_height  
        
        self.pole_width = pole_width
        self.pole_height = pole_height 
        self.width = 20
        self.height = 80        
        self.rect.x = 8
        self.rect.y = self.pole_height // 2 - self.height // 2 

        self.to_point_y_vel = 2.5
    
    
    def calc(self, point_ball):
        ball_y = point_ball[1]
        center_y = self.rect.y + self.height // 2
        #print(ball_y)
        
        if center_y < ball_y:
            self.rect.y += self.to_point_y_vel
        else:
            self.rect.y -= self.to_point_y_vel
          
 
        if self.rect.y < 3:
            self.rect.y = 3
            

        if self.rect.y > self.pole_height - self.height:
            self.rect.y = self.pole_height - self.height


class RocketUser(pygame.sprite.Sprite):
    image = load_image('rocket.png')
    
    def __init__(self, group, pole_width, pole_height):
        super().__init__(group)
        self.image = RocketUser.image
        self.rect = self.image.get_rect()
        self.pole_width = pole_width
        self.pole_height = pole_height  
        self.width = 20
        self.height = 80        
        self.rect.x = self.pole_width - 8 - self.width
        self.rect.y = self.pole_height // 2 - self.height // 2        
        
    def move_up(self):
        self.rect.y -= 5
        if self.rect.y < 10:
            self.rect.y = 5
    
    def move_down(self):
        self.rect.y += 5
        if self.rect.y > self.pole_height - self.height:
            self.rect.y = 415

       
running = True

p = Pole(width, height)
r_c = RocketComp(all_sprites, width, height)
r_u = RocketUser(all_sprites, width, height)
b = Ball(all_sprites, width, height)

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        r_u.move_up()
    if keys[pygame.K_DOWN]:
        r_u.move_down()   
    
    screen.fill((255,255,255))
    
    p.draw(screen)
    all_sprites.draw(screen)
      
    pygame.display.flip()
    
    point_ball = b.calc()
    r_c.calc(point_ball)
    
    collide_b_r_u = pygame.sprite.collide_rect(b, r_u)
    collide_r_c_b = pygame.sprite.collide_rect(r_c, b)
    
    if collide_b_r_u or collide_r_c_b:
        b.v_x *= -1
    
    clock.tick(60)
    
    if score_user >= score_end or score_comp >= score_end:
        running = False    
    


font = pygame.font.Font(None, 50)
    
if score_user >= score_end:
    text = font.render('Выиграл Пользователь', 1, (255, 0, 0))
elif score_comp >= score_end:
    text = font.render('Выиграл Компьютер', 1, (255, 0, 0))
        
text_x = width // 2 - text.get_width() // 2
text_y = height // 2 - text.get_height() // 2
text_w = text.get_width()
text_h = text.get_height()
    
pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 3)
screen.blit(text, (width // 2 - text_w // 2, 235))
pygame.display.flip()
time.sleep(10)
    
pygame.quit()
