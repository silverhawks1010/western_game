import os
import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        # Load the custom font
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "western.ttf"), 74)
        self.options = ["Start Game", "Options", "Quit"]
        self.selected_option = 0

        # Get the size of the screen
        self.screen_width, self.screen_height = self.screen.get_size()

        # Load and scale the background image
        self.background = pygame.image.load(os.path.join("assets", "images", "ecran_titre.jpg"))
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def display_menu(self):
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                label = self.font.render(option, True, (250, 214, 57))
            else:
                label = self.font.render(option, True, (255, 255, 255))
            label_rect = label.get_rect(center=(self.screen_width*0.508, self.screen_height*0.22 + i * 85))
            self.screen.blit(label, label_rect)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    return "start_game"
                elif self.selected_option == 1:
                    return "quit"
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for i, option in enumerate(self.options):
                label = self.font.render(option, True, (255, 255, 255))
                label_rect = label.get_rect(center=(self.screen_width*0.508, self.screen_height*0.22 + i * 85))
                if label_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_option = i
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.selected_option == 0:
                    return "start_game"
                elif self.selected_option == 1:
                    return "quit"
        return None