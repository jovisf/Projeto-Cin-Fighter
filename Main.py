import pygame
from fighter import Fighter

pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000





#load background image
bg_image = pygame.image.load("fotoHome2.jpg").convert_alpha()





#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


#create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False)
fighter_2 = Fighter(2, 700, 310, True)

#game loop
run = True
while run:

  clock.tick(FPS)

  #draw background
  draw_bg()

  #show player stats
  draw_health_bar(fighter_1.health, 20, 20)
  draw_health_bar(fighter_2.health, 580, 20)


  #draw fighters
  fighter_1.draw(screen)
  fighter_2.draw(screen)

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
    screen.blit(victory_img, (360, 150))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 200, 310, False)
      fighter_2 = Fighter(2, 700, 310, True)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False


  #update display
  pygame.display.update()

#exit pygame
pygame.quit()