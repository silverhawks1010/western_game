import pygame
import sys
from scenes.menu import Menu
from scenes.world import Map

# Initialize Pygame
pygame.init()

# Set up the display in full screen mode
frame = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Western Game")

# Create the menu
menu = Menu(frame)
map = None

# Main game loop
running = True
in_menu = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_menu:
            action = menu.handle_event(event)
            if action == "start_game":
                in_menu = False
                map = Map(frame)
            elif action == "quit":
                running = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_menu = True

    if in_menu:
        menu.display_menu()
    else:
        # Mise à jour du jeu
        map.update()

        # Mise à jour et dessin des balles
        if hasattr(map, 'player'):
            map.player.bullets.update()

        # Dessin de la map et des éléments
        map.draw()

        # Dessin des balles
        if hasattr(map, 'player'):
            map.player.bullets.draw(frame)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()