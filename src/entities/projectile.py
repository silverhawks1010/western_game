import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, image, collision_layer):
        super().__init__()
        scale_factor = 0.3
        original_size = image.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self.image = pygame.transform.scale(image, new_size)

        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(position)
        self.direction = direction
        self.speed = 500
        self.rect.center = position
        self.collision_layer = collision_layer

    def check_collision(self):
        # Vérifier si la balle touche un objet de la couche de collision
        bullet_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        for obj in self.collision_layer:
            obstacle_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if bullet_rect.colliderect(obstacle_rect):
                return True
        return False

    def update(self, delta_time=1 / 60):
        # Déplacer la balle
        if self.direction == 'up':
            self.position.y -= self.speed * delta_time
        elif self.direction == 'down':
            self.position.y += self.speed * delta_time
        elif self.direction == 'left':
            self.position.x -= self.speed * delta_time
        elif self.direction == 'right':
            self.position.x += self.speed * delta_time

        # Mettre à jour la position du rectangle
        self.rect.center = self.position

        # Si la balle touche un obstacle, la détruire
        if self.check_collision():
            self.kill()