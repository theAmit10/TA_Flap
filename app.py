import pygame,sys,random

"""
sys-> it will give the acess of system module.
"""

# for floor animination


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 700))
    screen.blit(floor_surface, (floor_x_pos + 576, 700)) # its is adding width of screen


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)    # randomly selection of pipe from the pipe_height list.
    bottom_new_pipe = pipe_surface.get_rect(midtop = (650,random_pipe_pos)) # crating the random height of the list
    top_new_pipe = pipe_surface.get_rect(midbottom = (650,random_pipe_pos - 350))
    return bottom_new_pipe,top_new_pipe


def move_pipe(pipes): # it takes an argument for a list of pipes whenever a SPWANPIPE event runs its create a list of pipes.
    for pipe in pipes: # so each rectangle of pipe inside a list
        pipe.centerx -= 5 # it moves all the to left a little amount.
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800: # here top pipe will never reach this situation. because of this condition
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) # first we have add surface, we have to decide we want to flip in x direction i.e False , and last want to flip in y direction.
            screen.blit(flip_pipe,pipe)


def check_collision(pipes): # to check death
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -300 or bird_rect.bottom >= 700: # 700 because we touch the floor their. and -200 so that we can go slightly above the sky means top.
        return False

    return  True


# but due to this a black spot comes in the bird to remove it we have to convert -> convert to convert_alpha() of bird_surface.
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3,1)# herre 1 is the scale
    return new_bird # this means -bird_movement * 3 it rotate three times in opposite direction.


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird,new_bird_rect


def score_display(game_state): # here we are giving parameter to check gameover or not.
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))    # antiallias text look sharper , (255,255,255) Red, green , blue color
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:  {(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {(int(high_score))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 280))
        screen.blit(high_score_surface, high_score_rect)

 # antiallias text look sharper , (255,255,255) Red, green , blue color
# here in line 59 score produce it return a float value so we have to convert it into int and than to string.

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# frequency= 44100  by default, size= 16, channels= 1 its valuse is by default 2, buffer= 256 is used for quality.
pygame.mixer.pre_init( buffer= 512)  # init () get initialize the pre-init() give
pygame.init()

screen = pygame.display.set_mode((576,800)) # adding screen width and length
clock = pygame.time.Clock() # this used for frame rates.
game_font = pygame.font.Font('04B_19.ttf',40)

# to create text for score
# 1st args is font style and another is size


# Game Variable

gravity = 0.25 # so the bird fall down
bird_movement = 0
game_active = True # to check we are playing game or not.
score = 0
high_score = 0



bg_surface = pygame.image.load('assests/background-night.png').convert()  # convert () is used to convert the image into the pygame file to work easily.
bg_surface = pygame.transform.scale2x(bg_surface) # this will adjust the bg image to the display screen


floor_surface = pygame.image.load('assests/base.png').convert()
floor_surface = pygame.transform.scale2x((floor_surface))
floor_x_pos = 0

bird_downflip = pygame.image.load("assests/bluebird-downflap.png").convert_alpha()
bird_downflip = pygame.transform.scale2x(bird_downflip)
bird_midflip = pygame.image.load("assests/bluebird-midflap.png").convert_alpha()
bird_midflip = pygame.transform.scale2x(bird_midflip)
bird_upflip = pygame.image.load("assests/bluebird-upflap.png").convert_alpha()
bird_upflip = pygame.transform.scale2x(bird_upflip)

bird_frames = [bird_downflip,bird_midflip,bird_upflip]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 350))

#   bird_surface = pygame.image.load('assests/bluebird-midflap.png').convert()
#   bird_surface = pygame.image.load('assests/bluebird-midflap.png').convert_alpha() # conver_alpha is used to remove the black rectangle during dotating.
#   bird_surface = pygame.transform.scale2x(bird_surface)
#   bird_rect = bird_surface.get_rect(center = (100, 350)) # it create a invisible rectangle field around the birds  , this is the position of the birds (100, 350).

BIRDFLIP  = pygame.USEREVENT + 1 # + 1 to create different kind of uservent means not as the first one.
pygame.time.set_timer(BIRDFLIP, 200)

pipe_surface = pygame.image.load("assests/pipe-red.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] # to add a number of pipe rect
# we are going to create a number of rectangle using a timer.
# creating timer -- variable must be in upper case.
SPAWNPIPE = pygame.USEREVENT # this event is run by timer , not by the user
pygame.time.set_timer(SPAWNPIPE,1200) # 1200 is in millisecond means 1.2 seconds

# for height of the pipe we are taking random number from the list
pipe_height = [300,400,500,600,200]

game_over_surface = pygame.image.load('assests/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center= (288, 400)) # placing in exactly center of the screen.


# for sound
flap_sound = pygame.mixer.Sound('sound/wing.wav')
death_sound = pygame.mixer.Sound('sound/die.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_coountdown = 100


while True:
    #    something like player or bg image etc which we have to show in screen
    for event in pygame.event.get(): # it will get all the event done by user .eg. any key pressed or user using the mouse.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # now our game get compeletly closed

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8 # so that bird move upwards opposite of gravity.
                flap_sound.play() # to play the sound whenever the player press space button.
            if event.key == pygame.K_SPACE and game_active == False: # this will only work if itd false
                game_active = True
                pipe_list.clear() # we are clearing the entire list
                bird_rect.center = (100,  350) # setting the starting position of birds.
                bird_movement = 0
                score = 0 # to reset score when we restart game

        if event.type == SPAWNPIPE:
                #   pipe_list.append(create_pipe())
                pipe_list.extend(create_pipe()) # here we are creating two list so top and bottom so we can't appent to a list instead of that we can extands the list.

        if event.type == BIRDFLIP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()


    screen.blit(bg_surface,(0,-200))   # it is used to add  that image in  black scrren. (0,0) thiis is x and y corordinate


    if game_active:
        # bird
        bird_movement += gravity # now bird movement = 0 + 0.25
        rotated_bird = rotate_bird(bird_surface) # to select the different birds
        bird_rect.centery += bird_movement # now bird move
        screen.blit(rotated_bird,bird_rect)# screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipe(pipe_list) # we take all the pipe in the pipe_list  and we are going to move them  tiny bit, and overrite this lists.
        draw_pipes(pipe_list)
# this is for score
        score += 0.01 # we we add 1 here than score run too fast so add 0.01 for normal speed but it return a float value so we have to convert it into int and than to string.
        score_display('main_game')
        score_sound_coountdown -= 1
        if score_sound_coountdown <= 0:
            score_sound.play()
            score_sound_coountdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')


#   floor
    floor_x_pos -= 1 # + -> moves forword - -> move backwords
    #   screen.blit(floor_surface,(floor_x_pos,700))
    draw_floor()
    if floor_x_pos <= -576: # for the continues animination of floor .
        floor_x_pos = 0

    pygame.display.update()     # this is used to show the above thing.
    clock.tick(120)     #it means 120 frames per seconds.