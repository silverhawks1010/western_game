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

        self.switch_map("western_map")

    def switch_map(self, map_name):
        self.tmx_data = pytmx.load_pygame(f"assets/map/{map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 3
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        map_center = (self.map_layer.map_rect.width // 2, self.map_layer.map_rect.height // 2)
        self.player = Player(map_center)
        self.group.add(self.player)

        npc1 = NPC((map_center[0] - 50, map_center[1]), 'assets/images/sprite/npc/CowBoyIdle.png', "Hello, I'm NPC 1!", interaction_type='dialog')
        npc2 = NPC((map_center[0] + 100, map_center[1]), 'assets/images/sprite/npc/CowBoyIdle.png', "Press the button quickly!", interaction_type='qte')
        npc3 = NPC((map_center[0], map_center[1] + 100), 'assets/images/sprite/npc/CowBoyIdle.png', "Prepare for battle!", interaction_type='combat')
        self.npcs.add(npc1, npc2, npc3)
        self.group.add(npc1, npc2, npc3)

    def update(self):
        self.player.update()
        self.npcs.update()
        self.handle_interactions()
        self.handle_collisions()
        self.group.update()
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

    def start_combat(self, npc):
        print("Combat: " + npc.message)
        combat = Combat(self.screen, self.player, npc)
        combat.run()
        self.current_combat = combat

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
                pygame.draw.rect(self.screen, (255, 0, 0), npc.hitbox, 2)
        if self.active_npc:
            self.active_npc.draw_dialog(self.screen)

    def toggle_hitboxes(self):
        self.show_hitboxes = not self.show_hitboxes