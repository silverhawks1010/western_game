import pygame
import sys
import os
from pygame import mixer

# Initialisation de Pygame
pygame.init()
mixer.init()

# Constantes
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Western Game"

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_assets()

    def load_assets(self):
        """Chargement des ressources du jeu"""
        # Chargement de la police
        try:
            self.font_path = os.path.join('assets', 'fonts', 'WesternBangBang-Regular.ttf')
            self.font = pygame.font.Font(self.font_path, 48)
        except:
            print("Erreur de chargement de la police, utilisation de la police système")
            self.font = pygame.font.SysFont(None, 48)

        # Chargement des sons
        self.sounds = {}
        sound_files = {
            'background': 'background_sound_theme_chill.mp3',
            'level_complete': 'fin_du_niveau.mp3',
            'walk_slow': 'marche_lente.mp3',
            'walk_fast': 'marche_rapide.mp3',
            'coin': 'obtenir_piece.mp3',
            'arcade': 'Theme_arcade.mp3'
        }
        
        for sound_name, file_name in sound_files.items():
            try:
                sound_path = os.path.join('assets', 'sounds', file_name)
                self.sounds[sound_name] = mixer.Sound(sound_path)
            except:
                print(f"Erreur de chargement du son: {file_name}")

        # Chargement des images
        try:
            self.background = pygame.image.load(
                os.path.join('assets', 'images', 'images.jpg')
            ).convert()
            self.background = pygame.transform.scale(
                self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        except:
            print("Erreur de chargement de l'image de fond")
            self.background = None

    def handle_events(self):
        """Gestion des événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Ajoutez ici d'autres contrôles

    def update(self):
        """Mise à jour du jeu"""
        pass  # À implémenter avec la logique du jeu

    def render(self):
        """Rendu du jeu"""
        # Affichage du fond
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)

        # Exemple de texte
        text = self.font.render("Western Game", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        """Boucle principale du jeu"""
        # Démarrer la musique de fond
        if 'background' in self.sounds:
            self.sounds['background'].play(-1)  # -1 pour loop infini

        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

def main():
    """Point d'entrée du jeu"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()