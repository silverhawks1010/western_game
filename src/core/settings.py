import os

# Paramètres de la fenêtre
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Western Game"
FULLSCREEN = False

# Chemins des ressources
GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(GAME_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
MAPS_DIR = os.path.join(ASSETS_DIR, 'maps')

# Fichiers de ressources
FONT_FILE = os.path.join(FONTS_DIR, 'WesternBangBang-Regular.ttf')

# Images
TITLE_SCREEN = os.path.join(IMAGES_DIR, 'ecran_titre.jpg')
BACKGROUND_GAME = os.path.join(IMAGES_DIR, 'images.jpg')

# Maps
MAP_PATHS = {
    'town': os.path.join(MAPS_DIR, 'town.tmx'),
    'saloon': os.path.join(MAPS_DIR, 'saloon.tmx'),
    'desert': os.path.join(MAPS_DIR, 'desert.tmx'),
    'mine': os.path.join(MAPS_DIR, 'mine.tmx')
}

# Tilesets
TILESET_PATHS = {
    'terrain': os.path.join(MAPS_DIR, 'terrain_tileset.png'),
    'buildings': os.path.join(MAPS_DIR, 'buildings_tileset.png'),
    'decorations': os.path.join(MAPS_DIR, 'decorations_tileset.png')
}

# Sons
SOUND_FILES = {
    'background': 'background_sound_theme_chill.mp3',
    'level_complete': 'fin_du_niveau.mp3',
    'walk_slow': 'marche_lente.mp3',
    'walk_fast': 'marche_rapide.mp3',
    'coin': 'obtenir_piece.mp3',
    'arcade': 'Theme_arcade.mp3'
}

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Paramètres du joueur
PLAYER_SPEED = 5
PLAYER_HEALTH = 100
PLAYER_START_MONEY = 0

# Paramètres de combat
BULLET_SPEED = 10
DAMAGE_NORMAL = 25
DAMAGE_HEADSHOT = 50
SHOOTING_COOLDOWN = 500  # en millisecondes

# Paramètres des ennemis
ENEMY_SPEEDS = {
    'slow': 2,
    'normal': 3,
    'fast': 4
}
ENEMY_HEALTH = {
    'weak': 50,
    'normal': 100,
    'strong': 150
}

# Paramètres du score et de l'économie
SCORE_KILL = 100
SCORE_HEADSHOT = 150
MONEY_KILL = 50
MONEY_MISSION = 200

# États du jeu
GAME_STATES = {
    'MENU': 0,
    'PLAYING': 1,
    'PAUSED': 2,
    'SHOP': 3,
    'GAME_OVER': 4,
    'VICTORY': 5
}

# Paramètres des menus
MENU_FONT_SIZE = 48
MENU_ITEM_SPACING = 60

# Paramètres de la boutique
SHOP_ITEMS = {
    'health_potion': {'price': 100, 'effect': 50},
    'speed_boost': {'price': 150, 'duration': 10},
    'better_gun': {'price': 500, 'damage_boost': 1.5}
}

# Niveaux de difficulté
DIFFICULTY_SETTINGS = {
    'easy': {
        'enemy_damage_multiplier': 0.8,
        'enemy_speed_multiplier': 0.8,
        'player_damage_multiplier': 1.2
    },
    'normal': {
        'enemy_damage_multiplier': 1.0,
        'enemy_speed_multiplier': 1.0,
        'player_damage_multiplier': 1.0
    },
    'hard': {
        'enemy_damage_multiplier': 1.2,
        'enemy_speed_multiplier': 1.2,
        'player_damage_multiplier': 0.8
    }
}

# Taille des tuiles pour les maps
TILE_SIZE = 32

# Paramètres de débug
DEBUG = False
SHOW_HITBOX = False
SHOW_FPS = False