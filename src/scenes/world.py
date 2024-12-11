# src/scenes/world.py

import pygame
import pytmx
import pyscroll
from entities.player import Player

class Map:
    def __init__(self, screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.player = None

        self.switch_map("test")

    def switch_map(self, map_name):
        self.tmx_data = pytmx.load_pygame(f"assets/map/{map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2  # Zoom level
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        # Calculate the center of the map
        map_center = (self.map_layer.map_rect.width // 2, self.map_layer.map_rect.height // 2)
        self.player = Player(map_center)
        self.group.add(self.player)

    def update(self):
        self.player.update()
        self.group.update()
        self.group.center(self.player.rect.center)

    def draw(self):
        self.group.draw(self.screen)