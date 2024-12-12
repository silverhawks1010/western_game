import pygame
import sys
from scenes.menu import Menu
from scenes.world import Map
from scenes.character_selection import CharacterSelection

# Initialize Pygame
pygame.init()

# Set up the display in full screen mode
frame = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Western Game")

# Create the menu
menu = Menu(frame)
character_selection = CharacterSelection(frame)
map = None
selected_character = None

# Main game loop
running = True
in_menu = True
in_character_selection = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_menu:
            action = menu.handle_event(event)
            if action == "start_game":
                in_menu = False
                in_character_selection = True
            elif action == "quit":
                running = False

        elif in_character_selection:
            character_action = character_selection.handle_event(event)
            if character_action and character_action[0] == "character_selected":
                selected_character = character_action[1]

                # Validate selected character
                if selected_character not in [0, 1, 2]:
                    print("Invalid character selected. Defaulting to character 0.")
                    selected_character = 0

                in_character_selection = False
                map = Map(frame, selected_character)

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_menu = True

    if in_menu:
        menu.display_menu()
    elif in_character_selection:
        character_selection.draw()
    else:
        # Update the game
        map.update()

        # Update and draw bullets
        if hasattr(map, 'player'):
            map.player.bullets.update()

        # Draw the map and elements
        map.draw()

        # Draw bullets
        if hasattr(map, 'player'):
            map.player.bullets.draw(frame)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
