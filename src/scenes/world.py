import os
import random
import pygame
import pytmx
import pyscroll
from entities.player import Player
from entities.npc import NPC
from scenes.combat import Combat

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

        self.selected_character = selected_character  # Ajoutez ceci
        self.switch_map("western_map")

    def switch_map(self, map_name):
        self.tmx_data = pytmx.load_pygame(f"assets/map/{map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 3
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        # Collision layer
        self.collision_layer = self.tmx_data.get_layer_by_name('Collisions')

        # Player

        self.player = Player(self.selected_character, (4000, 3000), self.collision_layer)

        foreground_layer = self.tmx_data.get_layer_by_name('Level 2')
        foreground_layer_index = self.tmx_data.layers.index(foreground_layer)
        self.group.add(self.player, layer=foreground_layer_index-1)

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

        self.group.center(self.player.hitbox.center)

    def handle_interactions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            for npc in self.npcs:
                if self.player.hitbox.colliderect(npc.rect):
                    if npc.interaction_type == 'combat':
                        self.start_combat(npc)

    def remove_npc(self, npc):
        self.npcs.remove(npc)
        self.group.remove(npc)

    def start_combat(self, npc):
        self.bg_channel.stop()
        self.bg_channel.play(self.battle_sound, loops=-1)

        combat = Combat(self.screen, self.player, npc)
        combat.run()

        self.bg_channel.stop()
        self.bg_channel.play(self.explo_sound, loops=-1)

        self.remove_npc(npc)

    def draw(self):
        self.group.draw(self.screen)
        self.player.bullets.draw(self.screen)

        # Draw NPC dialog
        if self.active_npc:
            self.active_npc.draw_dialog(self.screen)

        # Draw HUD
        self.draw_hud()

        if self.dev_mode:
            self.draw_hitboxes()
            self.draw_collision_layer()


    def draw_hud(self):
        self.screen.blit(self.hud_image, (10, 10))
        hud_rect = self.hud_image.get_rect(topleft=(10, 10))

        # Draw coins
        coin_image_rect = self.coin_image.get_rect()
        coin_image_rect.topleft = (hud_rect.x + 20, hud_rect.y + 20)
        self.screen.blit(self.coin_image, coin_image_rect.topleft)

        money_text = self.hud_font.render(f'{self.player.money}', True, (255, 255, 0))
        money_text_rect = money_text.get_rect(midleft=(coin_image_rect.right + 10, coin_image_rect.centery))
        self.screen.blit(money_text, money_text_rect)

        # Draw stars (points)
        start_x = hud_rect.x + 20
        for i in range(self.player.points):
            star_x = start_x + i * (self.star_image.get_width() + 5)
            self.screen.blit(self.star_image, (star_x, hud_rect.y + 60))

        # draw coordonnées
        coord_text = self.hud_font.render(f'{self.player.hitbox.topleft}', True, (255, 255, 0))
        coord_text_rect = coord_text.get_rect(midleft=(coin_image_rect.right + 10, coin_image_rect.centery+30))
        self.screen.blit(coord_text, coord_text_rect)

    def draw_collision_layer(self):
        for obj in self.collision_layer:
            if obj.name == 'Collisions':
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                pygame.draw.rect(self.screen, (0, 0, 255), rect, 2) # Draw the collision box in blue

    def draw_hitboxes(self):
        for npc in self.npcs:
            pygame.draw.rect(self.screen, (255, 0, 0), npc.hitbox, 2)
        pygame.draw.rect(self.screen, (0, 255, 0), self.player.hitbox, 2)

    def toggle_hitboxes(self):
        self.dev_mode = not self.dev_mode