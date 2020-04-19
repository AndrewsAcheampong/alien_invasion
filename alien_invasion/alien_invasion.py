
import pygame
from pygame.sprite import Group
from alien import Alien
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button


""". Creating the alien invasion game win#dow."""

def run_game():
    #initialize game and create screen object
    
    pygame.init()
    
    #creating an instance of Settings class    
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width , ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #make the play button
    play_button = Button(ai_settings , screen , "Play")

    #make an instance of the stats
    stats = GameStats(ai_settings)

    #make a ship
    ship = Ship(ai_settings, screen)

    #making an instance of the alien 
    alien = Alien(ai_settings , screen)

    #Making a group to store bullets in
    bullets = Group()

    #making a group of aliens
    aliens = Group()

    #create a fleet of aliens
    gf.create_fleet(ai_settings , screen , ship , aliens)

    #set actual game loop
    while True:

        gf.check_event(ai_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:

            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings , stats , screen , ship , aliens , bullets)
        gf.update_screen(ai_settings , screen , stats , ship , aliens , bullets , play_button)
       
        




run_game()

