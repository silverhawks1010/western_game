import pygame
import math
import random
from src.core.settings import *


class Bandit(pygame.sprite.Sprite):
    def __init__(self, x, y, bandit_type='normal', groups=None):
        super().__init__(groups) if groups else super().__init__()
        # Type et stats de base selon le type de bandit
        self.bandit_type = bandit_type
        self.setup_bandit_stats()

        # Position et dimensions
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.hitbox = self.rect.inflate(-10, -10)

        # Variables de mouvement
        self.direction = pygame.math.Vector2()
        self.facing = 'left'
        self.moving = False
        self.can_move = True
        self.speed = ENEMY_SPEEDS[bandit_type]

        # Animation
        self.frame_index = 0
        self.animation_speed = 0.15
        self.load_animations()
        self.image = self.animations['idle_left'][0]

        # Combat
        self.can_shoot = True
        self.shoot_cooldown = random.randint(1000, 2000)  # Différent pour chaque bandit
        self.last_shot = pygame.time.get_ticks()
        self.aggro_range = 300  # Distance d'activation du bandit

    def setup_bandit_stats(self):
        """Configure les stats selon le type de bandit"""
        self.stats = {
            'weak': {
                'health': ENEMY_HEALTH['weak'],
                'damage': 10,
                'speed': ENEMY_SPEEDS['slow'],
                'reward': 50
            },
            'normal': {
                'health': ENEMY_HEALTH['normal'],
                'damage': 20,
                'speed': ENEMY_SPEEDS['normal'],
                'reward': 100
            },
            'strong': {
                'health': ENEMY_HEALTH['strong'],
                'damage': 30,
                'speed': ENEMY_SPEEDS['fast'],
                'reward': 200
            }
        }

        stats = self.stats[self.bandit_type]
        self.health = stats['health']
        self.max_health = stats['health']
        self.damage = stats['damage']
        self.speed = stats['speed']
        self.reward = stats['reward']

    def load_animations(self):
        """Charge les animations du bandit"""
        self.animations = {
            'idle_right': [],
            'idle_left': [],
            'walk_right': [],
            'walk_left': [],
            'shoot_right': [],
            'shoot_left': [],
            'die': []
        }

        # Créer une surface temporaire pour le développement
        # À remplacer par les vrais sprites plus tard
        color = (139, 0, 0) if self.bandit_type == 'strong' else \
            (165, 42, 42) if self.bandit_type == 'normal' else \
                (188, 39, 50)  # weak

        temp_surface = pygame.Surface((self.width, self.height))
        temp_surface.fill(color)

        # Ajouter le sprite temporaire à toutes les animations
        for key in self.animations:
            if 'left' in key:
                self.animations[key].append(pygame.transform.flip(temp_surface, True, False))
            else:
                self.animations[key].append(temp_surface.copy())

    def move_towards_player(self, player_pos, dt):
        """Déplace le bandit vers le joueur"""
        if not self.can_move:
            return

        # Calculer la direction vers le joueur
        target_x, target_y = player_pos
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)

        # Mettre à jour la direction si le joueur est à portée
        if dist <= self.aggro_range:
            self.direction.x = dx / dist if dist > 0 else 0
            self.direction.y = dy / dist if dist > 0 else 0
            self.moving = True
            self.facing = 'right' if dx > 0 else 'left'
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.moving = False

        # Appliquer le mouvement
        if self.moving:
            self.hitbox.x += self.direction.x * self.speed * dt
            self.hitbox.y += self.direction.y * self.speed * dt
            self.rect.center = self.hitbox.center

    def animate(self, dt):
        """Gère l'animation du bandit"""
        animation_type = 'walk_' if self.moving else 'idle_'
        animation_type += self.facing

        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.animations[animation_type]):
            self.frame_index = 0

        self.image = self.animations[animation_type][int(self.frame_index)]

    def take_damage(self, amount):
        """Gère les dégâts reçus"""
        self.health -= amount
        if self.health <= 0:
            return True  # Indique que le bandit est mort
        return False

    def try_shoot(self):
        """Tente de tirer si le cooldown est terminé"""
        current_time = pygame.time.get_ticks()
        if self.can_shoot and current_time - self.last_shot >= self.shoot_cooldown:
            self.last_shot = current_time
            return True
        return False

    def draw_health_bar(self, surface):
        """Dessine la barre de vie du bandit"""
        bar_width = self.width
        bar_height = 6
        bar_position = (self.rect.centerx - bar_width / 2, self.rect.top - 10)

        # Fond de la barre
        pygame.draw.rect(surface, RED,
                         (bar_position[0], bar_position[1], bar_width, bar_height))

        # Barre de vie actuelle
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, GREEN,
                         (bar_position[0], bar_position[1], health_width, bar_height))

    def update(self, player_pos, dt):
        """Met à jour l'état du bandit"""
        self.move_towards_player(player_pos, dt)
        self.animate(dt)

    def draw(self, surface):
        """Dessine le bandit et sa barre de vie"""
        surface.blit(self.image, self.rect)
        self.draw_health_bar(surface)