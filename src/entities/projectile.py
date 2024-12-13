import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, image):
        super().__init__()
        scale_factor = 0.5
        original_size = image.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self.image = pygame.transform.scale(image, new_size)

        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(position)
        self.direction = direction
        self.speed = 300  # Vitesse réduite pour mieux voir les balles
        self.rect.center = position

        # Hitbox plus petite mais pas trop pour faciliter les collisions
        self.hitbox = self.rect.inflate(-2, -2)

    def update(self, delta_time=1/60):
        # Mettre à jour la position
        if self.direction == 'up':
            self.position.y -= self.speed * delta_time
        elif self.direction == 'down':
            self.position.y += self.speed * delta_time
        elif self.direction == 'left':
            self.position.x -= self.speed * delta_time
        elif self.direction == 'right':
            self.position.x += self.speed * delta_time

        # Mettre à jour le rect et la hitbox
        self.rect.center = self.position
        self.hitbox.center = self.position