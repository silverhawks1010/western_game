import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.idle_sprite_sheet = pygame.image.load("assets/images/sprite/mainchara/idle/cowboy_idle_spritesheet.png").convert_alpha()
        self.walk_sprite_sheet = pygame.image.load("assets/images/sprite/mainchara/walk/cowboy_walk_up_spritesheet.png").convert_alpha()
        self.idle_images = self.load_idle_images()
        self.walk_images = self.load_walk_images()
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect(center=position)
        self.speed = 1
        self.idle = True
        self.idle_index = 0
        self.idle_timer = 0
        self.walk_index = 0
        self.walk_timer = 0

    def load_idle_images(self):
        idle_images = []
        frame_width = self.idle_sprite_sheet.get_width() // 4  # Assuming 4 frames in the sprite sheet
        frame_height = self.idle_sprite_sheet.get_height()
        for i in range(4):
            frame = self.idle_sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))  # Scale the frame
            idle_images.append(frame)
        return idle_images

    def load_walk_images(self):
        walk_images = []
        frame_width = self.walk_sprite_sheet.get_width() // 4  # Assuming 4 frames in the sprite sheet
        frame_height = self.walk_sprite_sheet.get_height()
        for i in range(4):
            frame = self.walk_sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))  # Scale the frame
            walk_images.append(frame)
        return walk_images

    def update(self):
        keys = pygame.key.get_pressed()
        self.idle = True
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.idle = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.idle = False
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.idle = False
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.idle = False

        if self.idle:
            self.update_idle_animation()
        else:
            self.update_walk_animation()

    def update_idle_animation(self):
        self.idle_timer += 1
        if self.idle_timer >= 10:  # Adjust the speed of the animation
            self.idle_timer = 0
            self.idle_index = (self.idle_index + 1) % len(self.idle_images)
            self.image = self.idle_images[self.idle_index]

    def update_walk_animation(self):
        self.walk_timer += 1
        if self.walk_timer >= 10:  # Adjust the speed of the animation
            self.walk_timer = 0
            self.walk_index = (self.walk_index + 1) % len(self.walk_images)
            self.image = self.walk_images[self.walk_index]