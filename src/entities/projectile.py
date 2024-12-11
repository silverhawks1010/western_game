import pygame
import math
from src.core.settings import *
from src.entities import Player, Bandit


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, damage, shooter_type='player', groups=None):
        super().__init__(groups) if groups else super().__init__()

        # Caractéristiques du projectile
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.shooter_type = shooter_type  # 'player' ou 'enemy'

        # Création du sprite
        self.width = 8
        self.height = 4
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW if shooter_type == 'player' else RED)

        # Rectangle de collision
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Direction et mouvement
        self.direction = pygame.math.Vector2(direction)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Durée de vie du projectile
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 2000  # 2 secondes

        # Rotation de l'image selon la direction
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        self.image = pygame.transform.rotate(self.image, angle)

    def move(self, dt):
        """Déplace le projectile selon sa direction et sa vitesse"""
        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

    def check_collision(self, targets):
        """Vérifie les collisions avec les cibles"""
        for target in targets:
            if self.rect.colliderect(target.rect):
                # Ne pas se blesser soi-même
                if (self.shooter_type == 'player' and not isinstance(target, Player)) or \
                        (self.shooter_type == 'enemy' and not isinstance(target, Bandit)):
                    target.take_damage(self.damage)
                    return True
        return False

    def should_destroy(self):
        """Vérifie si le projectile doit être détruit"""
        current_time = pygame.time.get_ticks()
        # Détruire si hors écran ou si durée de vie dépassée
        if (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT or
                current_time - self.spawn_time > self.lifetime):
            return True
        return False

    def update(self, dt, targets=None):
        """Met à jour l'état du projectile"""
        self.move(dt)

        if targets and self.check_collision(targets):
            return True

        return self.should_destroy()

    def draw(self, surface):
        """Dessine le projectile"""
        surface.blit(self.image, self.rect)

    @staticmethod
    def create_player_bullet(x, y, direction):
        """Crée une balle de joueur"""
        return Projectile(x, y, direction, BULLET_SPEED, DAMAGE_NORMAL, 'player')

    @staticmethod
    def create_enemy_bullet(x, y, direction):
        """Crée une balle d'ennemi"""
        return Projectile(x, y, direction, BULLET_SPEED * 0.8, DAMAGE_NORMAL * 0.7, 'enemy')