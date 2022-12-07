# PyGame template.

# Import standard modules.
import sys
from random import random

# Import non-standard modules.
import pygame
from pygame.locals import *

# Define width = 640 and height = 480 of game window
width = 500
height = 500

# load images stone.webp, scissors.web, paper.webp from images folder
images = {"R": pygame.image.load("images/stone.webp"), "P": pygame.image.load("images/paper.webp"),
          "S": pygame.image.load("images/scissors.webp")}


# create classes for rock paper scissors inherit from entity class
class Entity:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter

        # draw images on screen at x,y coordinates of entity class object and resize image to 25,25 pixels size
    def draw(self, screen):
        screen.blit(pygame.transform.scale(images[self.letter], (35, 35)), (self.x, self.y))

    # random movement of entity on screen for 1 pixel
    def move(self):
        self.x += random() * 2 - 1
        self.y += random() * 2 - 1

    # move by 1 pixel towards closest entity on screen specified by letter
    def move_towards(self, letter, entities):
        # find closest entity
        closest = None
        closest_dist = 1000000
        for entity in entities:
            if entity.letter == letter:
                dist = ((entity.x - self.x) ** 2 + (entity.y - self.y) ** 2) ** 0.5
                if dist < closest_dist:
                    closest = entity
                    closest_dist = dist
        # move towards closest entity
        if closest is not None:
            self.x += (closest.x - self.x) / closest_dist
            self.y += (closest.y - self.y) / closest_dist

    # when entity collides with another entity that is specified by class Name
    # like rock is in proximity of paper then rock becaomes paper
    def collide(self, letter, entities):
        for entity in entities:
            if entity.letter == letter:
                if (entity.x - self.x) ** 2 + (entity.y - self.y) ** 2 < 100:
                    self.letter = letter


# create entities equally populated with letters R, P, S
# with random x and y values between 0 and 640 and 0 and 480
def create_entities(number):
    entities = []
    for i in range(number):
        letter = "RPS"[int(random() * 3)]
        x = random() * width
        y = random() * height
        entities.append(Entity(x, y, letter))
    return entities


entities = create_entities(30)


def update(dt):
    # entities chase entities with letter they are strong against if they exist
    for entity in entities:
        entity.move()
        entity.move_towards("RPS"["RPS".index(entity.letter) - 1], entities)

    # entities collide with each other
    for entity in entities:
        if entity.letter == "R":
            entity.collide("P", entities)
        elif entity.letter == "P":
            entity.collide("S", entities)
        elif entity.letter == "S":
            entity.collide("R", entities)




    for event in pygame.event.get():
        # We need to handle these events. Initially the only one you'll want to care
        # about is the QUIT event, because if you don't handle it, your game will crash
        # whenever someone tries to exit.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def draw(screen):

    screen.fill((252, 255, 233))  # Fill the screen with black.

    # draw all entities
    for entity in entities:
        entity.draw(screen)
    # display on screen big victory text when all entities are same
    # and specify which letter won replace RPS with words rock paper scissors
    if len(set([entity.letter for entity in entities])) == 1:
        font = pygame.font.SysFont('Comic Sans MS', 30)
        #change letters to words here if r then rock if p then paper if s then scissors
        if entities[0].letter == "R":
            text = font.render('Rock Wins', False, (0, 0, 0))
        elif entities[0].letter == "P":
            text = font.render('Paper Wins', False, (0, 0, 0))
        elif entities[0].letter == "S":
            text = font.render('Scissors Wins', False, (0, 0, 0))

        screen.blit(text, (width / 2 - 100, height / 2 - 100))

    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()


def run_pygame():
    # Initialise PyGame.
    pygame.init()

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 30.0
    fpsClock = pygame.time.Clock()

    # Set up the window.
    # change pygame window name here
    pygame.display.set_caption('RockPaperScissors')
    screen = pygame.display.set_mode((width, height))

    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    while True:  # Loop forever!
        update(dt)  # You can update/draw here, I've just moved the code for neatness.
        draw(screen)

        dt = fpsClock.tick(fps)


if __name__ == "__main__":
    run_pygame()
