import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, image):
        super().__init__()
        # Redimensionner l'image de la balle
        scale_factor = 0.5  # Réduire de moitié, ajustez cette valeur selon vos besoins
        original_size = image.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self.image = pygame.transform.scale(image, new_size)

        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(position)
        self.direction = direction
        self.speed = 500
        self.rect.center = position

    def update(self, delta_time=1 / 60):
        # Le reste du code reste identique
        if self.direction == 'up':
            self.position.y -= self.speed * delta_time
        elif self.direction == 'down':
            self.position.y += self.speed * delta_time
        elif self.direction == 'left':
            self.position.x -= self.speed * delta_time
        elif self.direction == 'right':
            self.position.x += self.speed * delta_time

        self.rect.center = self.position