import pygame
import os


class CharacterSelection:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # Charger les images des personnages pour le menu
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
        font_path = "assets/fonts/western.ttf"
        self.font = pygame.font.Font(font_path, 50)
        self.title_font = pygame.font.Font(font_path, 75)

        # Couleurs
        self.WHITE = (0, 0, 0)
        self.BLACK = (0, 0, 0)
        self.HIGHLIGHT_COLOR = (100, 100, 255)

    def draw(self):
        # charge l'image de fond
        background_image = pygame.image.load('assets/images/saloon1.jpg').convert()

        # redimensionne l'image pour qu'elle corresponde à la taille de l'écran
        background_image = pygame.transform.scale(
            background_image,
            (self.screen.get_width(), self.screen.get_height())
        )

        # Afficher l'image sur l'écran
        self.screen.blit(background_image, (0, 0))


        # Calculer les positions des personnages
        spacing = self.screen_width // 4
        start_x = spacing
        y = self.screen_height // 2 - 100

        # Noms des personnages
        character_names = ["McSonic", "McPeach", "Mcjoey"]

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
        if event.type == pygame.MOUSEMOTION:
            # Récupérer la position de la souris
            mouse_pos = event.pos
            spacing = self.screen_width // 4
            start_x = spacing
            y = self.screen_height // 2 - 100

            # Détecter sur quel personnage la souris est positionnée
            for i, character in enumerate(self.characters):
                x = start_x + i * spacing
                char_rect = character.get_rect(center=(x, y))
                if char_rect.collidepoint(mouse_pos):  # Si la souris est sur le personnage
                    self.selected_index = i  # Mettre à jour l'index sélectionné
                    break  # Sortir de la boucle après avoir trouvé un personnage

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Détecter un clic gauche de souris
            if event.button == 1:  # 1 signifie clic gauche
                mouse_pos = event.pos
                spacing = self.screen_width // 4
                start_x = spacing
                y = self.screen_height // 2 - 100

                # Vérifier quel personnage a été cliqué
                for i, character in enumerate(self.characters):
                    x = start_x + i * spacing
                    char_rect = character.get_rect(center=(x, y))
                    if char_rect.collidepoint(mouse_pos):  # Si la souris est sur le personnage
                        self.selected_index = i  # Mettre à jour l'index sélectionné
                        return "character_selected", self.selected_index  # Retourne l'index du personnage sélectionné

        return None