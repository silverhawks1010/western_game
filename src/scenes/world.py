import os
import random
import pygame
import pytmx
import pyscroll
from src.entities.player import Player
from src.entities.npc import NPC
from src.scenes.combat import Combat


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.player = None
        self.npcs = pygame.sprite.Group()
        self.dev_mode = True
        self.active_npc = None
        self.explo_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "background_sound_theme_chill.mp3"))
        self.battle_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "Theme_arcade.mp3"))
        self.bg_channel = pygame.mixer.Channel(3)
        self.explo_sound.set_volume(1)
        self.battle_sound.set_volume(1)
        self.font = pygame.font.SysFont('Arial', 32)
        self.clock = pygame.time.Clock()
        self.hud_image = pygame.image.load('assets/images/hud.png')
        self.hud_image = pygame.transform.scale(self.hud_image, (200, 100))  # Adjust size as needed
        self.hud_font = pygame.font.SysFont('Arial', 24)
        self.star_image = pygame.image.load('assets/images/star.png')
        self.star_image = pygame.transform.scale(self.star_image, (23, 23))
        self.coin_image = pygame.image.load('assets/images/coins.png')
        self.coin_image = pygame.transform.scale(self.coin_image, (32, 32))

        self.switch_map("western_map")

    def switch_map(self, map_name):
        self.tmx_data = pytmx.load_pygame(f"assets/map/{map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 3
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        self.collision_layer = self.tmx_data.get_layer_by_name('Collisions')
        self.player = Player((4027,1972), self.collision_layer)

        foreground_layer = self.tmx_data.get_layer_by_name('Level 2')
        foreground_layer_index = self.tmx_data.layers.index(foreground_layer)
        print(f"Foreground layer index: {foreground_layer_index}")
        self.group.add(self.player, layer=foreground_layer_index - 1)

        # Create NPCs with position as a tuple
        npc1 = NPC(
            position=(745, 583),
            image_path='assets/images/sprite/npc/CowBoyIdle.png',
            message="Prepare for battle!",
            interaction_type='combat'
        )
        self.npcs.add(npc1)
        self.group.add(npc1)
        for _ in range(5):
            npc_x = random.randint(0, self.map_layer.map_rect.width)
            npc_y = random.randint(0, self.map_layer.map_rect.height)
            npc = NPC(
                position=(npc_x, npc_y),
                image_path='assets/images/sprite/npc/CowBoyIdle.png',
                message="Prepare for battle!",
                interaction_type='combat'
            )
            self.npcs.add(npc)
            self.group.add(npc)

        self.bg_channel.stop()
        self.bg_channel.play(self.explo_sound, loops=-1)


    def update(self):
        delta_time = self.clock.tick(60) / 1000.0

        # Mise à jour du joueur avec le groupe de NPCs
        self.player.update(delta_time, self.npcs)

        # Vérifier les collisions balles-NPCs
        for bullet in self.player.bullets:
            bullet.update(delta_time)
            npc_hit = pygame.sprite.spritecollideany(bullet, self.npcs)
            if npc_hit:
                print("NPC hit by bullet!")
                bullet.kill()
                self.remove_npc(npc_hit)
                self.player.points += 1  # Ajouter des points quand un NPC est tué

        self.npcs.update(delta_time)
        self.handle_interactions()
        self.handle_collisions()
        self.group.update(delta_time)
        self.group.center(self.player.rect.center)

        # Dessiner les balles
        self.player.bullets.update(delta_time)
        # Supprimer les balles hors écran
        for bullet in self.player.bullets:
            if not self.screen.get_rect().colliderect(bullet.rect):
                bullet.kill()

    def handle_interactions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            for npc in self.npcs:
                if self.player.rect.colliderect(npc.rect):
                    if npc.interaction_type == 'dialog':
                        self.active_npc = npc
                    elif npc.interaction_type == 'qte':
                        self.start_qte(npc)
                    elif npc.interaction_type == 'combat':
                        self.start_combat(npc)
        else:
            self.active_npc = None

    def start_qte(self, npc):
        print("Quick Time Event: " + npc.message)

    def remove_npc(self, npc):
        self.npcs.remove(npc)
        self.group.remove(npc)
        print(f"NPC removed. Remaining NPCs: {len(self.npcs)}")

    def start_combat(self, npc):
        self.bg_channel.stop()
        self.bg_channel.play(self.battle_sound, loops=-1)

        print("Combat: " + npc.message)
        combat = Combat(self.screen, self.player, npc)
        combat.run()
        self.current_combat = combat

        self.bg_channel.stop()
        self.bg_channel.play(self.explo_sound, loops=-1)

        self.remove_npc(npc)

    def handle_collisions(self):
        for npc in self.npcs:
            if self.player.rect.colliderect(npc.hitbox):
                if self.player.direction == 'left':
                    self.player.position.x = npc.hitbox.right
                elif self.player.direction == 'right':
                    self.player.position.x = npc.hitbox.left - self.player.rect.width
                elif self.player.direction == 'up':
                    self.player.position.y = npc.hitbox.bottom
                elif self.player.direction == 'down':
                    self.player.position.y = npc.hitbox.top - self.player.rect.height
                self.player.rect.topleft = self.player.position


    def draw(self):
        self.group.draw(self.screen)

        # Dessiner les balles
        self.player.bullets.draw(self.screen)

        if self.active_npc:
            self.active_npc.draw_dialog(self.screen)


        self.screen.blit(self.hud_image, (10, 10))




        # Center the text within the HUD
        hud_rect = self.hud_image.get_rect(topleft=(10, 10))

        agent_text = self.hud_font.render(f'{self.player.money}', True, (255, 255, 0))
        agent_text_rect = agent_text.get_rect(center=(hud_rect.centerx, hud_rect.centery * 0.70))

        coin_image_rect = self.coin_image.get_rect()
        coin_image_rect.topleft = (hud_rect.centerx*0.25, hud_rect.centery * 0.45)
        self.screen.blit(self.coin_image, coin_image_rect.topleft)
        self.screen.blit(agent_text, agent_text_rect)

        total_stars_width = self.player.points * 33  # 30 for star width + 5 for spacing
        start_x = hud_rect.centerx - total_stars_width // 2.1
        for i in range(self.player.points):
            star_x = start_x + i * 33  # Adjust spacing as needed
            star_y = hud_rect.top + 60
            self.screen.blit(self.star_image, (star_x, star_y))

        if self.dev_mode:
            player_coords_text = self.hud_font.render(f'Coords: ({int(self.player.position.x)}, {int(self.player.position.y)})', True, (255, 255, 255))
            self.screen.blit(player_coords_text, (10, hud_rect.bottom + 10))

            # Afficher les icônes de balles
        ammo_start_x = self.screen.get_width() - 180
        ammo_start_y = 20
        spacing = 20

        if self.player.is_reloading:
            # Calculer combien de balles doivent être affichées pendant le rechargement
            current_time = pygame.time.get_ticks()
            reload_progress = (current_time - self.player.reload_start) / self.player.reload_time
            bullets_to_reload = self.player.max_magazine - self.player.ammo_in_magazine
            bullets_reloaded = min(bullets_to_reload,
                                   int(reload_progress * bullets_to_reload))

            # Afficher les balles actuelles + les balles en cours de rechargement
            for i in range(self.player.max_magazine):
                icon_pos = (ammo_start_x + (i * spacing), ammo_start_y)

                if i < self.player.ammo_in_magazine:
                    # Balles déjà dans le chargeur
                    self.screen.blit(self.player.ammo_icon, icon_pos)
                elif i < self.player.ammo_in_magazine + bullets_reloaded:
                    # Balles qui apparaissent progressivement
                    alpha = min(255, int((reload_progress * 255)))
                    fading_icon = self.player.ammo_icon.copy()
                    fading_icon.set_alpha(alpha)
                    self.screen.blit(fading_icon, icon_pos)
                else:
                    # Emplacements vides
                    grey_icon = self.player.ammo_icon.copy()
                    grey_icon.fill((100, 100, 100, 128), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(grey_icon, icon_pos)
        else:
            # Affichage normal des balles hors rechargement
            for i in range(self.player.max_magazine):
                icon_pos = (ammo_start_x + (i * spacing), ammo_start_y)
                if i < self.player.ammo_in_magazine:
                    self.screen.blit(self.player.ammo_icon, icon_pos)
                else:
                    grey_icon = self.player.ammo_icon.copy()
                    grey_icon.fill((100, 100, 100, 128), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(grey_icon, icon_pos)

        # Afficher le nombre total de munitions
        total_ammo_text = self.hud_font.render(f"/{self.player.total_ammo}", True, (255, 255, 255))
        self.screen.blit(total_ammo_text, (ammo_start_x + (self.player.max_magazine * spacing) + 5, ammo_start_y))



    def toggle_hitboxes(self):
        self.show_hitboxes = not self.show_hitboxes