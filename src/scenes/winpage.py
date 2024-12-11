# src/scenes/winpage.py

import pygame

class WinScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 64)
        self.message = "You Win!"
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.button_font = pygame.font.SysFont('Arial', 32)
        self.button_text = "Terminer"
        self.button_color = (255, 0, 0)
        self.button_rect = pygame.Rect(0, 0, 200, 50)
        self.button_rect.center = (self.screen.get_width() // 2, self.screen.get_height() - 100)

    def display(self):
        self.screen.fill(self.bg_color)
        text_surface = self.font.render(self.message, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_surface, text_rect)

        button_surface = self.button_font.render(self.button_text, True, self.text_color)
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        self.screen.blit(button_surface, button_surface.get_rect(center=self.button_rect.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                return "home"
        return None