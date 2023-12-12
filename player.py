import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < 750:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 255), (self.x, self.y, self.width, self.height))
    
    def collide_with_enemy(self, enemy):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
            pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        )

    def lose_life(self):
        self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0
