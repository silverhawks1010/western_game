# scenes/combat.py
import pygame
import random
import math

class Target:
    def __init__(self):
        self.size_options = {
            'large': {'radius': 50, 'multiplier': 1},
            'medium': {'radius': 35, 'multiplier': 1.5},
            'small': {'radius': 20, 'multiplier': 2.5},
            'tiny': {'radius': 12, 'multiplier': 4}
        }
        self.size = random.choice(list(self.size_options.keys()))
        self.radius = self.size_options[self.size]['radius']
        self.point_multiplier = self.size_options[self.size]['multiplier']
        self.rail = random.randint(0, 2)
        self.y = 200 + (self.rail * 100)
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(2, 5)
        if self.direction == 1:
            self.x = -self.radius
        else:
            self.x = pygame.display.get_surface().get_width() + self.radius
        self.active = True

    def move(self):
        self.x += self.speed * self.direction
        if (self.x < -self.radius * 2) or (self.x > pygame.display.get_surface().get_width() + self.radius * 2):
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (101, 67, 33), (self.x - 5, self.y - self.radius, 10, self.radius * 2 + 20))
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), int(self.radius * 0.8))
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), int(self.radius * 0.6))
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), int(self.radius * 0.4))
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), int(self.radius * 0.2))

class Combat:
    def __init__(self, frame, player, pnj):
        self.frame = frame
        self.player = player
        self.pnj = pnj
        self.running = True
        self.targets = []
        self.score = 0
        self.shots = 0
        self.hits = 0
        self.accuracy = 0
        self.font = pygame.font.SysFont('Arial', 32)
        self.start_time = pygame.time.get_ticks()
        self.game_time = 60

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.shots += 1
            for target in self.targets:
                distance = math.sqrt((mouse_x - target.x)**2 + (mouse_y - target.y)**2)
                if distance < target.radius:
                    points = int(100 * target.point_multiplier * (1 - distance/target.radius))
                    self.score += points

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.draw()
            pygame.display.flip()

