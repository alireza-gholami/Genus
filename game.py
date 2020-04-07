import pygame
import time
import random
from pygame.locals import *

# start Py_Game
pygame.init()

# load a music
crash_sound = pygame.mixer.Sound("Crash1.wav")
pygame.mixer.music.load("Action_Sport_Rock_Trailer .mp3")

# init game display size
display_width = 800
display_height = 600

# init colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
persian_green = (0, 166, 147)

car_image = pygame.image.load('redCar.png')
car_width = 45
game_display = pygame.display.set_mode((display_width, display_height))
# make a Caption 2
pygame.display.set_caption('Race Car')
# make a frame per second
clock = pygame.time.Clock()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        # game_display.fill(white)
        game_display.blit(pygame.image.load("img.png"), (0, 0))
        large_text = pygame.font.Font('freesansbold.ttf', 90)
        text_surf, text_rect = text_objects("Let's Play Game", large_text, red)
        text_rect.center = ((display_width / 2), (display_height / 5))
        game_display.blit(text_surf, text_rect)

        button("Play", 150, 450, 100, 50, white, persian_green, "play")         # make start button
        button("Quit", 550, 450, 100, 50, red, persian_green, "quit")           # make quit button

        pygame.display.update()


def button(message, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(game_display, active_color, (x, y, width, height))
        if click[0] == 1:
            if action == "play":
                game_loop()
            elif action == "quit":
                quit_game()
    else:
        pygame.draw.rect(game_display, inactive_color, (x, y, width, height))

    small_text = pygame.font.Font("freesansbold.ttf", 20)
    text_surf, text_rect = text_objects(message, small_text, black)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    game_display.blit(text_surf, text_rect)


def quit_game():
    pygame.quit()
    quit()


# display score
def score(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(count), True, red)
    game_display.blit(text, (0, 0))


# init stuff
def stuff_rect(x, y, width, height, my_color):
    pygame.draw.rect(game_display, my_color, [x, y, width, height])


# put a car in the middle
def car(x, y):
    game_display.blit(car_image, (x, y))


def text_objects(text, font, txt_color):
    text_surface = font.render(text, True, txt_color)
    text_rect = text_surface.get_rect()
    return text_surface, text_rect


def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 80)
    text_surf, text_rect = text_objects(text, large_text, black)
    text_rect.center = ((display_width/2), (display_height/2))
    game_display.blit(text_surf, text_rect)
    pygame.display.update()

    time.sleep(2)
    game_loop()


def crash():

    # stop music
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    large_text = pygame.font.Font('freesansbold.ttf', 80)
    text_surf, text_rect = text_objects("YOU CRASHED", large_text, white)
    text_rect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(pygame.image.load("crash.jpg"), (0, 20))
    game_display.blit(text_surf, text_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        button("Try Again", 150, 450, 100, 50, white, persian_green, "play")  # make start button
        button("Quit", 550, 450, 100, 50, red, persian_green, "quit")  # make quit button
        pygame.display.update()


def game_loop():
    # music load
    pygame.mixer.music.play(-1)
    # init car location
    y = (display_height * 0.8)
    x = (display_width * 0.45)
    # get a car location change
    x_change = 0

    stuff_start_x = random.randrange(0, display_width)
    stuff_start_y = -600
    circle_start_x = random.randrange(0, display_width)
    circle_start_y = random.randrange(500, 1000) * -1
    circle_radius = 25
    stuff_speed = 7
    stuff_width = 100
    stuff_height = 100
    stuff_color = red
    dodged = 0

    game_exit = False
    # get events until quit
    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                quit_game()
            # get a key to move
            keys = pygame.key.get_pressed()
            if keys[K_a] or keys[K_LEFT] and not keys[K_d]:
                x_change -= 5
            if keys[K_d] or keys[K_RIGHT] and not keys[K_a]:
                x_change += 5
            if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                x_change = 0
            if event.type == pygame.KEYUP and (event.key == pygame.K_a or event.key == pygame.K_d):
                x_change = 0
            if keys[K_UP]:
                x_change = 0

        x += x_change

        game_display.fill(white)
        # game_display.blit(pygame.image.load("disp.jpg"), (0, 0))

        # x, y, width, height, color
        stuff_rect(stuff_start_x, stuff_start_y, stuff_width, stuff_height, stuff_color)
        if dodged <= 5:
            circle_start_x = display_width
        if dodged > 5:
            pygame.draw.circle(game_display, black, (circle_start_x, circle_start_y), circle_radius)
            if circle_start_y > display_height:
                circle_start_y = 0 - circle_radius
                circle_start_x = random.randrange(0, display_width - 100)
                dodged += 1
                if dodged % 5 == 0:
                    circle_radius += 5
        stuff_start_y += stuff_speed
        circle_start_y += stuff_speed

        car(x, y)

        # Repeat stuff
        if stuff_start_y > display_height:
            stuff_start_y = 0 - stuff_height
            stuff_start_x = random.randrange(0, display_width - 100)
            dodged += 1
            if dodged % 5 == 0:
                stuff_speed += 1
                stuff_width += 5

        # Display player score
        score(dodged)
        stuff_location = stuff_start_x + stuff_width
        if y < stuff_start_y + stuff_height:
            if stuff_start_x < x < stuff_location or stuff_start_x < x + car_width < stuff_location:
                crash()
        circle_location = circle_start_x + circle_radius
        if y < circle_start_y + 25:
            if circle_start_x < x < circle_location or circle_start_x < x + car_width < circle_location:
                crash()

        # crash if impact with wall
        if x > display_width - car_width or x < 0:
            crash()

        pygame.display.update()     # display what happens in underground
        clock.tick(60)


game_intro()
game_loop()
quit_game()
