""".A module to work on the ships."""
import pygame

class Ship():

    def __init__(self,ai_settings, screen):
        """.Initialize the ship and set its position."""
        self.screen = screen
        self.ai_settings = ai_settings

        #load the ship image and get ts rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #start each new ship at the buttom center of the sreen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom  = self.screen_rect.bottom

        #store a decimal value for the ship's center
        self.center  = float(self.rect.centerx)

        # movement flag
        self.move_right = False
        self.move_left  = False
       

    def update(self):

        #updating the movement of the ship by 1.5 instead of 1
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.move_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

      


        #update rect object
        self.rect.centerx = self.center 

        


    def blitme(self):
        """.Draw the ship at its current position."""
        self.screen.blit(self.image , self.rect)

    def center_ship(self):
        """.center the ship on the sceen"""
        self.center = self.screen_rect.centerx
