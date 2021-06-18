import pygame
import sys
import random

def draw_floor():
    screen.blit(floor_surface , (floor_x_pos , 400))
    screen.blit(floor_surface , (floor_x_pos + 289 , 400))

def create_pipe():
    random_pipe_height=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop = (700 , random_pipe_height))
    top_pipe=pipe_surface.get_rect(midbottom = (700 , random_pipe_height - 200))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2

    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=511:
            screen.blit(pipe_surface , pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface , False , True)
            screen.blit(flip_pipe , pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        return False

    return True

def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird

def score_display(game_state):
    if game_state=='main_game':
        score_surface=game_font.render(str(int(score)),True,(255,255,255))
        score_rect=score_surface.get_rect(center = (145,60))
        screen.blit(score_surface,score_rect)
    if game_state=='game_over':
        score_surface=game_font.render(f'Your Score: {int(score)}',True,(255,255,255))
        score_rect=score_surface.get_rect(center = (145,230))
        screen.blit(score_surface,score_rect)

        high_score_surface=game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect=high_score_surface.get_rect(center = (145,385))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score>high_score:
        high_score=score
    return high_score


pygame.init()
screen=pygame.display.set_mode((289,511))
clock=pygame.time.Clock()
game_font=pygame.font.Font('04B_19__.TTF' , 25)

game_active=True
gravity=0.25
score=0
high_score=0

bird_movement=0
bg_surface=pygame.image.load('gallery/sprites/background.png').convert()

floor_surface=pygame.image.load('gallery/sprites/base.png').convert()
floor_x_pos=0

bird_surface=pygame.image.load('gallery/sprites/bird.png')
bird_rect=bird_surface.get_rect(center = (70 , 255))

pipe_surface=pygame.image.load('gallery/sprites/pipe.png')
pipe_list=[]


SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height=[250,300,350]

game_over_surface=pygame.image.load('gallery/sprites/message.png').convert_alpha()
game_over_rect=game_over_surface.get_rect(center = (145,255))

flap_sound=pygame.mixer.Sound('gallery/audio/wing.wav')
death_sound=pygame.mixer.Sound('gallery/audio/hit.wav')

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_active:
                bird_movement=0
                bird_movement -= 9
                flap_sound.play()
            
            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(70 , 255)
                bird_movement=0
                score=0


        if event.type==SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface , (0 , 0))

    if game_active:
        bird_movement += gravity
        rotated_bird=rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird , bird_rect) 
        game_active=check_collision(pipe_list)

        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score=update_score(score,high_score)
        score_display('game_over')

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -289:
        floor_x_pos=0

    pygame.display.update()
    clock.tick(120)

