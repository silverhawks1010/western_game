import os
import random
import pygame
import pytmx
import pyscroll
from src.entities.player import Player
from src.entities.npc import NPC
from src.scenes.combat import Combat

class Map:
    def __init__(self, screen, selected_character):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.player = None
        self.npcs = pygame.sprite.Group()
        self.dev_mode = True
        self.active_npc = None

        # Clock for delta_time
        self.clock = pygame.time.Clock()

        # Sounds
        self.explo_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "background_sound_theme_chill.mp3"))
        self.battle_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "Theme_arcade.mp3"))
        self.bg_channel = pygame.mixer.Channel(3)
        self.explo_sound.set_volume(1)
        self.battle_sound.set_volume(1)

        # HUD
        self.hud_image = pygame.transform.scale(pygame.image.load('assets/images/hud.png'), (200, 100))
        self.hud_font = pygame.font.SysFont('Arial', 24)
        self.star_image = pygame.transform.scale(pygame.image.load('assets/images/star.png'), (23, 23))
        self.coin_image = pygame.transform.scale(pygame.image.load('assets/images/coins.png'), (32, 32))

        self.selected_character = selected_character
        self.switch_map("western_map")

    def switch_map(self, map_name):
        self.tmx_data = pytmx.load_pygame(f"assets/map/{map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 3
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        # Collision layer
        self.collision_layer = self.tmx_data.get_layer_by_name('Collisions')
        # Passer le character_selected dans le constructeur
        self.player = Player(self.selected_character, (791, 721), self.collision_layer)
        self.group.add(self.player, layer=1)

        # NPCs
        self.spawn_npcs()

        # Background music
        self.bg_channel.stop()
        self.bg_channel.play(self.explo_sound, loops=-1)

    def spawn_npcs(self):
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

    def update(self):
        delta_time = self.clock.tick(60) / 1000.0

        # Player and NPC updates
        self.player.update(delta_time, self.npcs)
        self.npcs.update(delta_time)

        # Handle interactions and collisions
        self.handle_interactions()

        # Update bullets
        self.player.bullets.update(delta_time)
        for bullet in self.player.bullets:
            if not self.screen.get_rect().colliderect(bullet.rect):
                bullet.kill()

            npc_hit = pygame.sprite.spritecollideany(bullet, self.npcs)
            if npc_hit:
                bullet.kill()
                self.remove_npc(npc_hit)
                self.player.points += 1

        self.group.center(self.player.rect.center)

    def draw(self):
        self.group.draw(self.screen)
        self.player.bullets.draw(self.screen)

        # Draw NPC dialog
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

        # Draw stars for points
        total_stars_width = self.player.points * 33
        start_x = hud_rect.centerx - total_stars_width // 2.1
        for i in range(self.player.points):
            star_x = start_x + i * 33
            star_y = hud_rect.top + 60
            self.screen.blit(self.star_image, (star_x, star_y))

        # Draw ammo icons
        ammo_start_x = self.screen.get_width() - 180
        ammo_start_y = 20
        spacing = 20

        if self.player.is_reloading:
            # Calculate bullets being reloaded
            current_time = pygame.time.get_ticks()
            reload_progress = (current_time - self.player.reload_start) / self.player.reload_time
            bullets_to_reload = self.player.max_magazine - self.player.ammo_in_magazine
            bullets_reloaded = min(bullets_to_reload, int(reload_progress * bullets_to_reload))

            for i in range(self.player.max_magazine):
                icon_pos = (ammo_start_x + (i * spacing), ammo_start_y)
                if i < self.player.ammo_in_magazine:
                    # Current bullets
                    self.screen.blit(self.player.ammo_icon, icon_pos)
                elif i < self.player.ammo_in_magazine + bullets_reloaded:
                    # Reloading bullets with fade effect
                    alpha = min(255, int((reload_progress * 255)))
                    fading_icon = self.player.ammo_icon.copy()
                    fading_icon.set_alpha(alpha)
                    self.screen.blit(fading_icon, icon_pos)
                else:
                    # Empty slots
                    grey_icon = self.player.ammo_icon.copy()
                    grey_icon.fill((100, 100, 100, 128), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(grey_icon, icon_pos)
        else:
            # Normal ammo display
            for i in range(self.player.max_magazine):
                icon_pos = (ammo_start_x + (i * spacing), ammo_start_y)
                if i < self.player.ammo_in_magazine:
                    self.screen.blit(self.player.ammo_icon, icon_pos)
                else:
                    grey_icon = self.player.ammo_icon.copy()
                    grey_icon.fill((100, 100, 100, 128), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(grey_icon, icon_pos)

        # Draw total ammo
        total_ammo_text = self.hud_font.render(f"/{self.player.total_ammo}", True, (255, 255, 255))
        self.screen.blit(total_ammo_text, (ammo_start_x + (self.player.max_magazine * spacing) + 5, ammo_start_y))

        if self.dev_mode:
            self.draw_hitboxes()

    def toggle_hitboxes(self):
        self.dev_mode = not self.dev_mode