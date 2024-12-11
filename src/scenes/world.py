import os
import random

import pygame
import pytmx
import pyscroll
from entities.player import Player
from entities.npc import NPC
from scenes.combat import Combat

class Map:
    def __init__(self, screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.player = None
        self.npcs = pygame.sprite.Group()
        self.show_hitboxes = True
        self.active_npc = None  # Track the active NPC for dialog
        self.explo_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "background_sound_theme_chill.mp3"))
        self.battle_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "Theme_arcade.mp3"))
        self.bg_channel = pygame.mixer.Channel(0)
        self.explo_sound.set_volume(0.08)
        self.battle_sound.set_volume(0.08)
        self.font = pygame.font.SysFont('Arial', 32)  # Charger la police pour afficher le texte
        self.clock = pygame.time.Clock()  # Ajouter un horloge pour calculer delta_time

        self.switch_map("western_map")

    # src/scenes/world.py

    def switch_map(self, map_name):
        self.tmx_data = pytmx.load_pygame(f"assets/map/{map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 3
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        map_center = (self.map_layer.map_rect.width // 2, self.map_layer.map_rect.height // 2)
        self.player = Player(map_center)
        self.group.add(self.player)

        for _ in range(5):
            x = random.randint(0, self.map_layer.map_rect.width)
            y = random.randint(0, self.map_layer.map_rect.height)
            npc = NPC((x, y), 'assets/images/sprite/npc/CowBoyIdle.png', "Prepare for battle!",
                      interaction_type='combat')
            self.npcs.add(npc)
            self.group.add(npc)

        # Arrêter la musique actuelle et jouer la nouvelle musique de fond
        self.bg_channel.stop()
        self.bg_channel.play(self.explo_sound, loops=-1)

    def update(self):
        delta_time = self.clock.tick(60) / 1000.0  # Temps écoulé en secondes
        self.player.update(delta_time)
        self.npcs.update(delta_time)
        self.handle_interactions()
        self.handle_collisions()
        self.group.update(delta_time)
        self.group.center(self.player.rect.center)

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

    def start_combat(self, npc):
        print("Combat: " + npc.message)
        combat = Combat(self.screen, self.player, npc)
        combat.run()
        self.current_combat = combat
        self.bg_channel.stop()
        self.bg_channel.play(self.battle_sound, loops=-1)
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
        if self.show_hitboxes:
            for npc in self.npcs:
                # Code pour dessiner les hitboxes
                pass
        if self.active_npc:
            self.active_npc.draw_dialog(self.screen)

        # Afficher l'argent du joueur
        money_text = self.font.render(f'Argent: {self.player.money}', True, (255, 255, 255))
        score_text = self.font.render(f'Score: {self.player.points}/5', True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(score_text, (10, 50))

    def toggle_hitboxes(self):
        self.show_hitboxes = not self.show_hitboxes