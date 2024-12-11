import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(position)
        self.direction = direction
        self.speed = 0.8

        # Position initiale centrée sur le joueur
        self.rect.center = position

        # Ajustement de la position initiale selon la direction
        offset = 30  # Distance de départ du centre du joueur
        if self.direction == 'up':
            self.position.y -= offset
        elif self.direction == 'down':
            self.position.y += offset
        elif self.direction == 'left':
            self.position.x -= offset
        elif self.direction == 'right':
            self.position.x += offset

    def update(self):
        # Déplacement selon la direction
        if self.direction == 'up':
            self.position.y -= self.speed
        elif self.direction == 'down':
            self.position.y += self.speed
        elif self.direction == 'left':
            self.position.x -= self.speed
        elif self.direction == 'right':
            self.position.x += self.speed

        # Mise à jour de la position du rectangle
        self.rect.center = self.position