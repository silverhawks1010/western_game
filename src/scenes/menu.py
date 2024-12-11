import os
import pygame


class Popup:
    def __init__(self, screen, message):
        self.screen = screen
        self.message = message
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "western.ttf"), 74)
        self.width, self.height = 300, 200
        self.rect = pygame.Rect((self.screen.get_width() - self.width) // 2,
                                (self.screen.get_height() - self.height) // 2, self.width, self.height)
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


class OptionsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.parent = None
        self.font = pygame.font.Font(None, 36)
        self.width, self.height = 500, 400
        self.rect = pygame.Rect(
            (screen.get_width() - self.width) // 2,
            (screen.get_height() - self.height) // 2,
            self.width, self.height
        )

        # Couleurs
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.button_color = (100, 100, 100)
        self.hover_color = (150, 150, 150)

        # Options
        self.settings = {
            'fullscreen': pygame.display.get_surface().get_flags() & pygame.FULLSCREEN,
            'music_volume': 50,
            'sfx_volume': 50
        }

        # Création des boutons
        button_height = 40
        spacing = 20
        start_y = self.rect.y + 50

        # Sliders
        self.music_slider = pygame.Rect(self.rect.x + 200, start_y, 200, button_height)
        self.sfx_slider = pygame.Rect(self.rect.x + 200, start_y + button_height + spacing, 200, button_height)

        # Bouton Plein écran
        self.fullscreen_button = pygame.Rect(
            self.rect.x + 200,
            start_y + (button_height + spacing) * 2,
            200,
            button_height
        )

        # Bouton Retour
        self.back_button = pygame.Rect(
            self.rect.centerx - 50,
            self.rect.bottom - 60,
            100,
            button_height
        )

        self.dragging = None

    def display(self):
        # Fond
        pygame.draw.rect(self.screen, self.bg_color, self.rect)

        # Titre
        title = self.font.render("Options", True, self.text_color)
        title_rect = title.get_rect(centerx=self.rect.centerx, y=self.rect.y + 20)
        self.screen.blit(title, title_rect)

        # Volume Musique
        text = self.font.render(f"Musique: {self.settings['music_volume']}%", True, self.text_color)
        self.screen.blit(text, (self.rect.x + 20, self.music_slider.y))
        pygame.draw.rect(self.screen, self.button_color, self.music_slider)
        slider_pos = self.music_slider.x + (self.music_slider.width * self.settings['music_volume'] / 100)
        pygame.draw.rect(self.screen, self.text_color,
                         (slider_pos - 5, self.music_slider.y, 10, self.music_slider.height))

        # Volume SFX
        text = self.font.render(f"Effets: {self.settings['sfx_volume']}%", True, self.text_color)
        self.screen.blit(text, (self.rect.x + 20, self.sfx_slider.y))
        pygame.draw.rect(self.screen, self.button_color, self.sfx_slider)
        slider_pos = self.sfx_slider.x + (self.sfx_slider.width * self.settings['sfx_volume'] / 100)
        pygame.draw.rect(self.screen, self.text_color,
                         (slider_pos - 5, self.sfx_slider.y, 10, self.sfx_slider.height))

        # Bouton Plein écran
        pygame.draw.rect(self.screen, self.button_color, self.fullscreen_button)
        text = self.font.render("Plein écran: " + ("Oui" if self.settings['fullscreen'] else "Non"),
                                True, self.text_color)
        text_rect = text.get_rect(center=self.fullscreen_button.center)
        self.screen.blit(text, text_rect)

        # Bouton Retour
        pygame.draw.rect(self.screen, self.button_color, self.back_button)
        text = self.font.render("Retour", True, self.text_color)
        text_rect = text.get_rect(center=self.back_button.center)
        self.screen.blit(text, text_rect)

    def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if self.music_slider.collidepoint(mouse_pos):
                    self.dragging = 'music'
                elif self.sfx_slider.collidepoint(mouse_pos):
                    self.dragging = 'sfx'
                elif self.fullscreen_button.collidepoint(mouse_pos):
                    self.settings['fullscreen'] = not self.settings['fullscreen']
                    if self.settings['fullscreen']:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1024, 768))

                    # Mettre à jour l'écran et le menu parent
                    self.screen = screen
                    if self.parent:
                        self.parent.screen = screen
                        self.parent.screen_width = screen.get_width()
                        self.parent.screen_height = screen.get_height()

                        # Recharger et redimensionner le background
                        self.parent.background = pygame.image.load(os.path.join("assets", "images", "ecran_titre.jpg"))
                        self.parent.background = pygame.transform.scale(
                            self.parent.background,
                            (self.parent.screen_width, self.parent.screen_height)
                        )
                        self.parent.background_rect = self.parent.background.get_rect(
                            center=(self.parent.screen_width // 2, self.parent.screen_height // 2)
                        )

                    # Réinitialiser le menu d'options
                    self.__init__(screen)

                elif self.back_button.collidepoint(mouse_pos):
                    return True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = None

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                mouse_x = event.pos[0]
                if self.dragging == 'music':
                    slider = self.music_slider
                    relative_x = max(0, min(mouse_x - slider.x, slider.width))
                    self.settings['music_volume'] = int((relative_x / slider.width) * 100)
                elif self.dragging == 'sfx':
                    slider = self.sfx_slider
                    relative_x = max(0, min(mouse_x - slider.x, slider.width))
                    self.settings['sfx_volume'] = int((relative_x / slider.width) * 100)

            return False

class Menu:
        def __init__(self, screen):
            self.options_menu = None
            self.screen = screen
            self.options = ["Start Game", "Options", "Quit"]

            # Dimensions de base
            self.base_width = 1920
            self.base_height = 1080
            self.screen_width = self.screen.get_width()
            self.screen_height = self.screen.get_height()

            # Mise à l'échelle
            self.scale_x = self.screen_width / self.base_width
            self.scale_y = self.screen_height / self.base_height
            self.font_size = int(74 * min(self.scale_x, self.scale_y))
            self.font = pygame.font.Font(os.path.join("assets", "fonts", "western.ttf"), self.font_size)

            # Background
            self.background = pygame.image.load(os.path.join("assets", "images", "ecran_titre.jpg"))
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
            self.background_rect = self.background.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

            # Audio
            self.hover_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "hover_sound.mp3"))
            self.bg_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "main_music.mp3"))
            self.bg_channel = pygame.mixer.Channel(0)
            self.hover_channel = pygame.mixer.Channel(1)
            self.bg_channel.set_volume(0.1)
            self.bg_channel.play(self.bg_sound, loops=-1)

            self.selected_option = -1

        def display_menu(self):
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, self.background_rect)

            spacing = int(self.font_size * 1.5)
            start_y = int(self.screen_height * 0.22)

            for i, option in enumerate(self.options):
                if i == self.selected_option:
                    color = (250, 214, 57)
                else:
                    color = (255, 255, 255)

                label = self.font.render(option, True, color)
                label_rect = label.get_rect(center=(self.screen_width // 2, start_y + i * spacing))
                self.screen.blit(label, label_rect)

            if self.options_menu:
                self.options_menu.display()

            pygame.display.flip()

        def handle_event(self, event):
            if self.options_menu:
                if self.options_menu.handle_event(event):
                    self.bg_channel.set_volume(self.options_menu.settings['music_volume'] / 100)
                    self.hover_channel.set_volume(self.options_menu.settings['sfx_volume'] / 100)
                    self.options_menu = None
                return None

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                spacing = int(self.font_size * 1.5)
                start_y = int(self.screen_height * 0.22)

                for i, option in enumerate(self.options):
                    label = self.font.render(option, True, (255, 255, 255))
                    label_rect = label.get_rect(center=(self.screen_width // 2, start_y + i * spacing))
                    if label_rect.collidepoint(mouse_x, mouse_y):
                        if self.selected_option != i:
                            self.hover_channel.play(self.hover_sound)
                        self.selected_option = i
                        return None

                self.selected_option = -1

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.selected_option == 0:
                    return "start_game"
                elif self.selected_option == 1:
                    self.options_menu = OptionsMenu(self.screen)
                    self.options_menu.parent = self
                elif self.selected_option == 2:
                    return "quit"

            return None