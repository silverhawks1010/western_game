import pygame
import sys
from scenes.menu import Menu

# Initialize Pygame
pygame.init()

# Set up the display in full screen mode
frame = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Western Game")

# Create the menu
menu = Menu(frame)

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
            elif action == "quit":
                running = False

    if in_menu:
        menu.display_menu()
    else:
        # Fill the screen with a color (optional)
        frame.fill((0, 0, 0))
        # Update the display
        pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()