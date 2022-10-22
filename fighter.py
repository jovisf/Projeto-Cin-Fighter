import pygame
#teste
class Fighter():
  def __init__(self, player, x, y, flip):
    self.player = player
    self.flip = flip
    self.frame_index = 0
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.action = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.hit = False
    self.health = 1000
    self.alive = True
    self.action = 0
    self.mana = 100
    self.defend = False



  def move(self, screen_width, screen_height, surface, target):
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    #get keypresses
    key = pygame.key.get_pressed()

    #can only perform other actions if not currently attacking
    if self.attacking == False:
      #check player 1 controls
      if self.player == 1:
        #movement
        if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_d]:
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_w] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #squat
        if key[pygame.K_s]:
          self.rect = pygame.Rect(( self.rect.left, self.rect.bottom, 90, 110))
        else:
          self.rect = pygame.Rect(( self.rect.left, self.rect.top, 80, 180))
        #defend
        if key[pygame.K_x]:
          self.defend = True
        else:
          self.defend = False


        #attack
        if key[pygame.K_r] or key[pygame.K_t]:
          self.attack(surface, target)
          #determine which attack type was used
          if key[pygame.K_r]:
            self.attack_type = 1
          if key[pygame.K_t]:
            self.attack_type = 2


      #check player 2 controls
      if self.player == 2:
        #movement
        if key[pygame.K_LEFT]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT]:
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_UP] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #attack
        if key[pygame.K_KP1] or key[pygame.K_KP2]:
          self.attack(surface, target)
          #determine which attack type was used
          if key[pygame.K_KP1]:
            self.attack_type = 1
          if key[pygame.K_KP2]:
            self.attack_type = 2
        #squat
        if key[pygame.K_DOWN]:
          self.rect = pygame.Rect(( self.rect.left, self.rect.bottom, 90, 110))
        else:
          self.rect = pygame.Rect(( self.rect.left, self.rect.top, 80, 180))
        #defend
        if key[pygame.K_KP3]:
          self.defend = True
        else:
          self.defend = False


    #apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure players face each other
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy

    



  def attack(self,surface, target):
    self.attacking = True
    attacking_rect = pygame.Rect(self.rect.centerx - (1.5 * self.rect.width * self.flip), self.rect.y, 1.5 * self.rect.width, self.rect.height / 2.85)
    if attacking_rect.colliderect(target.rect):
      if target.defend:
        target.health -= 1
      else:
        target.health -= 100
    pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
    self.attacking = False



  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()



  def draw(self, surface,color):
    pygame.draw.rect(surface, color, self.rect)