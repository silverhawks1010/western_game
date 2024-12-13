import pygame
import random
import math
from src.scenes.winpage import WinScene

class Crosshair:
    def __init__(self):
        self.size = 20
        self.color = (255, 255, 255)  # Blanc
        self.thickness = 2

    def draw(self, screen, pos):
        x, y = pos
        # Ligne horizontale
        pygame.draw.line(screen, self.color, (x - self.size, y), (x + self.size, y), self.thickness)
        # Ligne verticale
        pygame.draw.line(screen, self.color, (x, y - self.size), (x, y + self.size), self.thickness)
        # Petit cercle au centre
        pygame.draw.circle(screen, self.color, (x, y), 3)
        # Cercle extérieur
        pygame.draw.circle(screen, self.color, (x, y), self.size, self.thickness)

class GunSprite:
    def __init__(self, screen_width, screen_height):
        # Charger l'image du sprite
        self.spritesheet = pygame.image.load('assets/images/biggun.png')

        # Dimensions de chaque frame
        self.frame_width = self.spritesheet.get_width() // 4
        self.frame_height = self.spritesheet.get_height()

        # Charger le son de tir
        self.shoot_sound = pygame.mixer.Sound('assets/sounds/combat_shoot.mp3')

        # Créer les frames avec une plus grande taille
        self.frames = []
        scale_factor = 1.5
        for i in range(4):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            new_width = int(self.frame_width * scale_factor)
            new_height = int(self.frame_height * scale_factor)
            frame = pygame.transform.scale(frame, (new_width, new_height))
            self.frames.append(frame)

            # Position de base du pistolet (encore plus bas)
            self.base_x = screen_width - self.frames[0].get_width() - 40
            self.base_y = screen_height - self.frames[0].get_height() + 80  # Augmenté de 30 à 80

            # Position actuelle
            self.x = self.base_x
            self.y = self.base_y

            # Paramètres de suivi de la souris augmentés
            self.follow_strength = 0.4  # Augmenté de 0.3 à 0.4
            self.max_offset_x = 70  # Augmenté de 40 à 70
            self.max_offset_y = 50  # Augmenté de 30 à 50

            # Le reste des attributs reste identique
            self.current_frame = 0
            self.is_animating = False
            self.animation_speed = 0.1
            self.animation_timer = 0
            self.screen_width = screen_width
            self.screen_height = screen_height

    def update_position(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos

        # Calculer la distance relative entre la souris et le centre de l'écran
        screen_center_x = self.screen_width // 2
        screen_center_y = self.screen_height // 2

        # Normaliser les distances (-1 à 1)
        dx = (mouse_x - screen_center_x) / (self.screen_width / 2)
        dy = (mouse_y - screen_center_y) / (self.screen_height / 2)

        # Appliquer les offsets avec lissage
        offset_x = dx * self.max_offset_x * self.follow_strength
        offset_y = dy * self.max_offset_y * self.follow_strength

        # Mettre à jour progressivement la position
        self.x = self.base_x + offset_x
        self.y = self.base_y + offset_y

    def start_animation(self):
        if not self.is_animating:
            self.is_animating = True
            self.current_frame = 0
            self.animation_timer = 0
            self.shoot_sound.play()

    def update(self, delta_time):
        if self.is_animating:
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0
                    self.is_animating = False

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))


class Target:
    def __init__(self, moving=False):
        self.size_options = {
            'large': {'radius': 50, 'multiplier': 1},
            'medium': {'radius': 35, 'multiplier': 1.5},
            'small': {'radius': 20, 'multiplier': 2.5},
            'tiny': {'radius': 12, 'multiplier': 4}
        }
        self.size = random.choice(list(self.size_options.keys()))
        self.radius = self.size_options[self.size]['radius']
        self.point_multiplier = self.size_options[self.size]['multiplier']
        self.rail = random.randint(0, 2)
        self.y = 200 + (self.rail * 100)

        # Position initiale et direction de mouvement
        self.direction = random.choice([-1, 1])  # -1 pour gauche, 1 pour droite
        if self.direction == 1:
            self.x = -self.radius  # Commence à gauche de l'écran
        else:
            self.x = pygame.display.get_surface().get_width() + self.radius  # Commence à droite de l'écran

        self.active = True
        self.visible = True
        self.moving = moving

        # Vitesse de déplacement pour les cibles mobiles
        if moving:
            # Augmentation significative de la vitesse
            self.speed = random.uniform(400, 600)  # Vitesse entre 400 et 600 pixels par seconde
            self.has_timer = False
        else:
            self.speed = 0
            self.x = random.randint(self.radius, pygame.display.get_surface().get_width() - self.radius)
            self.has_timer = True
            self.apparition_time = random.uniform(1, 3)
            self.disparition_time = pygame.time.get_ticks() + self.apparition_time * 1000

    def move(self, delta_time, screen_width):
        # Pour les cibles statiques avec timer
        if self.has_timer and pygame.time.get_ticks() > self.disparition_time:
            self.visible = False
            self.active = False
            return

        if self.moving:
            # Déplacement horizontal
            self.x += self.speed * self.direction * delta_time

            # Désactiver la cible si elle sort complètement de l'écran
            if self.direction == 1 and self.x > screen_width + self.radius * 2:
                self.active = False
            elif self.direction == -1 and self.x < -self.radius * 2:
                self.active = False

    def draw(self, screen):
        if self.active and self.visible:  # Vérifier si la cible est active et visible
            pygame.draw.rect(screen, (101, 67, 33), (self.x - 5, self.y - self.radius, 10, self.radius * 2 + 20))
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), int(self.radius * 0.8))
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), int(self.radius * 0.6))
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), int(self.radius * 0.4))
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), int(self.radius * 0.2))


class Combat:
    def __init__(self, frame, player, pnj, combat_number=1):  # Ajout de combat_number
        self.frame = frame
        self.player = player
        self.pnj = pnj
        self.combat_number = combat_number  # Stocker le numéro du combat
        self.running = True
        self.targets = []
        self.score = 0
        self.shots = 0
        self.hits = 0
        self.accuracy = 0
        self.font = pygame.font.Font('assets/fonts/western.ttf', 48)
        self.small_font = pygame.font.Font('assets/fonts/western.ttf', 32)
        self.sign_bg = pygame.image.load('assets/images/pancarte.png')
        self.sign_bg = pygame.transform.scale(self.sign_bg, (400, 350))
        self.start_time = pygame.time.get_ticks()
        self.game_time = 30
        self.background = pygame.image.load('assets/images/shooter_bg.png')
        self.background = pygame.transform.scale(self.background, self.frame.get_size())
        self.clock = pygame.time.Clock()
        self.gun = GunSprite(self.frame.get_width(), self.frame.get_height())
        self.crosshair = Crosshair()
        # Charger le son d'impact
        self.hit_sound = pygame.mixer.Sound('assets/sounds/bullet_hitmetal.mp3')
        # Cacher le curseur au début du jeu
        pygame.mouse.set_visible(False)
        # Couleurs pour le HUD
        self.text_color = (255, 255, 255)  # Blanc
        self.highlight_color = (255, 215, 0)  # Or pour les valeurs importantes

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mouse.set_visible(True)  # Réafficher le curseur en quittant
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.gun.start_animation()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.shots += 1
            for target in self.targets:
                distance = math.sqrt((mouse_x - target.x)**2 + (mouse_y - target.y)**2)
                if distance < target.radius:
                    points = int(100 * target.point_multiplier * (1 - distance/target.radius))
                    self.score += points
                    self.hits += 1
                    target.active = False
                    self.hit_sound.play()

    def update(self, delta_time):
        if pygame.time.get_ticks() - self.start_time > self.game_time * 1000:
            self.running = False
            self.end_game()

        # Gérer les cibles en fonction du numéro de combat
        if len(self.targets) < 5:
            # Combat 2 : cibles mobiles
            if self.combat_number == 2:
                self.targets.append(Target(moving=True))
            # Combat 1 : cibles statiques
            else:
                self.targets.append(Target(moving=False))

        # Mettre à jour toutes les cibles
        for target in self.targets:
            target.move(delta_time, self.frame.get_width())

        # Nettoyer les cibles inactives
        self.targets = [target for target in self.targets if target.active]

        if self.shots > 0:
            self.accuracy = (self.hits / self.shots) * 100

        self.gun.update(delta_time)
        self.gun.update_position(pygame.mouse.get_pos())

    def draw(self):
        self.frame.blit(self.background, (0, 0))
        for target in self.targets:
            target.draw(self.frame)

        # Créer un fond semi-transparent pour le HUD
        hud_surface = pygame.Surface((250, 150))  # Ajuster la taille du fond si nécessaire
        hud_surface.set_alpha(128)  # Définir la transparence (0 = transparent, 255 = opaque)
        hud_surface.fill((0, 0, 0))  # Remplir le fond de noir
        hud_rect = hud_surface.get_rect(bottomright=(self.frame.get_width() - 10, self.frame.get_height() - 10))
        self.frame.blit(self.sign_bg, (-40, -40))

        # Score (positionné en haut à gauche)
        score_label = self.small_font.render("SCORE", True, self.text_color)
        score_value = self.font.render(str(self.score), True, self.highlight_color)
        self.frame.blit(score_label, (75, 92))  # Position fixe en haut à gauche
        self.frame.blit(score_value, (75, 118))  # Position fixe en haut à gauche

        # Précision (positionné en haut à gauche)
        accuracy = f"{self.accuracy:.1f}%" if self.shots > 0 else "0.0%"
        accuracy_label = self.small_font.render("PRECISION", True, self.text_color)
        accuracy_value = self.font.render(accuracy, True, self.highlight_color)
        self.frame.blit(accuracy_label, (75, 162))  # Position fixe en haut à gauche
        self.frame.blit(accuracy_value, (75, 188))  # Position fixe en haut à gauche

        # Timer (coin supérieur droit)
        timer_surface = pygame.Surface((120, 100))
        timer_surface.set_alpha(128)
        timer_surface.fill((0, 0, 0))
        self.frame.blit(timer_surface, (self.frame.get_width() - 130, 10))

        timer_label = self.small_font.render("TEMPS", True, self.text_color)
        time_left = max(0, self.game_time - (pygame.time.get_ticks() - self.start_time) // 1000)
        timer_value = self.font.render(f"{time_left}s", True,
                                       (255, 50, 50) if time_left <= 3 else self.highlight_color)

        timer_label_rect = timer_label.get_rect()
        timer_label_rect.topright = (self.frame.get_width() - 20, 20)
        timer_value_rect = timer_value.get_rect()
        timer_value_rect.topright = (self.frame.get_width() - 20, 55)

        self.frame.blit(timer_label, timer_label_rect)
        self.frame.blit(timer_value, timer_value_rect)

        # Dessiner l'arme et le viseur
        self.gun.draw(self.frame)
        self.crosshair.draw(self.frame, pygame.mouse.get_pos())

    def end_game(self):
        # Réafficher le curseur à la fin du jeu
        pygame.mouse.set_visible(True)
        print(f"Score: {self.score}")
        print(f"Shots: {self.accuracy}")
        if self.accuracy < 1 or self.score < 10:
            print("Défaite! Votre précision est inférieure à 50% ou votre score est insuffisant.")
        else:
            print("Victoire! Vous avez gagné.")
            self.player.points += 5
            self.player.money += int(self.accuracy * 10)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(delta_time)
            self.draw()
            pygame.display.flip()