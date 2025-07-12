import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 1

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.speed = PLAYER_SPEED
        
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            
    def draw(self, screen):
        # Draw a simple retro spaceship
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        # Add some detail
        pygame.draw.polygon(screen, WHITE, [
            (self.x + self.width//2, self.y),
            (self.x + 10, self.y + self.height),
            (self.x + self.width - 10, self.y + self.height)
        ])

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.speed = BULLET_SPEED
        
    def update(self):
        self.y -= self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
        
    def is_off_screen(self):
        return self.y < 0

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = ENEMY_SPEED
        
    def update(self):
        self.y += self.speed
        
    def draw(self, screen):
        # Draw a simple retro enemy
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # Add some retro details
        pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + 5, 10, 10))
        pygame.draw.rect(screen, WHITE, (self.x + 25, self.y + 5, 10, 10))
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Space Shooter")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50)
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
        # Enemy spawn timer
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60  # frames
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Shoot bullet
                    bullet_x = self.player.x + self.player.width // 2 - 2
                    bullet_y = self.player.y
                    self.bullets.append(Bullet(bullet_x, bullet_y))
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
            
        return True
    
    def update(self):
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            enemy_x = random.randint(0, SCREEN_WIDTH - 40)
            self.enemies.append(Enemy(enemy_x, -30))
            self.enemy_spawn_timer = 0
        
        # Check collisions
        self.check_collisions()
    
    def check_collisions(self):
        # Bullet-enemy collisions
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.player.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw instructions
        instructions = [
            "Arrow Keys / A,D: Move",
            "Space: Shoot"
        ]
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 24).render(instruction, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 60 + i * 25))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
