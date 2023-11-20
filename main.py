import pygame
import os
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_frame_1 = pygame.image.load(os.path.join('player','temp1.png')).convert_alpha()
        player_frame_2 = pygame.image.load(os.path.join('player','temp2.png')).convert_alpha()

        self.player_frame_list = [player_frame_1,player_frame_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(os.path.join('player','jump.png')).convert_alpha()

        self.image = self.player_frame_list[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,400))
        self.gravity = 0

        #self.jumpsounds

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:

            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            #restart score and reload main game
        if self.rect.top <= 0:
            self.rect.top = 0

    def animation_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.image = self.player_jump
        else:
            self.player_index += 0.05
            if self.player_index >= len(self.player_frame_list):
                self.player_index = 0
            self.image = self.player_frame_list[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('pipes','pipe.png')).convert_alpha()
        self.rect = self.image.get_rect(midtop=((x,y)))
        self.speed = 5

    def pipe_mov(self):
        self.rect.x -= self.speed
    def update(self):
        self.pipe_mov()
    def delete(self):
        if self.rect < -100:
            self.kill()

def display_score():
    pass

def collision_sprite():
    pass



FPS = 60
WIDTH = 500
HEIGHT = 600

TRAN = (0,0,0,0)
TEXT_COLOR = ((111,196,169))

#windows and title
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird Concept!")
#pygame.display.set_icon()

#groups
player = pygame.sprite.GroupSingle()
player.add(Player())

pipes = pygame.sprite.Group()




#background & screens
bg_surf = pygame.image.load(os.path.join('backgrounds','extended2.png')).convert_alpha()
bg_x_pos1 = 0
bg_x_pos2 = bg_surf.get_width()
player_test = pygame.image.load(os.path.join('player','temppt.png')).convert_alpha()
player_test_scaled = pygame.transform.rotozoom(player_test,0,2)
player_test_rect = player_test_scaled.get_rect(center=(WIDTH//2,HEIGHT//2))
pygame.init()
#font
game_font = pygame.font.Font(os.path.join('font','Pixeltype.ttf'),50)
start_time = 0
score = 0
#states
game_active= 'B'
    # 'A' == intro screen
    # 'B' == main game
    # 'C' == game over 

clock = pygame.time.Clock()
run = True

for i in range(99):
    x = WIDTH + i*200
    y = random.randint(200,HEIGHT-200)
    pipes.add(Pipe(x,y))

while run:
    clock.tick(FPS)
    #WIN.fill('white')
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if game_active == 'A': #DURING INTRO
            if event.type == pygame.KEYDOWN and event.type == pygame.K_SPACE:
                game_active = 'B'
                #start_time = pygame.time.get_ticks()

        elif game_active == 'B': #MAIN GAME
            pass

        elif game_active == 'C': #GAME OVER
            if event.type == pygame.KEYDOWN and event.type == pygame.K_SPACE:
                game_active = 'B'
                #maybe restart start_time to zero?
                start_time = pygame.time.get_ticks() 


    if game_active == 'A': #INTRO
        WIN.fill(TRAN)
        #BLIT DEAD CHACTER
        # 
        game_title_surf = game_font.render("Slippy Bird!",False,TEXT_COLOR)
        game_title_rect = game_title_surf.get_rect(center = (250,50))

        WIN.blit(game_title_surf,game_title_rect)

    if game_active == 'B': #MAIN GAME
        WIN.blit(bg_surf,(bg_x_pos1,0))
        WIN.blit(bg_surf,(bg_x_pos2,0))        
        bg_x_pos1 -= 2
        bg_x_pos2 -= 2
        #if bg_x_pos < -500:
            #bg_x_pos = 0
        if bg_x_pos1 <= -(bg_surf.get_width()):
            bg_x_pos1 = bg_surf.get_width()
        if bg_x_pos2 <= -(bg_surf.get_width()):
            bg_x_pos2 = bg_surf.get_width()
        #WIN.blit(bg_surf,(bg_x_pos,0))
        # score = display function
        player.draw(WIN)
        player.update()
        # 
        pipes.update()
        for pipe in pipes:
            WIN.blit(pipe.image, pipe.rect)
        # 
        # check for collision with sprites
        pass 
    if game_active == 'C': #GAME OVER
        WIN.fill('red')
        WIN.blit(player_test_scaled,player_test_rect)

    pygame.display.update()
