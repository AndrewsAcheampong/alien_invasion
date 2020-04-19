""". A module to control the functionalities of the game ."""
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event , ai_settings , screen , ship , bullets):
    # Detecting events of the keyboard. When the right key is pressed, the ship moves right    
    if event.key == pygame.K_RIGHT:
        ship.move_right = True

    if event.key == pygame.K_LEFT:
        ship.move_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings , screen , ship , bullets)
      

def fire_bullets(ai_settings , screen , ship , bullets):

      if len(bullets) < ai_settings.bullet_allowed:
            #creating an instance of the Bullet Class
            new_bullet = Bullet(ai_settings , screen , ship)
            bullets.add(new_bullet)



def check_keyup_events(event , ship):
    # When the right key is left, the ship stops moving
    if event.key == pygame.K_RIGHT:
        ship.move_right = False

    if event.key == pygame.K_LEFT:
        ship.move_left = False


#Codes for the Bullets
    """.Update position of the bullets and get rid of old bullets."""
def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()
    # Get rid of bullets  that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)



def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    
    #check for any bullets that have hit aliens
    #if so, get rid of the bullet and the aliens
    collisions = pygame.sprite.groupcollide(bullets , aliens ,True , True)

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)




def check_event(ai_settings , screen , stats , play_button , ship , aliens , bullets):
    """.Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x , mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event , ai_settings, screen , ship , bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event , ship)
        
def check_play_button(ai_settings , screen , stats , play_button ,ship , aliens , bullets , mouse_x , mouse_y):
    """.Start a new game when the player hits play."""
    if play_button.rect.collidepoint(mouse_x , mouse_y):
        stats.reset_stats()
        stats.game_active = True

        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship() 
    
        

def get_number_aliens_x(ai_settings , alien_width):
    """.Determine the number of aliens that fit in a row."""
    available_space_x  = ai_settings.screen_width - 2 * alien_width
    number_aliens_x    = int(available_space_x / (2 * alien_width) )
    return number_aliens_x

def get_number_rows(ai_settings , ship_height , alien_height):
    
    available_space_y = (ai_settings.screen_height - ( 3 * alien_height ) - ship_height )
    number_rows       =  int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings , screen , aliens , alien_number , row_number):    
    # Creating the first row of aliens
        alien         = Alien(ai_settings , screen)
        alien_width   = alien.rect.width
        alien.x       = alien_width + 2  * alien_width  * alien_number
        alien.rect.x  = alien.x
        alien.rect.y  = alien.rect.height + 2 * alien.rect.height  * row_number
        aliens.add(alien)

    
def create_fleet(ai_settings , screen , ship , aliens):
    """.Create a full fleet of aliens."""

    alien = Alien(ai_settings , screen)
    number_aliens_x = get_number_aliens_x(ai_settings , alien.rect.width)
    number_rows     = get_number_rows(ai_settings , ship.rect.height , alien.rect.height)

     #create fleet of aliens.
    for row_number in range(number_rows):
        #create the first row for 
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings , screen , aliens , alien_number , row_number)

def check_fleet_edges(ai_settings , aliens):
    """.Respond when aliens reach the edge """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings , aliens)
            break

def change_fleet_direction(ai_settings , aliens):
    """.Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)

    else :
        stats.game_active = False
   

def update_aliens(ai_settings , stats , screen , ship , aliens , bullets):
    """.Check if the fleet is at an edge and change the positions of all the aliens in the fleet."""
    check_fleet_edges(ai_settings , aliens)
    aliens.update()

    #Detecting alien ship collision
    if pygame.sprite.spritecollideany(ship , aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    #look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings , stats , screen , ship , aliens , bullets)



def check_aliens_bottom(ai_settings , stats , screen , ship , aliens , bullets):
    """check if any aliens have reach the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings , stats , screen , ship , aliens , bullets)
            break


def update_screen(ai_settings , screen , stats , ship , aliens , bullets , play_button):
    """Update images on the screen and flip to the new screen."""
    
    #redraw the screen diring each pass through the loop
    screen.fill(ai_settings.bg_color)

    #redraw all bullets behind  ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #drawing a ship on the screen
    ship.blitme()

    #drawing an alien onto the screen
    aliens.draw(screen)

    #Draw the play button if the game is
    if not stats.game_active:
        play_button.draw_button() 

    # Make the most recently drawn screen visible
    pygame.display.flip()
    

