from pickle import TRUE
from re import T
import pygame

#teste
class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
    self.player = player
    self.size = data[0]
    self.image_scale = data[1]
    self.offset = data[2]
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.hit = False
    self.health = 1000
    self.alive = True
    self.defend = False
    self.defendHit = False
    self.squat = False

  def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list

  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.squat = False
    self.attack_type = 0
    

    #get keypresses
    key = pygame.key.get_pressed()

    #can only perform other actions if not currently attacking
    if self.attacking == False and self.alive == True and round_over == False:
      #check player 1 controls
      if self.player == 1:
        #movement
        if key[pygame.K_a] and not(self.squat) and not(self.defend):
          dx = -SPEED
          self.running = True
        if key[pygame.K_d] and not(self.squat) and not(self.defend):
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_w] and self.jump == False and not(self.defend):
          self.vel_y = -30
          self.jump = True
        #squat
        if key[pygame.K_s] and self.jump == False:
          self.rect = pygame.Rect(( self.rect.left, self.rect.bottom, 80, 110))
          self.squat = True
        else:
          self.rect = pygame.Rect(( self.rect.left, self.rect.top, 80, 180))
          self.squat = False
        #defend
        if key[pygame.K_x]:
          self.defend = True
        else:
          self.defend = False



        #attack
        if (key[pygame.K_r] or key[pygame.K_t]) and not(self.defend):
          self.attack(surface, target)
          #determine which attack type was used
          if key[pygame.K_r]:
            self.attack_type = 1
          if key[pygame.K_t]:
            self.attack_type = 2



      #check player 2 controls
      if self.player == 2:
        #movement
        if key[pygame.K_LEFT] and not(self.squat) and not(self.defend):
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT] and not(self.squat) and not(self.defend):
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_UP] and self.jump == False and not(self.defend):
          self.vel_y = -30
          self.jump = True
        #attack
        if key[pygame.K_o] or key[pygame.K_m]:
          self.attack(surface, target)
          #determine which attack type was used
          if key[pygame.K_o]:
            self.attack_type = 1
          if key[pygame.K_m]:
            self.attack_type = 2
        #squat
        if key[pygame.K_DOWN]:
          self.rect = pygame.Rect(( self.rect.left, self.rect.bottom, 90, 110))
          self.squat = True
        else:
          self.rect = pygame.Rect(( self.rect.left, self.rect.top, 80, 180))
          self.squat = False
        #defend
        if key[pygame.K_p]:
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

    
#handle animation updates
  def update(self):
    #check what action the player is performing
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit
    elif self.defendHit == True:
      if self.squat == True:
        self.update_action(11)
      else:
        self.update_action(9)
    elif self.attacking == True:
      if self.squat == True:
        if self.attack_type == 1:
          self.update_action(12)
        elif self.attack_type == 2:
          self.update_action(13)
      else:
        if self.attack_type == 1:
          self.update_action(3)#3:attack1
        elif self.attack_type == 2:
          self.update_action(4)#4:attack2
    elif self.jump == True:
      self.update_action(2)#2:jump
    elif self.defend == True:
      if self.squat == True:
        self.update_action(10)
      else:
        self.update_action(8)
    elif self.squat == True:
      self.update_action(7)
    elif self.running == True:
      self.update_action(1)#1:run
    else:
      self.update_action(0)#0:idle

    animation_cooldown = 50
    #update image
    self.image = self.animation_list[self.action][self.frame_index]
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 3 or self.action == 4 or self.action == 12 or self.action == 13:
          self.attacking = False
          self.attack_cooldown = 20
        #check if damage was taken
        if self.action == 5:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking = False
          self.attack_cooldown = 20
        if self.action == 11 or 9:
          self.defendHit = False


  def attack(self,surface, target):
    if self.attack_cooldown == 0:
      #execute attack
      self.attacking = True
      if self.squat == True:
        attacking_rect = pygame.Rect(self.rect.centerx - (1.5 * self.rect.width * self.flip), self.rect.y - 110, 1.5 * self.rect.width, self.rect.height / 2.85)
      else:
        attacking_rect = pygame.Rect(self.rect.centerx - (1.5 * self.rect.width * self.flip), self.rect.y, 1.5 * self.rect.width, self.rect.height / 2.85)
      if attacking_rect.colliderect(target.rect):
        if target.defend and (self.squat == target.squat):
          target.health -= 10
          target.defendHit = True
        else:
          target.health -= 100
          target.hit = True
      pygame.draw.rect(surface, (0, 255, 0), attacking_rect)



  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()



  def draw(self, surface,color):
    pygame.draw.rect(surface, color, self.rect)
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))