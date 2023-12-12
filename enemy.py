import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
        self.speed = 2  # Velocidad inicial
        self.color = (255, 0, 0)

    def update(self):
        self.y += self.speed

    def reset(self):
        self.y = 0
        self.x = random.randint(0, 750)
        self.speed += 0.1  # Aumenta la velocidad gradualmente

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))