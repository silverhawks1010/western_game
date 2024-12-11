import pygame
from src.entities.projectile import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.idle_sprite_sheet = pygame.image.load('assets/images/sprite/mainchara/western_idle.png').convert_alpha()
        self.walk_sprite_sheet = pygame.image.load('assets/images/sprite/mainchara/western_walk.png').convert_alpha()
        self.idle_images = self.load_idle_images()
        self.walk_images = self.load_walk_images()
        self.image = self.idle_images['down'][0]
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.Vector2(position)
        self.speed = 10
        self.idle = True
        self.direction = 'down'
        self.idle_index = 0
        self.idle_timer = 0
        self.walk_index = 0
        self.walk_timer = 0
        self.animation_speed = 0.02
        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.shot_cooldown = 1500

        self.points = 0
        self.money = 0

        self.bullet_sprites = {
            'up': None,
            'down': None,
            'left': None,
            'right': None
        }

        try:
            self.bullet_sprites = {
                'up': pygame.image.load('assets/images/map/balle/balleHAUT.png').convert_alpha(),
                'down': pygame.image.load('assets/images/map/balle/balleBAS.png').convert_alpha(),
                'left': pygame.image.load('assets/images/map/balle/balleGAUCHE.png').convert_alpha(),
                'right': pygame.image.load('assets/images/map/balle/balleDROITE.png').convert_alpha()
            }
            print("Bullet sprites loaded successfully")
        except Exception as e:
            print(f"Error loading bullet sprites: {e}")

        try:
            self.shot_sound = pygame.mixer.Sound('assets/sounds/gunshot1.wav')
            self.shot_sound.set_volume(0.1)  # Réduire le volume à 10% (ajustez entre 0.0 et 1.0)
            print("Shot sound loaded successfully")
        except Exception as e:
            print(f"Error loading shot sound: {e}")
            self.shot_sound = None

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shot_cooldown:
            screen = pygame.display.get_surface()
            screen_center = (screen.get_width() // 2, screen.get_height() // 2)

            if self.bullet_sprites[self.direction]:
                # Jouer le son de tir s'il est chargé
                if self.shot_sound:
                    self.shot_sound.play()

                # Ajuster l'offset selon la direction
                offset = 30
                spawn_pos = list(screen_center)

                if self.direction == 'up':
                    spawn_pos[1] -= offset
                elif self.direction == 'down':
                    spawn_pos[1] += offset
                elif self.direction == 'left':
                    spawn_pos[0] -= offset
                elif self.direction == 'right':
                    spawn_pos[0] += offset

                bullet = Bullet(spawn_pos, self.direction, self.bullet_sprites[self.direction])
                self.bullets.add(bullet)
                self.last_shot = current_time

    def load_idle_images(self):
        idle_images = {'down': [], 'right': [], 'left': [], 'up': []}
        frame_width = self.idle_sprite_sheet.get_width() // 4  # Assuming 4 frames per row in the sprite sheet
        frame_height = self.idle_sprite_sheet.get_height() // 4  # Assuming 4 rows for each direction
        for direction, row in zip(idle_images.keys(), range(4)):
            for i in range(4):
                frame = self.idle_sprite_sheet.subsurface(pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))  # Scale the frame
                idle_images[direction].append(frame)
        return idle_images

    def load_walk_images(self):
        walk_images = {'down': [], 'right': [], 'left': [], 'up': []}
        frame_width = self.walk_sprite_sheet.get_width() // 4  # Assuming 4 frames per row in the sprite sheet
        frame_height = self.walk_sprite_sheet.get_height() // 4  # Assuming 4 rows for each direction
        for direction, row in zip(walk_images.keys(), range(4)):
            for i in range(4):
                frame = self.walk_sprite_sheet.subsurface(pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))  # Scale the frame
                walk_images[direction].append(frame)
        return walk_images

    def update(self, delta_time, npcs=None):
        keys = pygame.key.get_pressed()
        self.idle = True

        if keys[pygame.K_SPACE]:
            print("Space pressed")  # Debug
            self.shoot()

        if keys[pygame.K_LSHIFT]:
            self.speed = 100  # Speed in pixels per second
            self.animation_speed = 0.2  # Animation speed in seconds per frame
        else:
            self.speed = 50  # Speed in pixels per second
            self.animation_speed = 0.3  # Animation speed in seconds per frame

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.position.x -= self.speed * delta_time
            self.idle = False
            self.direction = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.position.x += self.speed * delta_time
            self.idle = False
            self.direction = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.position.y -= self.speed * delta_time
            self.idle = False
            self.direction = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.position.y += self.speed * delta_time
            self.idle = False
            self.direction = 'down'

        self.rect.topleft = self.position  # Update rect position based on the floating-point position


        if self.idle:
            self.update_idle_animation(delta_time)
        else:
            self.update_walk_animation(delta_time)

        # Ajout de la gestion du tir
        if keys[pygame.K_SPACE]:  # Tir avec la barre d'espace
            self.shoot()


        # Mise à jour des balles et détection des collisions
        for bullet in self.bullets:
            bullet.update(delta_time)
            if npcs:  # Vérification que npcs existe
                # Vérifier les collisions avec les NPCs
                for npc in npcs:
                    if bullet.rect.colliderect(npc.rect):
                        print("NPC hit!")  # Debug
                        npc.kill()  # Tuer le NPC
                        bullet.kill()  # Supprimer la balle
                        break

            # Supprimer les balles hors écran
            if not pygame.display.get_surface().get_rect().colliderect(bullet.rect):
                bullet.kill()

    def update_idle_animation(self, delta_time):
        self.idle_timer += delta_time
        if self.idle_timer >= (self.animation_speed + 0.1):  # Adjust the speed of the animation
            self.idle_timer = 0
            self.idle_index = (self.idle_index + 1) % len(self.idle_images[self.direction])
            self.image = self.idle_images[self.direction][self.idle_index]

    def update_walk_animation(self, delta_time):
        self.walk_timer += delta_time
        if self.walk_timer >= self.animation_speed:  # Adjust the speed of the animation
            self.walk_timer = 0
            self.walk_index = (self.walk_index + 1) % len(self.walk_images[self.direction])
            self.image = self.walk_images[self.direction][self.walk_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        self.bullets.draw(surface)