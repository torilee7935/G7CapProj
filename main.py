import pygame
from fighter import Fighter
from button import Button, Label

#initialized sound and fonts
pygame.mixer.init()
pygame.font.init()

#Game Window Size===
SCREEN_W = 1280; SCREEN_H = 720; FPS=60; counter = 0

#define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#Define fighter variables
SAMURAI_SIZE = 137
SAMURAI_SCALE = 3
SAMURAI_OFFSET = [87, 62]
SAMURAI_DATA = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET]
WIZARD_SIZE = 160
WIZARD_SCALE = 2
WIZARD_OFFSET = [86, 51]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
HERO_SIZE = 126
HERO_SCALE = 3
HERO_OFFSET = [55, 22]
HERO_DATA = [HERO_SIZE, HERO_SCALE, HERO_OFFSET]
EVILWIZARD_SIZE = 250
EVILWIZARD_SCALE = 2.6
EVILWIZARD_OFFSET = [108, 98]
EVILWIZARD_DATA = [EVILWIZARD_SIZE, EVILWIZARD_SCALE, EVILWIZARD_OFFSET]

#Number of animation steps for each fighter
SAMURAI_STEPS = [8, 8, 2, 2, 5, 6, 4, 6]
WIZARD_STEPS = [6, 8, 2, 2, 8, 8, 4, 7]
HERO_STEPS = [10, 8, 3, 3, 7, 6, 9, 3, 11]
EVILWIZARD_STEPS = [8, 8, 2, 2, 8, 8, 3, 7]



#Game Window
window = pygame.display.set_mode((SCREEN_W, SCREEN_H))

 #Game Window Title
pygame.display.set_caption("Pixel Pummel")

intro_Image = pygame.image.load("assets/backgrounds/opening.png").convert_alpha() #starts background as intro image

def draw_InitImage(window, Image, SCREEN_W, SCREEN_H):
    scaled_initImage = pygame.transform.scale(Image, (SCREEN_W, SCREEN_H))
    window.blit(scaled_initImage, (0, 0))

    # Fade effect function
def fade_out(window, SCREEN_W, SCREEN_H, fade_speed=5):
    fade_surface = pygame.Surface((SCREEN_W, SCREEN_H))
    fade_surface.fill((0, 0, 0))

    for alpha in range(0, 255, fade_speed):
        fade_surface.set_alpha(alpha)
        window.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)  # Adjust delay for speed

#Sounds
lobby_fx = pygame.mixer.Sound("assets/sounds/lobby.mp3")
lobby_fx.set_volume(0.3)
lobby_fx.play(loops=10)
spaceSound=pygame.mixer.Sound("assets/sounds/space.mp3")
spaceSound.set_volume(0.5)
gameMusic=pygame.mixer.Sound("assets/sounds/GameMusic.mp3")
gameMusic.set_volume(.2)
victory_fx = pygame.mixer.Sound("assets/sounds/victory.wav")
victory_fx.set_volume(0.5)

sword_fx = pygame.mixer.Sound("assets/sounds/sword.wav")
punch_fx = pygame.mixer.Sound("assets/sounds/punch.wav")
woosh_fx = pygame.mixer.Sound("assets/sounds/wizard_woosh.wav")
sword_fx.set_volume(0.5)
punch_fx.set_volume(0.5)
woosh_fx.set_volume(0.5)


def lowerVolume(sound, duration):
    start_time = pygame.time.get_ticks()
    initial_volume = sound.get_volume()

    while pygame.time.get_ticks() - start_time < duration:
        elapsed_time = pygame.time.get_ticks() - start_time
        progress = elapsed_time / duration
        current_volume = initial_volume * (1 - progress)

        sound.set_volume(current_volume)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.time.delay(0)  # Adjust delay for smoothness

enter = True
while enter:

    if not pygame.mixer.get_busy():
        lobby_fx.play()

    draw_InitImage(window, intro_Image, SCREEN_W, SCREEN_H)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        spaceSound.play()
        fade_out(window, SCREEN_W, SCREEN_H)  # Add fading effect
        enter = False
        

    pygame.display.update()

# Player selection screen after opening screen
player_selection_screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# Font setup
font = pygame.font.Font("fonts/AeroviasBrasilNF.ttf", 48)

# Create label instances
player1_label = Label("Fighter 1", font, (255, 255, 255), 250, 50)
player2_label = Label("Fighter 2", font, (255, 255, 255), 900, 50)

# Load fighter spritesheets
samurai_sheet = pygame.image.load("assets/fighters/samurai/samurai.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/fighters/wizard/wizard.png").convert_alpha()
hero_sheet = pygame.image.load("assets/fighters/hero/hero.png").convert_alpha()
evilWizard_sheet = pygame.image.load("assets/fighters/evilWizard/evilWizard.png").convert_alpha()

# Load button images for characters
evilWizardButtonImage = pygame.image.load('assets/buttons/evilWizardButton.png').convert_alpha()
heroButtonImage = pygame.image.load('assets/buttons/heroButton.png').convert_alpha()
samuraiButtonImage = pygame.image.load('assets/buttons/samuraiButton.png').convert_alpha()
wizardButtonImage = pygame.image.load('assets/buttons/wizardButton.png').convert_alpha()

# Start button
startButtonImage = pygame.image.load('assets/buttons/start_button.png').convert_alpha()
start_button = Button(520, 350, startButtonImage, scale=1.0)

# player 1 image button array
player1_buttons = [
    Button(105, 110, evilWizardButtonImage, 2.5),
    Button(85, 375, heroButtonImage, 3.5),
    Button(300, 375, samuraiButtonImage, 3),
    Button(310, 130, wizardButtonImage, 2.5)
]
# player 2 image button array
player2_buttons = [
    Button(950, 110, evilWizardButtonImage, 2.5),
    Button(850, 375, heroButtonImage, 3.5),
    Button(700, 375, samuraiButtonImage, 3),
    Button(700, 130, wizardButtonImage, 2.5)
]

# Button selected for each player
player1_selected = None
player2_selected = None

# Character selection loop
run = True
sel1 = False; sel2 = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check Player 1's buttons
            for button in player1_buttons:
                if button.is_over(pygame.mouse.get_pos()):
                    player1_selected = button  # Assign the selected button to player1_selected
                    player1_label.highlight()
                    sel1 = True
                    print("Player 1 selected a character")  #debugging 

            # Check Player 2's buttons
            for button in player2_buttons:
                if button.is_over(pygame.mouse.get_pos()):
                    player2_selected = button  # Assign the selected button to player2_selected
                    player2_label.highlight()
                    sel2 = True
                    print("Player 2 selected a character") #debugging

            if start_button.is_over(pygame.mouse.get_pos()) and (sel1 == True and sel2 == True):
                print("Start button clicked")
                run = False

    player_selection_screen.fill((BLACK)) 

    # Draw labels
    player1_label.draw(player_selection_screen)
    player2_label.draw(player_selection_screen)

    # Draw buttons for both players and start button
    for button in player1_buttons:
        button.draw(player_selection_screen)

    for button in player2_buttons:
        button.draw(player_selection_screen)

    start_button.draw(player_selection_screen)

    pygame.display.update()

# setting fighters from correct butoon choice
for index, button in enumerate(player1_buttons):
    if button == player1_selected:
        if index == 0:
            fighter1 = Fighter(200, 400, EVILWIZARD_DATA, evilWizard_sheet, EVILWIZARD_STEPS, 1, woosh_fx) 
            f1=0
        elif index == 1:
            fighter1 = Fighter(200, 400, HERO_DATA, hero_sheet, HERO_STEPS, 1, punch_fx)
            f1=1
        elif index == 2:
            fighter1 = Fighter(200, 400, SAMURAI_DATA, samurai_sheet, SAMURAI_STEPS, 1, sword_fx)
            f1=2
        elif index == 3:
            fighter1 = Fighter(200, 400, WIZARD_DATA, wizard_sheet, WIZARD_STEPS, 1, woosh_fx)
            f1=3

for index, button in enumerate(player2_buttons):
    if button == player2_selected:
        if index == 0:
            fighter2 = Fighter(800, 400, EVILWIZARD_DATA, evilWizard_sheet, EVILWIZARD_STEPS, 2, woosh_fx) 
            f2=0
        elif index == 1:
            fighter2 = Fighter(800, 400, HERO_DATA, hero_sheet, HERO_STEPS, 2, punch_fx)
            f2=1
        elif index == 2:
            fighter2 = Fighter(800, 400, SAMURAI_DATA, samurai_sheet, SAMURAI_STEPS, 2, sword_fx)
            f2=2
        elif index == 3:
            fighter2 = Fighter(800, 400, WIZARD_DATA, wizard_sheet, WIZARD_STEPS, 2, woosh_fx)
            f2=3


lowerVolume(lobby_fx, 3000)

lobby_fx.stop()

#Load Background Image on Startup
init_Image = pygame.image.load("assets/backgrounds/arena.png").convert_alpha()
#***snow.png can be changed to our starting menu whenever we find it/create it

gameoverImage = pygame.image.load("assets/backgrounds/gameover.png").convert_alpha()

#Load fighter spritesheets
samurai_sheet = pygame.image.load("assets/fighters/samurai/samurai.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/fighters/wizard/wizard.png").convert_alpha()

#Load Button Images
start_img = pygame.image.load("assets/buttons/start_button.png").convert_alpha()
quit_img = pygame.image.load("assets/buttons/quit_button.png").convert_alpha()

#Create Button Instances
start_button = Button(100, 200, start_img, 1)
quit_button = Button(125, 300, quit_img, 1)

#Number of animation steps for each fighter
SAMURAI_STEPS = [8, 8, 2, 2, 5, 6, 4, 6]
WIZARD_STEPS = [6, 8, 2, 2, 8, 8, 4, 7]


def draw_InitImage(window, init_Image, SCREEN_W, SCREEN_H):
    scaled_initImage = pygame.transform.scale(init_Image, (SCREEN_W, SCREEN_H))
    window.blit(scaled_initImage, (0, 0))

def draw_centerInitImage(window, init_Image):
    scaled_initImage = pygame.transform.scale(init_Image, (450, 250))
    x = (SCREEN_W - scaled_initImage.get_width()) // 2 # Calculate the position to center the image
    y = (SCREEN_H - scaled_initImage.get_height()) // 2
    window.blit(scaled_initImage, (x, y)) # Blit the image to the calculated position

#health bar function
def draw_health_bar(health, x, y):
    ratio= health / 100 #changes size of health bar
    pygame.draw.rect(window, BLACK, (x-2, y-2, 404, 34)) #border
    pygame.draw.rect(window, RED, (x,y, 400, 30)) #red underneath
    pygame.draw.rect(window, GREEN, (x,y, 400 * ratio, 30))

clock=pygame.time.Clock()

draw_InitImage(window, init_Image, SCREEN_W, SCREEN_H)
pygame.display.update()
fighter1.update()
fighter2.update()


def gameover():
    draw_centerInitImage(window, gameoverImage)
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  
                    return True
                elif event.key == pygame.K_q:  
                    return False
            elif event.type == pygame.QUIT:
                pygame.quit()  
                exit() 

# Function to display an image with a timer
def displayCountdown(window, count, background, SCREEN_W, SCREEN_H, timer_duration=1000):
    image = pygame.image.load(count).convert_alpha()
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < timer_duration:
        window.blit(image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    window.fill((0, 0,0))  # Blit the background to clear only the image


#coundown before game
sound = pygame.mixer.Sound("assets/sounds/countdown.mp3")
sound.play()
sound.set_volume(.5)
displayCountdown(window, "assets/countdown/3.png", init_Image, SCREEN_W, SCREEN_H)
draw_InitImage(window, init_Image, SCREEN_W, SCREEN_H)
displayCountdown(window, "assets/countdown/2.png", init_Image, SCREEN_W, SCREEN_H)
draw_InitImage(window, init_Image, SCREEN_W, SCREEN_H)
displayCountdown(window, "assets/countdown/1.png", init_Image, SCREEN_W, SCREEN_H)


gameMusic.play()


#GAME LOOP===
running = True
while running:

    if not pygame.mixer.get_busy():
        gameMusic.play()

    #Draw Background
    draw_InitImage(window, init_Image, SCREEN_W, SCREEN_H)

    #draw health bar
    draw_health_bar(fighter1.health, 20, 20)
    draw_health_bar(fighter2.health, SCREEN_W-420, 20)


    #Move Fighter
    if fighter1.alive and fighter2.alive:
        fighter1.move(SCREEN_W, SCREEN_H, window, fighter2)
        fighter2.move(SCREEN_W, SCREEN_H, window, fighter1)

    #update fighter animation
    fighter1.update()
    fighter2.update()

    #Draw Fighter
    fighter1.draw(window)
    fighter2.draw(window)

    
    for event in pygame.event.get(): #event handler for exit
        if event.type == pygame.QUIT: #if clicked window x top right game loop ends
            running = False


    if not fighter1.alive or not fighter2.alive:
        counter+=1
        if counter >= 300:
            victory_fx.play()
            restart = gameover()
            if restart:
                fighter1.health = 100
                fighter2.health = 100
                fighter1.alive =True
                fighter2.alive = True
                fighter1.respawn(200, 400)
                fighter2.respawn(800,400)
                counter = 0  
                continue 
            else:
                running = False

    pygame.display.update() #updates window after moving the fighters and drawing them

    clock.tick(FPS)

#Exit Pygame
pygame.quit()
