import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, position, image_path, message, interaction_type='dialog'):
        super().__init__()
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.frames = self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)
        self.message = message
        self.interaction_type = interaction_type
        self.position = pygame.Vector2(position)
        self.frame_index = 0
        self.animation_speed = 100
        self.last_update = pygame.time.get_ticks()
        self.hitbox = self.rect.inflate(-self.rect.width * 0.90, -self.rect.height * 0.90)
        self.font = pygame.font.Font(None, 24)  # Font for the dialog text

        try:
            self.image = pygame.image.load('assets/images/sprite/npc/npc.png').convert_alpha()
        except:
            self.image = pygame.Surface((32, 48))
            self.image.fill((255, 0, 0))  # Red rectangle as fallback

        self.rect = self.image.get_rect(center=position)

        # Death animation
        self.dying = False
        self.death_animation_frame = 0
        self.death_animation_timer = 0
        self.death_animation_speed = 0.1

        # Death sound
        try:
            self.death_sound = pygame.mixer.Sound('assets/sounds/npc_death.wav')
            self.death_sound.set_volume(0.2)
        except:
            self.death_sound = None

    def load_frames(self):
        frames = []
        frame_width = self.sprite_sheet.get_width() // 7
        frame_height = self.sprite_sheet.get_height()
        for i in range(7):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def update(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
        self.hitbox.center = self.rect.center

    def draw_dialog(self, screen):
        text_surface = self.font.render(self.message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midbottom=self.rect.midtop)
        text_rect.y -= 10  # Adjust position above the NPC
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(10, 10))  # Background for the text
        screen.blit(text_surface, text_rect)

    def kill(self):
        if self.death_sound:
            self.death_sound.play()
        print("NPC killed!")  # Debug
        super().kill()