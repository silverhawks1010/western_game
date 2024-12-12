import pygame
from src.entities.projectile import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, character_index, position, collision_layer):
        super().__init__()

        # Chemins des sprites basés sur l'index du personnage
        character_sprites = {
            0: {  # Bleu
                'idle': 'assets/images/sprite/mainchara/BLEU_idle.png',
                'walk': 'assets/images/sprite/mainchara/BLEU_walk.png'
            },
            1: {  # Orange
                'idle': 'assets/images/sprite/mainchara/ORANGE_idle.png',
                'walk': 'assets/images/sprite/mainchara/ORANGE_walk.png'
            },
            2: {  # Western (original)
                'idle': 'assets/images/sprite/mainchara/western_idle.png',
                'walk': 'assets/images/sprite/mainchara/western_walk.png'
            }
        }

        # Chargement des sprites du personnage sélectionné
        self.idle_sprite_sheet = pygame.image.load(character_sprites[character_index]['idle']).convert_alpha()
        self.walk_sprite_sheet = pygame.image.load(character_sprites[character_index]['walk']).convert_alpha()

        # Chargement des images d'animation
        self.idle_images = self.load_idle_images()
        self.walk_images = self.load_walk_images()

        # Initialisation de l'image et du rectangle
        self.image = self.idle_images['down'][0]
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.Vector2(position)

        self.hitbox = pygame.Rect(0, 0, 20, 20)
        self.hitbox.center = self.rect.center

        # Variables de mouvement et d'animation
        self.speed = 50
        self.idle = True
        self.direction = 'down'
        self.idle_index = 0
        self.idle_timer = 0
        self.walk_index = 0
        self.walk_timer = 0
        self.animation_speed = 0.2  # En secondes par frame

        # Couche de collision
        self.collision_layer = collision_layer

        # Gestion des tirs
        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.shot_cooldown = 800
        self.collision_layer = collision_layer
        self.ammo_in_magazine = 6  # Munitions dans le chargeur
        self.max_magazine = 6  # Taille du chargeur
        self.total_ammo = 12  # Munitions totales
        self.is_reloading = False
        self.reload_time = 6000  # 10 secondes en millisecondes
        self.reload_start = 0
        self.shot_cooldown = 800

        # Points et argent
        self.points = 0
        self.money = 0

        # Chargement des sprites des balles et des sons
        self.bullet_sprites = None  # Initialiser l'attribut
        self.load_bullet_sprites()  # Appeler la méthode pour charger les sprites

        try:
            self.reload_sound = pygame.mixer.Sound('assets/sounds/revolver_reload.mp3')
            self.reload_sound.set_volume(0.1)
            print("Reload sound loaded successfully")
        except Exception as e:
            print(f"Error loading reload sound: {e}")
            self.reload_sound = None

        # Sounds
        self.shot_sound = self.load_shot_sound()

    def load_bullet_sprites(self):
        try:
            self.ammo_icon = pygame.image.load('assets/images/map/balle/balleGAUCHE.png').convert_alpha()
            self.ammo_icon = pygame.transform.scale(self.ammo_icon, (20, 20))  # Ajuster la taille selon besoin
        except Exception as e:
            print(f"Error loading ammo icon: {e}")
            self.ammo_icon = None

        try:
            self.bullet_sprites = {
                'up': pygame.image.load('assets/images/map/balle/balleHAUT.png').convert_alpha(),
                'down': pygame.image.load('assets/images/map/balle/balleBAS.png').convert_alpha(),
                'left': pygame.image.load('assets/images/map/balle/balleGAUCHE.png').convert_alpha(),
                'right': pygame.image.load('assets/images/map/balle/balleDROITE.png').convert_alpha()
            }
        except Exception as e:
            print(f"Error loading bullet sprites: {e}")
            self.bullet_sprites = {'up': None, 'down': None, 'left': None, 'right': None}

        # Chargement du son de tir
        try:
            self.shot_sound = pygame.mixer.Sound('assets/sounds/gunshot1.wav')
            self.shot_sound.set_volume(0.1)
            print("Shot sound loaded successfully")
        except Exception as e:
            print(f"Error loading shot sound: {e}")
            return None

    def load_shot_sound(self):
        try:
            shot_sound = pygame.mixer.Sound('assets/sounds/gunshot1.wav')
            shot_sound.set_volume(0.1)
            return shot_sound
        except Exception as e:
            print(f"Error loading shot sound: {e}")
            return None

    def load_idle_images(self):
        return self.load_images_from_sheet(self.idle_sprite_sheet)

    def load_walk_images(self):
        return self.load_images_from_sheet(self.walk_sprite_sheet)

    def load_images_from_sheet(self, sprite_sheet):
        directions = ['down', 'right', 'left', 'up']
        images = {direction: [] for direction in directions}
        frame_width = sprite_sheet.get_width() // 4
        frame_height = sprite_sheet.get_height() // 4

        for direction, row in zip(directions, range(4)):
            for i in range(4):
                frame = sprite_sheet.subsurface(
                    pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (frame_width * 1.5, frame_height * 1.5))
                images[direction].append(frame)

        return images

    def handle_animation(self, delta_time):
        if self.idle:
            self.update_idle_animation(delta_time)
        else:
            self.update_walk_animation(delta_time)

    def handle_shooting(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.shoot()

    def check_collisions(self, rect):
        for obj in self.collision_layer:
            if obj.name == 'Collisions' and rect.colliderect(pygame.Rect(obj.x, obj.y, obj.width, obj.height)):
                return True
        return False

    def shoot(self):
        current_time = pygame.time.get_ticks()

        # Vérifier le rechargement
        if self.is_reloading:
            if current_time - self.reload_start >= self.reload_time:
                self.ammo_in_magazine = min(self.max_magazine, self.total_ammo)
                self.total_ammo -= self.ammo_in_magazine
                self.is_reloading = False
            else:
                return  # Ne pas tirer pendant le rechargement

        # Vérifier s'il reste des munitions
        if self.ammo_in_magazine <= 0:
            # Recharger si on a encore des munitions totales
            if self.total_ammo > 0 and not self.is_reloading:
                self.is_reloading = True
                self.reload_start = current_time
                if self.reload_sound:
                    self.reload_sound.play()
            return

        if current_time - self.last_shot > self.shot_cooldown:
            screen = pygame.display.get_surface()
            screen_center = (screen.get_width() // 2, screen.get_height() // 2)

            if self.bullet_sprites[self.direction]:
                if self.shot_sound:
                    self.shot_sound.play()

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
                self.ammo_in_magazine -= 1

                # Recharger automatiquement si le chargeur est vide
                if self.ammo_in_magazine == 0 and self.total_ammo > 0:
                    self.is_reloading = True
                    self.reload_start = current_time
                    if self.reload_sound:
                        self.reload_sound.play()

    def load_idle_images(self):
        idle_images = {'down': [], 'right': [], 'left': [], 'up': []}
        frame_width = self.idle_sprite_sheet.get_width() // 4
        frame_height = self.idle_sprite_sheet.get_height() // 4
        for direction, row in zip(idle_images.keys(), range(4)):
            for i in range(4):
                frame = self.idle_sprite_sheet.subsurface(
                    pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (frame_width * 1.5, frame_height * 1.5))
                idle_images[direction].append(frame)
        return idle_images

    def load_walk_images(self):
        walk_images = {'down': [], 'right': [], 'left': [], 'up': []}
        frame_width = self.walk_sprite_sheet.get_width() // 4
        frame_height = self.walk_sprite_sheet.get_height() // 4
        for direction, row in zip(walk_images.keys(), range(4)):
            for i in range(4):
                frame = self.walk_sprite_sheet.subsurface(
                    pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (frame_width * 1.5, frame_height * 1.5))
                walk_images[direction].append(frame)
        return walk_images

    def update(self, delta_time, npcs=None):
        self.handle_movement(delta_time)
        self.handle_animation(delta_time)
        self.handle_shooting()
        self.update_bullets(delta_time, npcs)
        self.hitbox.center = self.rect.center

    def handle_movement(self, delta_time):
        keys = pygame.key.get_pressed()
        new_position = self.position.copy()
        self.idle = True

        if keys[pygame.K_LSHIFT]:
            self.speed = 100
            self.animation_speed = 0.1
        else:
            self.speed = 50
            self.animation_speed = 0.3

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            new_position.x -= self.speed * delta_time
            self.direction = 'left'
            self.idle = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_position.x += self.speed * delta_time
            self.direction = 'right'
            self.idle = False
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            new_position.y -= self.speed * delta_time
            self.direction = 'up'
            self.idle = False
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_position.y += self.speed * delta_time
            self.direction = 'down'
            self.idle = False

        new_rect = self.hitbox.copy()
        new_rect.center = new_position
        if not self.check_collisions(new_rect):
            self.position = new_position
            self.rect.center = self.position

    def update_idle_animation(self, delta_time):
        self.idle_timer += delta_time
        if self.idle_timer >= self.animation_speed:
            self.idle_timer = 0
            self.idle_index = (self.idle_index + 1) % len(self.idle_images[self.direction])
            self.image = self.idle_images[self.direction][self.idle_index]

    def update_walk_animation(self, delta_time):
        self.walk_timer += delta_time
        if self.walk_timer >= self.animation_speed:
            self.walk_timer = 0
            self.walk_index = (self.walk_index + 1) % len(self.walk_images[self.direction])
            self.image = self.walk_images[self.direction][self.walk_index]

    def update_bullets(self, delta_time, npcs):
        self.bullets.update(delta_time)
        for bullet in list(self.bullets):
            # Vérifier si la balle sort de l'écran
            if not pygame.display.get_surface().get_rect().colliderect(bullet.rect):
                bullet.kill()

            # Vérifier les collisions avec les NPCs
            if npcs:
                npc_hit = pygame.sprite.spritecollideany(bullet, npcs)
                if npc_hit:
                    bullet.kill()
                    npc_hit.kill()
                    self.points += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        self.bullets.draw(surface)