import pygame
import os
from sprites import *
#from functions import *
pygame.font.init() #fonts
pygame.mixer.init() #sound effects



from pygame.constants import K_LCTRL

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anime game!")

WHITE =(255,255,255) 
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)
COLORKEY_SS_NARUTO=(73,176,255)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

FPS = 60 #frames per seconds
VEL = 5 #object movement velocity
BULLET_VEL = 7 #bullets movement velocity
MAX_BULLETS = 3 # number of bullets

#IMAGES
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'valley.jpg')), (WIDTH, HEIGHT))

#SpriteSheets
ss = spritesheet(os.path.join('Assets','naruto_sheet.bmp'))
#naruto_images=[]
naruto_images = ss.images_at( (pygame.Rect(4,11,29,44), pygame.Rect(200,493,42,33),pygame.Rect(38,446,56,32)), colorkey=(73,176,255))

#SOUNDS
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'impact.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'impact.wav'))


YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2


def implement_physics(red, yellow):
    if red.y + VEL + red.height < HEIGHT-15:
        red.y += VEL//2
    if yellow.y + VEL + yellow.height < HEIGHT-15:
        yellow.y += VEL//2

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, a, b):
    #fill go first, then blit
    #WIN.fill(WHITE)
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH-red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))



    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    #WIN.blit(RED_SPACESHIP, (red.x, red.y))
    image=naruto_images[b]
    WIN.blit(image, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)


    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT-15: #UP 
        yellow.y += 2*VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #DOWN
        yellow.y -= VEL
    return 0

def red_handle_movement(keys_pressed, red, m):
    
    var = m[1]

    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
        red.x -= VEL
        if var < 2:
            m.remove(var)
            var+=1
        else:
            m.remove(var)
            var=1
        m.append(var)
    elif keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
        red.x += VEL
    elif keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT-15: #DOWN
        red.y += VEL
    elif keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        red.y -= 2*VEL
    else:
        m.remove(var)
        var=0
        m.append(var)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2-draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT)) # get added to main loop in pygame.event.get()
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():

    red = pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    n = [99, 0]
    m = [99, 0]
    num_events=0


    #main loop
    clock = pygame.time.Clock()
    run =True
    while run:
        clock.tick(FPS) #run while loop at FPS speed

        for event in pygame.event.get():  #check in-game events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            winner_text=""

            if event.type == RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()

        if red_health<=0:
            winner_text = "Yellow Wins!"
        if yellow_health<=0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        

        #print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed() #which keys are pressed
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red, m)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, n[1], m[1])
        implement_physics(red, yellow)

    
    main()
    #pygame.quit()


if __name__ == "__main__":
    main()