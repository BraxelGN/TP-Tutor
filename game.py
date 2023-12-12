import random
import pygame
from player import Player
from enemy import Enemy

class Game:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Esquivar - El juego V1")

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.player = Player(self.width // 2, self.height - 50)
        initial_enemy = Enemy(random.randint(0, 750), 50)
        self.enemies = [initial_enemy]
        self.score = 0
        self.wave_count = 0  
        self.max_enemies = 6  
        self.font = pygame.font.Font(None, 36) 
        self.game_over = False
        self.show_main_menu()
        
    def exit_game(self):
        pygame.quit()
        quit()

    def show_main_menu(self):
        menu_text = self.font.render("Presiona Enter para comenzar", True, (0, 0, 0))
        exit_text = self.font.render("Presiona Esc para Salir", True, (0, 0, 0))

        while True:
            self.screen.fill((255, 255, 255))
            self.screen.blit(menu_text, (self.width // 2 - 200, self.height // 2 - 50))
            self.screen.blit(exit_text, (self.width // 2 - 200, self.height // 2 + 80))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

            pygame.time.delay(100)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over:
                        self.reset_game()
                elif event.key == pygame.K_ESCAPE: 
                    self.exit_game()
                    
    def generate_enemy(self):
        min_distance = 150 

        while True:
            x = random.randint(0, 750)
            y = 50  

            if all(pygame.math.Vector2(x, y).distance_to(pygame.math.Vector2(enemy.x, enemy.y)) > min_distance for enemy in self.enemies):
                return Enemy(x, y)

    def update(self):
        if not self.game_over:
            self.player.update()

            for enemy in self.enemies:
                enemy.update()
                if enemy.y > self.height:
                    enemy.reset()
                    self.score += 10
                    for enemy in self.enemies:
                        enemy.speed += 0.1

            if self.score >= 10 * (self.wave_count + 1):
                self.wave_count += 1
                if len(self.enemies) < self.max_enemies:
                    new_enemy = self.generate_enemy()
                    self.enemies.append(new_enemy)

            for enemy in self.enemies:
                if self.player.collide_with_enemy(enemy):
                    self.player.lose_life()
                    if self.player.is_game_over():
                        self.game_over = True

    def draw(self):
        self.screen.fill((255, 255, 255))

        if not self.game_over:
            score_text = self.font.render(f"Puntaje: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))

            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
        else:
            self.show_game_over_screen()

        pygame.display.flip()

    def reset_game(self):
        self.player = Player(self.width // 2, self.height - 50)
        initial_enemy = Enemy(random.randint(0, 750), 50)
        self.enemies = [initial_enemy]
        self.score = 0
        self.game_over = False
    
    def show_game_over_screen(self):
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        score_text = self.font.render(f"Puntaje final: {self.score}", True, (0, 0, 0))
        restart_text = self.font.render("Presiona Enter para reiniciar", True, (0, 0, 0))
        exit_text = self.font.render("Presiona Esc para Salir", True, (0, 0, 0))

        while True:
            self.screen.fill((255, 255, 255))
            self.screen.blit(game_over_text, (self.width // 2 - 100, self.height // 2 - 50))
            self.screen.blit(score_text, (self.width // 2 - 120, self.height // 2))
            self.screen.blit(restart_text, (self.width // 2 - 180, self.height // 2 + 50))
            self.screen.blit(exit_text, (self.width // 2 - 220, self.height // 2 + 100))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reset_game()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.exit_game()
            
            pygame.time.delay(100)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

            if self.game_over:
                self.show_game_over_screen()
            

