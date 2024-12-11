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
        self.speed = random.uniform(500, 1000)
        if self.direction == 1:
            self.x = -self.radius
        else:
            self.x = pygame.display.get_surface().get_width() + self.radius
        self.active = True

    def move(self, delta_time):
        self.x += self.speed * self.direction * delta_time
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
        self.game_time = 20  # Durée du jeu en secondes
        self.background = pygame.image.load('assets/images/shooter_bg.png')  # Charger l'image de fond
        self.background = pygame.transform.scale(self.background, self.frame.get_size())  # Redimensionner l'image de fond
        self.clock = pygame.time.Clock()

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
                    self.hits += 1
                    target.active = False

    def update(self, delta_time):
        if pygame.time.get_ticks() - self.start_time > self.game_time * 1000:
            self.running = False
            self.end_game()
        if len(self.targets) < 5:
            self.targets.append(Target())
        for target in self.targets:
            target.move(delta_time)
        self.targets = [target for target in self.targets if target.active]
        if self.shots > 0:
            self.accuracy = (self.hits / self.shots) * 100

    def draw(self):
        self.frame.blit(self.background, (0, 0))  # Dessiner l'image de fond redimensionnée
        for target in self.targets:
            target.draw(self.frame)
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        accuracy_text = self.font.render(f'Accuracy: {self.accuracy:.2f}%', True, (255, 255, 255))
        time_left = self.game_time - (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = self.font.render(f'Time Left: {time_left}s', True, (255, 255, 255))
        self.frame.blit(score_text, (10, 10))
        self.frame.blit(accuracy_text, (10, 50))
        self.frame.blit(time_text, (10, 90))

    def end_game(self):
        print(f"Score: {self.score}")
        print(f"Shots: {self.accuracy}")
        if self.accuracy < 1 or self.score < 10:  # Condition de défaite
            print("Défaite! Votre précision est inférieure à 50% ou votre score est insuffisant.")
        else:  # Condition de victoire
            print("Victoire! Vous avez gagné.")
            self.player.points += 1
            self.player.money += int(self.accuracy * 10)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # Temps écoulé en secondes
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(delta_time)
            self.draw()
            pygame.display.flip()