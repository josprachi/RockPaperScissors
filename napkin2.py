import pygame
from pygame.locals import *
import random

WIDTH = 800
HEIGHT = 640
RockCount = [0]

#this is for test commit 
 
# Did code to python pep 8 style guide.
# https://www.python.org/dev/peps/pep-0008/
class Player(pygame.sprite.Sprite):
    @classmethod
    def load_images(cls):
        # convert image to pygame format will help with speed
        # convert_alpha() will not show invisable parts with pngs and jpg
        cls.images = [
            pygame.image.load('napkin1.png').convert_alpha(),
            pygame.image.load('napkin2.png').convert_alpha(),
            pygame.image.load('napkin3.png').convert_alpha(),
            pygame.image.load('napkin4.png').convert_alpha()]
 
    def __init__(self, x, y, w, h):
        super(Player,self).__init__()
        self.image=self.images[0]
        self.rect = pygame.Rect(x, y, w, h)
        self.velocity = 10#5
        self.is_jumping = False
        self.jump_count = 5
        self.walk_left = 0, 2
        self.walk_right = 0, 1
        self.walk_count = 0
        self.walk_pos = 0
        self.walk_cut = 0,3
        self.tick = 100
        self.next_tick = 100
        self.hurt = False
 
    def can_move(self, ticks):
        if ticks > self.tick:
            self.tick += self.next_tick
            return True
        return False
 
    def draw(self, surface):
        surface.blit(Player.images[self.walk_pos], self.rect)
    
    def get_hurt(self):
        self.walk_pos = self.walk_cut[1]
 
    def move_left(self):
        if self.rect.x > self.velocity:
            self.walk_count = (self.walk_count + 1) % len(self.walk_left)
            self.walk_pos = self.walk_left[self.walk_count]
            self.rect.x -= self.velocity
 
    def move_right(self, width):
        if self.rect.x < width - self.rect.width - self.velocity:
            self.walk_count = (self.walk_count + 1) % len(self.walk_right)
            self.walk_pos = self.walk_right[self.walk_count]
            self.rect.x += self.velocity
            
class Scissors(pygame.sprite.Sprite):
    def __init__(self,texture,x,y,w,h):        
        super(Scissors,self).__init__()
        self.image = texture
        self.rect = Rect(x,y,w,h)
        self.rect.x = random.randrange(100,WIDTH - self.rect.width)
        #self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 15)
        self.speedx = random.randrange(-3, 3)
        self.collected = False

    def update(self):
        self.rect.y += self.speedy
        if (self.rect.top > HEIGHT + 10)or (self.collected):
            self.rect.x = random.randrange(100,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 15)
            self.collected = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)        

class Rock(pygame.sprite.Sprite):
    def __init__(self,texture,x,y,w,h):
        super(Rock,self).__init__()
        self.image = texture
        self.rect = Rect(x,y,w,h)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.collected = False

    def update(self):
        self.rect.y += self.speedy
        if (self.rect.top > HEIGHT + 10) or (self.collected):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 15)
            self.collected = False

    def draw(self, surface):
        #print(self.rect)
        surface.blit(self.image, self.rect)        
    


class Scene:
    def __init__(self):
        pygame.init()
        # basic pygame setup
        pygame.display.set_caption('Napkin Move')
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.surface = pygame.display.set_mode(self.rect.size)
        self.clock = pygame.time.Clock()
        self.life = 100
 
        # Scene setup
        Player.load_images()
        self.background = pygame.image.load('bg1.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, self.rect.size)
        self.heartImg = pygame.image.load('heart.png').convert_alpha()
        self.heartImg = pygame.transform.scale(self.heartImg,(50,50))
        self.player = Player(300, HEIGHT-100, 64, 64)
        self.scissors = Scissors(pygame.image.load('scissors.png').convert_alpha(),10, 100, 64, 64)
        self.Rock = Rock(pygame.image.load('rock.png').convert_alpha(),400, 100, 64, 64)

        self.Scorefont = pygame.font.SysFont(None, 42)
        self.Scoretext = self.Scorefont.render("0", True,(255,0,0))
 
    def mainloop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        print("moveLeft")
                        self.player.move_left()
                    elif event.key == pygame.K_d:
                        print("moveRight")
                        self.player.move_right(self.rect.width)
 
            ticks = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
 
            if self.player.can_move(ticks):
                if keys[pygame.K_LEFT]:
                    self.player.move_left()
                elif keys[pygame.K_RIGHT]:
                    self.player.move_right(self.rect.width)
            self.scissors.update()
            self.Rock.update()
            if pygame.sprite.collide_circle(self.player, self.Rock):
                self.Rock.collected = True
                RockCount[0] += 1
                print("Collision happend")
                self.Scoretext = self.Scorefont.render(str(RockCount[0]), True,(255,0,0))
                if self.life < 100:
                    self.life += 10
                    #self.heartImg.set_alpha((255*self.life)/10000)
                    
            if pygame.sprite.collide_rect_ratio(1.5)(self.player,self.scissors):
                self.scissors.collected = True                
                print("Collision happend with scissors")                
                if self.life > 0:
                    self.life -= 10
                    print(self.life)
                    self.player.get_hurt()
                    #self.heartImg.set_alpha((255*self.life)/10000)
                      
         
 
            # drawing
            self.surface.blit(self.background, (0,0))
            self.player.draw(self.surface)
            self.scissors.draw(self.surface)
            self.Rock.draw(self.surface)
            self.surface.blit(self.Scoretext,(20,20))
            self.surface.blit(self.heartImg,(WIDTH*0.8,20))
 
            # draw code here
 
            pygame.display.flip()
            self.clock.tick(30)


 
if __name__ == '__main__':
    scene = Scene()
    scene.mainloop()
    pygame.quit()
