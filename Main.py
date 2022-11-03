import pygame
from pygame.locals import *
from pygame import mixer

import sys
from button import Button
from fighter import Fighter

pygame.init()

#create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cin Fighter")
BG = pygame.image.load("assets/Background.png")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000


#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

#load background image
bg_image = pygame.image.load("assets/backgroungd/back.jpg").convert_alpha()

#load spritesheets
warrior_sheet = pygame.image.load("sprites-4.png").convert_alpha()
chun_sheet = pygame.image.load("chunSprites.png").convert_alpha()

#load vicory image
victory_img = pygame.image.load("victory.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [6, 6, 10, 4, 7, 4, 7, 1, 1, 1, 1, 1, 4, 7]
CHUN_ANIMATION_STEPS = [4, 12, 13, 5, 5, 4, 4, 1, 1, 3, 1, 1, 4, 7]

#define font
count_font = pygame.font.Font("turok.ttf", 80)
score_font = pygame.font.Font("turok.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  SCREEN.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  SCREEN.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 1000
  pygame.draw.rect(SCREEN, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(SCREEN, RED, (x, y, 400, 30))
  pygame.draw.rect(SCREEN, GREEN, (x, y, 400 * ratio, 30))

# music 
mixer.init()
mixer.music.load('Street-Fighter-II-Arcade-Ryu-Stage.ogg')
mixer.music.play()

def options():
    def toggleMusic():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Options", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(200, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(200, 300), 
                            text_input="Back", font=get_font(45), base_color="Black", hovering_color="Green")
        OPTIONS_MUTE = Button(image=None, pos=(200, 200), 
                            text_input="Mute", font=get_font(45), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        
        OPTIONS_MUTE.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MUTE.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_MUTE.checkForInput(OPTIONS_MOUSE_POS):
                    toggleMusic()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


#game loop
def play():

    #create two instances of fighters
    fighter_1 = Fighter(1, 250, 430, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
    fighter_2 = Fighter(2, 900, 430, True, WARRIOR_DATA, chun_sheet, CHUN_ANIMATION_STEPS)

    #define game variables
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]#player scores. [P1, P2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    while True:

        clock.tick(FPS)

        #draw background
        draw_bg()

        #show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("GIORDANO: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("CALEGARIO: " + str(score[1]), score_font, RED, 580, 60)

        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, fighter_1, round_over)
        else:
            #display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            #update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update fighters
        fighter_1.update()
        fighter_2.update()

        #draw fighters
        fighter_1.draw(SCREEN)
        fighter_2.draw(SCREEN)

        # back button  
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BACK = Button(image='assets/exit_btn.png', pos=(1150, 80), 
                            text_input="", font=get_font(24), base_color="Black", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()


        #check for player defeat
        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            #display victory image
            SCREEN.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 250, 430, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
                fighter_2 = Fighter(2, 900, 430, True, WARRIOR_DATA, chun_sheet, CHUN_ANIMATION_STEPS)

        #update display
        pygame.display.update()

main_menu()

#exit pygame
pygame.quit()