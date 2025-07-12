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
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
DARK_GREEN = (0, 128, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)

# IT Crowd inspired colors
TERMINAL_GREEN = (0, 255, 0)
RETRO_AMBER = (255, 191, 0)
CRT_BLUE = (0, 162, 232)
ERROR_RED = (255, 69, 0)

# Player settings
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 1

class MatrixRain:
    def __init__(self):
        self.drops = []
        for i in range(50):
            self.drops.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'speed': random.randint(2, 6),
                'char': random.choice(['0', '1', 'IT', 'PC', 'CPU', 'RAM', 'GPU'])
            })
    
    def update(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            if drop['y'] > SCREEN_HEIGHT:
                drop['y'] = random.randint(-100, -10)
                drop['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, screen):
        font = pygame.font.Font(None, 20)
        for drop in self.drops:
            text = font.render(drop['char'], True, TERMINAL_GREEN)
            screen.blit(text, (drop['x'], drop['y']))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 40
        self.speed = PLAYER_SPEED
        self.blink_timer = 0
        
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def update(self):
        self.blink_timer += 1
            
    def draw(self, screen):
        # Draw IT Crowd inspired computer/server as player
        pygame.draw.rect(screen, LIGHT_GRAY, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), 2)
        
        # Screen/monitor on top
        pygame.draw.rect(screen, BLACK, (self.x + 10, self.y - 10, 40, 15))
        
        # Blinking LED lights
        if self.blink_timer % 60 < 30:
            pygame.draw.circle(screen, TERMINAL_GREEN, (self.x + 15, self.y + 10), 3)
        if (self.blink_timer + 20) % 60 < 30:
            pygame.draw.circle(screen, ERROR_RED, (self.x + 25, self.y + 10), 3)
        if (self.blink_timer + 40) % 60 < 30:
            pygame.draw.circle(screen, CRT_BLUE, (self.x + 35, self.y + 10), 3)
        
        # "IT" text on the computer
        font = pygame.font.Font(None, 16)
        it_text = font.render("IT", True, TERMINAL_GREEN)
        screen.blit(it_text, (self.x + self.width//2 - 8, self.y + self.height//2))

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 12
        self.speed = BULLET_SPEED
        
    def update(self):
        self.y -= self.speed
        
    def draw(self, screen):
        # Draw as glowing data packet
        pygame.draw.rect(screen, RETRO_AMBER, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
        
    def is_off_screen(self):
        return self.y < 0

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 40
        self.speed = ENEMY_SPEED
        self.enemy_type = random.choice(['virus', 'bug', 'error'])
        self.animation_timer = 0
        
    def update(self):
        self.y += self.speed
        self.animation_timer += 1
        
    def draw(self, screen):
        if self.enemy_type == 'virus':
            # Draw as a corrupted file/virus
            pygame.draw.rect(screen, ERROR_RED, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, BLACK, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), 2)
            
            # Glitchy effect
            if self.animation_timer % 20 < 10:
                for i in range(5):
                    x_offset = random.randint(-2, 2)
                    y_offset = random.randint(-2, 2)
                    pygame.draw.rect(screen, MAGENTA, 
                                   (self.x + x_offset, self.y + y_offset, 
                                    random.randint(5, 15), random.randint(2, 8)))
            
            # "VIRUS" text
            font = pygame.font.Font(None, 12)
            virus_text = font.render("VIRUS", True, WHITE)
            screen.blit(virus_text, (self.x + 5, self.y + self.height//2 - 5))
            
        elif self.enemy_type == 'bug':
            # Draw as a software bug
            pygame.draw.rect(screen, DARK_GREEN, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, TERMINAL_GREEN, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), 2)
            
            # Bug legs/antennae
            for i in range(4):
                start_x = self.x + 10 + i * 8
                start_y = self.y + self.height
                end_x = start_x + random.randint(-3, 3)
                end_y = start_y + 8
                pygame.draw.line(screen, TERMINAL_GREEN, (start_x, start_y), (end_x, end_y), 2)
            
            # "BUG" text
            font = pygame.font.Font(None, 12)
            bug_text = font.render("BUG", True, WHITE)
            screen.blit(bug_text, (self.x + 10, self.y + self.height//2 - 5))
            
        else:  # error
            # Draw as a system error
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x + 2, self.y + 2, self.width - 4, self.height - 4))
            pygame.draw.rect(screen, BLUE, (self.x + 4, self.y + 4, self.width - 8, self.height - 8))
            
            # Blinking X
            if self.animation_timer % 40 < 20:
                pygame.draw.line(screen, WHITE, (self.x + 15, self.y + 10), (self.x + 35, self.y + 30), 3)
                pygame.draw.line(screen, WHITE, (self.x + 35, self.y + 10), (self.x + 15, self.y + 30), 3)
            
            # "ERROR" text
            font = pygame.font.Font(None, 10)
            error_text = font.render("ERROR", True, WHITE)
            screen.blit(error_text, (self.x + 8, self.y + self.height - 12))
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.max_timer = 30
        self.particles = []
        
        # Create particles
        for _ in range(15):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.randint(-5, 5),
                'vy': random.randint(-5, 5),
                'color': random.choice([RETRO_AMBER, WHITE, YELLOW, ORANGE])
            })
    
    def update(self):
        self.timer += 1
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # gravity
    
    def draw(self, screen):
        alpha = 1 - (self.timer / self.max_timer)
        for particle in self.particles:
            size = max(1, int(5 * alpha))
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), size)
    
    def is_finished(self):
        return self.timer >= self.max_timer

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("IT Crowd: Debug the System!")
        self.clock = pygame.time.Clock()
        
        # Background effect
        self.matrix_rain = MatrixRain()
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT - 60)
        self.bullets = []
        self.enemies = []
        self.explosions = []
        self.score = 0
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Enemy spawn timer
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 80
        
        # Screen effects
        self.screen_shake = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_x = self.player.x + self.player.width // 2 - 3
                    bullet_y = self.player.y
                    self.bullets.append(Bullet(bullet_x, bullet_y))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
            
        return True
    
    def update(self):
        self.matrix_rain.update()
        self.player.update()
        
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
        
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            enemy_x = random.randint(0, SCREEN_WIDTH - 50)
            self.enemies.append(Enemy(enemy_x, -40))
            self.enemy_spawn_timer = 0
        
        self.check_collisions()
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
    
    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    
                    # Create explosion
                    explosion_x = enemy.x + enemy.width // 2
                    explosion_y = enemy.y + enemy.height // 2
                    self.explosions.append(Explosion(explosion_x, explosion_y))
                    
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    self.screen_shake = 5
                    break
    
    def draw(self):
        # Screen shake effect
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        self.screen.fill(BLACK)
        
        # Draw matrix rain background
        self.matrix_rain.draw(self.screen)
        
        # Create a surface for the main game to apply shake effect
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_surface.fill(BLACK)
        game_surface.set_colorkey(BLACK)
        
        # Draw game objects on the game surface
        self.player.draw(game_surface)
        
        for bullet in self.bullets:
            bullet.draw(game_surface)
            
        for enemy in self.enemies:
            enemy.draw(game_surface)
        
        for explosion in self.explosions:
            explosion.draw(game_surface)
        
        # Blit the game surface with shake effect
        self.screen.blit(game_surface, (shake_x, shake_y))
        
        # Draw UI (not affected by shake)
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Draw retro-style UI border
        pygame.draw.rect(self.screen, TERMINAL_GREEN, (0, 0, SCREEN_WIDTH, 40))
        pygame.draw.rect(self.screen, BLACK, (2, 2, SCREEN_WIDTH - 4, 36))
        
        # Draw score with IT Crowd style
        score_text = self.font_medium.render(f"SYSTEM INTEGRITY: {self.score}%", True, TERMINAL_GREEN)
        self.screen.blit(score_text, (10, 12))
        
        # Draw IT Crowd inspired status messages
        status_messages = [
            "DEBUGGING IN PROGRESS...",
            "HAVE YOU TRIED TURNING IT OFF AND ON AGAIN?",
            "SYSTEM STATUS: OPERATIONAL"
        ]
        current_message = status_messages[min(2, self.score // 50)]
        status_text = self.font_small.render(current_message, True, RETRO_AMBER)
        self.screen.blit(status_text, (SCREEN_WIDTH - status_text.get_width() - 10, 15))
        
        # Draw instructions
        instructions = [
            "ARROW KEYS / A,D: NAVIGATE SYSTEM",
            "SPACE: DEPLOY ANTIVIRUS",
            "MISSION: ELIMINATE ALL BUGS & VIRUSES"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, CRT_BLUE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 70 + i * 20))
        
        # Draw retro scanlines effect
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(self.screen, (0, 50, 0), (0, y), (SCREEN_WIDTH, y))
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
