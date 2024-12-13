import pygame
import math
from src.entities.npc import NPC


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        # Chargement du sprite sheet du bandit
        try:
            self.sprite_sheet = pygame.image.load('assets/images/sprite/npc/bandit_du_desert.png').convert_alpha()
        except Exception as e:
            print(f"Erreur lors du chargement du sprite bandit: {e}")
            self.sprite_sheet = pygame.Surface((32, 32))
            self.sprite_sheet.fill((255, 0, 0))

        # Configuration de l'ennemi
        self.speed = 40
        self.health = 2
        self.hit_cooldown = 0  # Cooldown entre les impacts
        self.damage_cooldown = 2000
        self.last_damage_time = 0
        self.detection_range = 200
        self.is_chasing = False

        # Système de recul
        self.knockback_distance = 200  # Distance de recul
        self.knockback_duration = 0.5  # Durée du recul en secondes
        self.is_knocked_back = False
        self.knockback_timer = 0
        self.knockback_direction = pygame.math.Vector2(0, 0)

        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.2
        self.frames = self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-20, -20)

        # Système de clignotement
        self.is_flashing = False
        self.flash_duration = 0.2  # Durée du flash en secondes
        self.flash_timer = 0
        self.flash_interval = 0.05  # Durée entre chaque alternance de visibilité
        self.flash_visible = True
        self.original_frames = None

    def take_damage(self):
        current_time = pygame.time.get_ticks()
        if current_time > self.hit_cooldown:
            self.health -= 1
            self.hit_cooldown = current_time + 500  # 500ms de cooldown entre les impacts
            self.start_flash()  # On a déjà la méthode start_flash donc on l'utilise directement
            return True
        return False

    def start_flash(self):
        self.is_flashing = True
        self.flash_timer = self.flash_duration
        self.flash_visible = True
        # Sauvegarder les frames originales
        self.original_frames = self.frames.copy()
        # Créer les frames blanches pour le flash
        self.white_frames = []
        for frame in self.frames:
            white_frame = frame.copy()
            white_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            white_surface.fill((255, 255, 255, 150))  # Blanc semi-transparent
            white_frame.blit(white_surface, (0, 0))
            self.white_frames.append(white_frame)

    def update_flash(self, delta_time):
        if self.is_flashing:
            self.flash_timer -= delta_time

            # Alterner entre visible et invisible
            if self.flash_timer % self.flash_interval < self.flash_interval / 2:
                self.frames = self.white_frames
            else:
                self.frames = self.original_frames

            # Mettre à jour l'image actuelle
            self.image = self.frames[self.animation_frame]

            # Arrêter le flash quand le timer est écoulé
            if self.flash_timer <= 0:
                self.is_flashing = False
                self.frames = self.original_frames
                self.image = self.frames[self.animation_frame]

    def load_frames(self):
        frames = []
        frame_width = self.sprite_sheet.get_width() // 6
        frame_height = self.sprite_sheet.get_height()

        for i in range(6):
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def apply_knockback(self, player_pos):
        # Calculer la direction de recul (direction opposée au joueur)
        dx = self.hitbox.centerx - player_pos[0]
        dy = self.hitbox.centery - player_pos[1]

        # Normaliser le vecteur
        length = math.sqrt(dx * dx + dy * dy)
        if length != 0:
            self.knockback_direction.x = dx / length
            self.knockback_direction.y = dy / length

        self.is_knocked_back = True
        self.knockback_timer = self.knockback_duration

    def update(self, delta_time, player):
        self.update_flash(delta_time)
        # Mise à jour de l'animation
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.frames)
            self.image = self.frames[self.animation_frame]

        # Gérer le recul
        if self.is_knocked_back:
            self.knockback_timer -= delta_time
            if self.knockback_timer <= 0:
                self.is_knocked_back = False
            else:
                # Appliquer le mouvement de recul
                knockback_speed = self.knockback_distance * (self.knockback_timer / self.knockback_duration)
                self.hitbox.x += self.knockback_direction.x * knockback_speed * delta_time
                self.hitbox.y += self.knockback_direction.y * knockback_speed * delta_time
                self.rect.center = self.hitbox.center
                return None

        # Comportement normal si pas en recul
        distance_to_player = math.sqrt(
            (player.hitbox.centerx - self.hitbox.centerx) ** 2 +
            (player.hitbox.centery - self.hitbox.centery) ** 2
        )

        if distance_to_player <= self.detection_range and not self.is_knocked_back:
            self.is_chasing = True

            # Calculer la direction vers le joueur
            dx = player.hitbox.centerx - self.hitbox.centerx
            dy = player.hitbox.centery - self.hitbox.centery

            # Normaliser le vecteur de direction
            length = math.sqrt(dx ** 2 + dy ** 2)
            if length != 0:
                dx = dx / length
                dy = dy / length

            # Déplacer l'ennemi
            self.hitbox.x += dx * self.speed * delta_time
            self.hitbox.y += dy * self.speed * delta_time
            self.rect.center = self.hitbox.center

            # Vérifier les collisions et gérer les dégâts
            if self.hitbox.colliderect(player.hitbox):
                current_time = pygame.time.get_ticks()
                if current_time - self.last_damage_time >= self.damage_cooldown:
                    player.current_lives -= 1
                    self.last_damage_time = current_time
                    # Appliquer le recul après avoir infligé des dégâts
                    self.apply_knockback((player.hitbox.centerx, player.hitbox.centery))

                    if player.current_lives <= 0:
                        return "game_over"

        return None