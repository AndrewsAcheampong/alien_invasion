import sys

import pygame 
from settings import Settings
from ship import Ship


def run_game():

    # pygame.init()
    # screen = pygame.display.set_mode((1200 , 650))
    # bg_color = (0,0,255)


    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.width , ai_settings.height))
    pygame.display.set_caption("Andy's Game")

    #make ship
    ship = Ship(screen)

    screen.fill(ai_settings.bg_color)
    ship.blitme()

    




    #Startiing the maing gme loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

run_game()

