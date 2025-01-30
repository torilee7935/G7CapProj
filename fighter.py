import pygame


class Fighter():
    def __init__(self, x, y, data, sprite_sheet, animation_steps, player_number, attack_sound):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.orgoffset=data[2]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0=idle, 1=run/walk, 2=jump, 3=fall, 4=attack1, 5=attack2, 6=hit, 7=death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        self.rect = pygame.Rect((x, y , 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.health = 100
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = attack_sound
        self.hit = False
        self.alive = True
        self.player_number = player_number
        
        
    def load_images(self, sprite_sheet, animation_steps):
        
        #extract sprites from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):        
            sprite_list = []
            for x in range(animation):
                sprite = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                sprite_list.append(pygame.transform.scale(sprite, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(sprite_list)  
        return animation_list    
    
            
    def move(self, SCREEN_W, SCREEN_H, surface, opponent):
        speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #get keystrokes
        key = pygame.key.get_pressed()

        #PLAYER 1 CONTROLS ======
        #ONLY do these IF NOT attacking
        if self.player_number == 1:
            if self.attacking == False:
            
            #Left and Right
                if key[pygame.K_a]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_d]:
                    dx = speed
                    self.running = True
            #Jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
            #Attack
                if key[pygame.K_q] or key[pygame.K_e]:
                    self.attack(surface, opponent)
                #Determine which attacks q or e
                    if key[pygame.K_q]:
                        self.attack_type = 1
                    if key[pygame.K_e]:
                        self.attack_type = 2


        #PLAYER 2 CONTROLS ======
        elif self.player_number == 2: 
            if self.attacking == False:
                #Left and Right
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.running = True
                #Jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #Attack
                if key[pygame.K_n] or key[pygame.K_m]:
                    self.attack(surface, opponent)
                    #Determine which attacks n or m
                    if key[pygame.K_n]:
                        self.attack_type = 1
                    if key[pygame.K_m]:
                        self.attack_type = 2

        #Gravity -> Jump
        #This will cause player 1 & 2 to be uneven until player 2 controls are implemented
        self.vel_y += gravity
        dy += self.vel_y

        #STAY ON SCREEN
        #Left Side
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        #Right Side
        if self.rect.right + dx > SCREEN_W:
            dx = SCREEN_W - self.rect.right
        #Bottom 
        if self.rect.bottom + dy > SCREEN_H - 140:
            self.vel_y = 0
            self.jump = False
            dy = SCREEN_H - 136 - self.rect.bottom

        #Fighters face each other
        if opponent.rect.centerx > self.rect.centerx:
            self.flip = False
            self.offset = self.orgoffset
        else:
            
            self.flip = True
            if self.orgoffset == [87, 62]:
                self.offset= [23,62]
            if self.orgoffset == [86, 51]:
                self.offset=[30,51]
            if self.orgoffset == [55, 22]:
                self.offset=[45,22]
            if self.orgoffset == [108, 98]:
                self.offset == [[114, 98]]

        #attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -=1

        #update position
        self.rect.x += dx
        self.rect.y += dy


    #function to handle animation updating
    def update(self):
        
        #check what movement being performed
        if self.health <= 0:
            self.health=0
            self.alive = False
            if self.orgoffset == [55,22]:
                self.update_action(8)
            else:
                self.update_action(7)
        elif self.hit == True:
            if self.orgoffset == [55,22]:
                self.update_action(7)
            else:
                self.update_action(6)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action (4)
            elif self.attack_type == 2:
                self.update_action(5)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else :
            self.update_action(0) 
        


        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
        #check if animation is finished, loop back around
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                #if player is dead end animation
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0
                #check if attack is true 
                if self.action == 4 or self.action == 5:
                    self.attacking = False
                    self.attack_cooldown = 20 
                elif self.action == 6 or (self.action == 7 and self.orgoffset == [55,22]):
                    self.hit = False
                    #if the player was in the middle of an attack, then attack is also stopped
                    self.attacking = False
                    self.attack_cooldown = 20
       
                
    def attack(self, surface, opponent):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            hitbox = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if hitbox.colliderect(opponent.rect):
                opponent.health -= 10
                opponent.hit = True



    def update_action(self, new_action):
        #check if the new action is different from previous
        if new_action != self.action:
            self.action = new_action
            #update animation index
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def respawn(self,x,y):
        self.rect = pygame.Rect((x, y , 80, 180))