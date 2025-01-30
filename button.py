import pygame
class Button():
    def __init__(self, x, y, image, scale=1.0):
        self.x = x
        self.y = y
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        #get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        #check mouse pos and clicks
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        #draw button
        surface.blit(self.image, (self.rect.x, self.rect. y))
        
        return action
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

# Label class
class Label:
    def __init__(self, text, font, color, x, y):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.highlighted = False

    def draw(self, surface):
        label_color = (0, 255, 0) if self.highlighted else self.color
        rendered_text = self.font.render(self.text, True, label_color)
        surface.blit(rendered_text, (self.x, self.y))

    def highlight(self):
        self.highlighted = True

    def unhighlight(self):
        self.highlighted = False
        
        
