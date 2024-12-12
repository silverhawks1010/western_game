import pygame
import os


class CharacterSelection:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # Charger les images des personnages
        self.characters = [
            pygame.image.load('assets/images/sprite/mainchara/BLEUFACE.png').convert_alpha(),
            pygame.image.load('assets/images/sprite/mainchara/ORANGEFACE.png').convert_alpha(),
            pygame.image.load('assets/images/sprite/mainchara/westernFACE.png').convert_alpha()
        ]

        # Redimensionner les personnages
        self.characters = [pygame.transform.scale(char, (200, 300)) for char in self.characters]

        # Index du personnage sélectionné
        self.selected_index = 0

        # Polices
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 75)

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.HIGHLIGHT_COLOR = (100, 100, 255)

    def draw(self):
        # Charger l'image de fond (assurez-vous de l'avoir initialisée dans le constructeur)
        background_image = pygame.image.load('assets/images/saloon.jpg').convert()

        # Redimensionner l'image pour qu'elle corresponde à la taille de l'écran
        background_image = pygame.transform.scale(
            background_image,
            (self.screen.get_width(), self.screen.get_height())
        )

        # Afficher l'image sur l'écran
        self.screen.blit(background_image, (0, 0))

        # Cette section me permet de choisir le titre qui se trouve en haut
        title = self.title_font.render("", True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)

        # Calculer les positions des personnages
        spacing = self.screen_width // 4
        start_x = spacing
        y = self.screen_height // 2 - 150

        # Noms des personnages
        character_names = ["MacSonic", "MacPeach", "Macjoey"]

        # Dessiner les personnages
        for i, character in enumerate(self.characters):
            x = start_x + i * spacing
            char_rect = character.get_rect(center=(x, y))

            # Surligner le personnage sélectionné
            if i == self.selected_index:
                pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOR,
                                 (char_rect.x - 10, char_rect.y - 10,
                                  char_rect.width + 20, char_rect.height + 20), 4)

            self.screen.blit(character, char_rect)

            # Afficher le nom du personnage
            name = self.font.render(character_names[i], True, self.WHITE)
            name_rect = name.get_rect(center=(x, y + 200))
            self.screen.blit(name, name_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Se déplacer vers la gauche
                self.selected_index = (self.selected_index - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                # Se déplacer vers la droite
                self.selected_index = (self.selected_index + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                # Retourner l'index du personnage sélectionné
                return "character_selected", self.selected_index
        return None