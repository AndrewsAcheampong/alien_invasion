""". Creating a bullet class."""
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self , ai_settings , screen , ship):
        """. A bullet to fire bullets."""

        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect((0, 0),(ai_settings.bullet_width, ai_settings.bullet_height))
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top


        #store the bullet position as a decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


         
    def update(self):
        """.Move bullet up the screen."""
        self.y -= self.speed_factor 

        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen , self.color , self.rect)