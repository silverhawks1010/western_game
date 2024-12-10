import os
import pygame

class Popup:
    def __init__(self, screen, message):
        self.screen = screen
        self.message = message
        self.font = pygame.font.Font(None, 36)
        self.width, self.height = 300, 200
        self.rect = pygame.Rect((self.screen.get_width() - self.width) // 2, (self.screen.get_height() - self.height) // 2, self.width, self.height)
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.button_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 150, 100, 30)
        self.button_color = (100, 100, 100)
        self.button_text = "OK"

    def display(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.message, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 20))
        self.screen.blit(text_surface, text_rect)
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        button_text_surface = self.font.render(self.button_text, True, self.text_color)
        button_text_rect = button_text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text_surface, button_text_rect)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                return True
        return False

class Menu:
    def __init__(self, screen):
        self.popup = None
        self.screen = screen
        self.options = ["Start Game", "Options", "Quit"]
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "western.ttf"), 74)
        self.selected_option = -1

        # Get the size of the screen
        self.screen_width, self.screen_height = self.screen.get_size()

        # Load and scale the background image
        self.background = pygame.image.load(os.path.join("assets", "images", "ecran_titre.jpg"))
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        # Load sounds
        self.hover_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "hover_sound.mp3"))
        self.bg_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "main_music.mp3"))

        # Initialize audio channels
        self.bg_channel = pygame.mixer.Channel(0)
        self.hover_channel = pygame.mixer.Channel(1)

        # Play background sound
        self.bg_channel.set_volume(0.05)
        self.bg_channel.play(self.bg_sound, loops=-1)

    def display_menu(self):
        self.screen.blit(self.background, (0, 0))
        font_size = int(self.screen_height * 0.07)  # Calculate font size based on screen height
        font = pygame.font.Font(os.path.join("assets", "fonts", "western.ttf"), font_size)
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                label = font.render(option, True, (250, 214, 57))
            else:
                label = font.render(option, True, (255, 255, 255))
            label_rect = label.get_rect(center=(self.screen_width*0.508, self.screen_height*0.22 + i * (font_size + 10)))
            self.screen.blit(label, label_rect)
        if self.popup:
            self.popup.display()
        pygame.display.flip()

    def handle_event(self, event):
        if self.popup:
            if self.popup.handle_event(event):
                self.popup = None
            return None

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            hovered = False
            for i, option in enumerate(self.options):
                label = self.font.render(option, True, (255, 255, 255))
                label_rect = label.get_rect(center=(self.screen_width * 0.508, self.screen_height * 0.22 + i * 85))
                if label_rect.collidepoint(mouse_x, mouse_y):
                    if self.selected_option != i:
                        self.hover_channel.play(self.hover_sound)
                    self.selected_option = i
                    hovered = True
            if not hovered:
                self.selected_option = -1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.selected_option == 0:
                    return "start_game"
                elif self.selected_option == 1:
                    self.popup = Popup(self.screen, "Voulez-vous couper le son ?")
                elif self.selected_option == 2:
                    return "quit"
        return None