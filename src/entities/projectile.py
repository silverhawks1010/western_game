import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, image):
        super().__init__()
<<<<<<< Updated upstream
        self.image = pygame.transform.scale(image, (20, 20))  # Taille fixe pour mieux voir
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(position)
        self.direction = direction
        self.speed = 500
        self.rect.center = position
        self.hitbox = self.rect.inflate(-4, -4)

    def update(self, delta_time=1/60):
        # Mettre à jour la position
        move_amount = self.speed * delta_time
        if self.direction == 'up':
            self.position.y -= move_amount
        elif self.direction == 'down':
            self.position.y += move_amount
        elif self.direction == 'left':
            self.position.x -= move_amount
        elif self.direction == 'right':
            self.position.x += move_amount
=======
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.direction = direction
        self.speed = 300  # Adjust speed as needed

    def update(self, delta_time):
        if self.direction == 'up':
            self.rect.y -= self.speed * delta_time
        elif self.direction == 'down':
            self.rect.y += self.speed * delta_time
        elif self.direction == 'left':
            self.rect.x -= self.speed * delta_time
        elif self.direction == 'right':
            self.rect.x += self.speed * delta_time
>>>>>>> Stashed changes

    def draw(self, surface):
        print(self.image)
        surface.blit(self.image, self.rect.topleft)