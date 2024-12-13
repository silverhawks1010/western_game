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
        self.dev_mode = False
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

        # Combat tracking
        self.total_npcs_to_defeat = 3
        self.defeated_npcs = 0
        self.cross_image = pygame.transform.scale(
            pygame.image.load('assets/images/red_cross.png'),
            (30, 30)
        )

    def draw_defeated_npc_tracker(self):
        # Position for the first cross (bottom right corner)
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Calculate starting position for crosses
        cross_spacing = 40  # Space between crosses
        start_x = screen_width - (self.total_npcs_to_defeat * cross_spacing) - 20
        base_y = screen_height - 50

        # Draw placeholder crosses (grayed out)
        for i in range(self.total_npcs_to_defeat):
            pos_x = start_x + (i * cross_spacing)
            if i < self.defeated_npcs:
                # Draw red cross for defeated NPCs
                self.screen.blit(self.cross_image, (pos_x, base_y))
            else:
                # Draw grayed out cross for remaining NPCs
                grayed_cross = self.cross_image.copy()
                grayed_cross.fill((100, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(grayed_cross, (pos_x, base_y))

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

        npc2 = NPC(
            position=(1268, 577),
            image_path='assets/images/sprite/npc/CowBoyIdle.png',
            message="Prepare for battle!",
            interaction_type='combat'
        )
        self.npcs.add(npc2)
        self.group.add(npc2)

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

        combat = Combat(self.screen, self.player, npc, combat_number=self.player.combat_number)
        combat.run()

        # Vérifier le résultat du combat
        if combat.score >= 800 and combat.accuracy >= 0.5:  # 50% de précision
            self.player.combat_number += 1
            self.defeated_npcs += 1
            self.remove_npc(npc)  # Supprimer le NPC seulement en cas de victoire

            # Vérifier si le jeu est gagné
            if self.defeated_npcs >= self.total_npcs_to_defeat:
                self.game_won()
        else:
            # Le joueur perd une vie en cas de défaite
            self.player.current_lives -= 1
            if self.player.current_lives <= 0:
                self.game_over()

        self.bg_channel.stop()
        self.bg_channel.play(self.explo_sound, loops=-1)

    def draw_lives(self):
        heart_spacing = 40
        base_y = self.screen.get_height() - 50

        for i in range(self.player.max_lives):
            pos_x = 20 + (i * heart_spacing)
            if i < self.player.current_lives:
                # Cœur plein
                self.screen.blit(self.player.heart_image, (pos_x, base_y))
            else:
                # Cœur vide (grisé)
                grayed_heart = self.player.heart_image.copy()
                grayed_heart.fill((100, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(grayed_heart, (pos_x, base_y))

    def game_over(self):
        game_over_font = pygame.font.SysFont('Arial', 72)
        game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
        retry_font = pygame.font.SysFont('Arial', 36)
        retry_text = retry_font.render('Press SPACE to retry or ESC to quit', True, (255, 255, 255))

        text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2,
                                                    self.screen.get_height() // 2))
        retry_rect = retry_text.get_rect(center=(self.screen.get_width() // 2,
                                                 self.screen.get_height() // 2 + 80))

        # Créer l'overlay sombre
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Réinitialiser le jeu
                        self.reset_game()
                        waiting_for_input = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Dessiner l'écran de game over
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(retry_text, retry_rect)
            pygame.display.flip()

    # Ajoutez la méthode reset_game dans la classe Map
    def reset_game(self):
        # Réinitialiser les vies du joueur
        self.player.current_lives = self.player.max_lives

        # Réinitialiser le combat_number
        self.player.combat_number = 1

        # Réinitialiser les NPCs vaincus
        self.defeated_npcs = 0

        # Recréer tous les NPCs
        self.npcs.empty()
        self.spawn_npcs()

    def draw(self):
        self.group.draw(self.screen)
        self.player.bullets.draw(self.screen)

        if self.active_npc:
            self.active_npc.draw_dialog(self.screen)

        self.draw_hud()
        self.draw_defeated_npc_tracker()
        self.draw_lives()  # Ajouter l'affichage des vies

        if self.dev_mode:
            self.draw_hitboxes()
            self.draw_collision_layer()

    def game_won(self):
        victory_font = pygame.font.SysFont('Arial', 72)
        victory_text = victory_font.render('Victory!', True, (255, 215, 0))
        text_rect = victory_text.get_rect(center=(self.screen.get_width() // 2,
                                                  self.screen.get_height() // 2))

        # Afficher l'écran de victoire
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)

        self.screen.blit(overlay, (0, 0))
        self.screen.blit(victory_text, text_rect)
        pygame.display.flip()

        # Attendre quelques secondes
        pygame.time.wait(3000)

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

        # Draw ammo icons
        screen_width = self.screen.get_width()
        ammo_spacing = 25  # Espacement entre les balles

        # Afficher le texte des munitions totales
        total_ammo_text = self.hud_font.render(f"/{self.player.total_ammo}", True, (255, 255, 255))
        total_ammo_rect = total_ammo_text.get_rect(midright=(screen_width - 20, 30))
        self.screen.blit(total_ammo_text, total_ammo_rect)

        if self.player.is_reloading:
            # Calculer combien de balles doivent être affichées pendant le rechargement
            reload_progress = (pygame.time.get_ticks() - self.player.reload_start) / self.player.reload_time
            bullets_to_show = int((reload_progress * self.player.max_magazine))
            bullets_to_show = max(0, min(bullets_to_show, self.player.max_magazine))
        else:
            bullets_to_show = self.player.ammo_in_magazine

        # Dessiner les balles de droite à gauche, en commençant après le texte des munitions totales
        for i in range(self.player.max_magazine):
            bullet_x = total_ammo_rect.left - 30 - (i * ammo_spacing)  # 30 pixels de marge entre le texte et les balles
            bullet_y = 20

            if i < bullets_to_show:
                # Balle pleine
                self.screen.blit(self.player.ammo_icon, (bullet_x, bullet_y))
            else:
                # Balle vide (grisée)
                grayed_bullet = self.player.ammo_icon.copy()
                grayed_bullet.fill((100, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(grayed_bullet, (bullet_x, bullet_y))

        # Draw stars (points)
        start_x = hud_rect.x + 20
        for i in range(self.player.points):
            star_x = start_x + i * (self.star_image.get_width() + 5)
            self.screen.blit(self.star_image, (star_x, hud_rect.y + 60))


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