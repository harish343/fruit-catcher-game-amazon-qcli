import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BASKET_WIDTH = 100  # Wider basket for easier catching
BASKET_HEIGHT = 40
FRUIT_SIZE = 30
BASKET_SPEED = 12  # Faster basket movement
FRUIT_SPEED = 3  # Slower fruit falling speed
FRUIT_SPAWN_RATE = 60  # Less frequent spawning (higher = less frequent)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

class Basket:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
        self.y = SCREEN_HEIGHT - BASKET_HEIGHT - 10
        self.width = BASKET_WIDTH
        self.height = BASKET_HEIGHT
        self.speed = BASKET_SPEED
    
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            # Prevent going off screen
            if self.x < 0:
                self.x = 0
    
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            # Prevent going off screen
            if self.x > SCREEN_WIDTH - self.width:
                self.x = SCREEN_WIDTH - self.width
    
    def draw(self, screen):
        # Draw basket as a brown rectangle with a rim
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Fruit:
    def __init__(self):
        self.x = random.randint(FRUIT_SIZE, SCREEN_WIDTH - FRUIT_SIZE)
        self.y = -FRUIT_SIZE
        self.size = FRUIT_SIZE
        # Add some variation to fruit speed to make it more interesting
        self.speed = FRUIT_SPEED + random.uniform(-0.5, 0.5)
        self.color = RED  # Apple color
    
    def update(self):
        self.y += self.speed
    
    def draw(self, screen):
        # Draw apple as a red circle with a small green stem
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
        # Draw stem
        pygame.draw.rect(screen, GREEN, (self.x - 2, self.y - self.size // 2 - 5, 4, 8))
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fruit Catcher")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        self.basket = Basket()
        self.fruits = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.spawn_timer = 0
        self.difficulty_timer = 0  # For progressive difficulty
    
    def spawn_fruit(self):
        self.spawn_timer += 1
        self.difficulty_timer += 1
        
        # Progressive difficulty - spawn rate increases every 300 frames (5 seconds at 60fps)
        current_spawn_rate = max(30, FRUIT_SPAWN_RATE - (self.difficulty_timer // 300) * 5)
        
        if self.spawn_timer >= current_spawn_rate:
            self.fruits.append(Fruit())
            self.spawn_timer = 0
            # Add some randomness to spawn timing to make it less predictable
            self.spawn_timer = random.randint(-10, 10)
    
    def update_fruits(self):
        for fruit in self.fruits[:]:  # Create a copy to iterate over
            fruit.update()
            
            # Check collision with basket - make collision detection more forgiving
            basket_rect = self.basket.get_rect()
            fruit_rect = fruit.get_rect()
            
            # Expand collision area slightly for easier catching
            expanded_basket = pygame.Rect(
                basket_rect.x - 5, 
                basket_rect.y - 5, 
                basket_rect.width + 10, 
                basket_rect.height + 10
            )
            
            if fruit_rect.colliderect(expanded_basket):
                self.fruits.remove(fruit)
                self.score += 1
            
            # Check if fruit hit the ground
            elif fruit.is_off_screen():
                self.fruits.remove(fruit)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.basket.move_left()
        if keys[pygame.K_RIGHT]:
            self.basket.move_right()
    
    def draw_ui(self):
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, BLACK)
        self.screen.blit(lives_text, (10, 50))
        
        # Draw difficulty level
        difficulty_level = (self.difficulty_timer // 300) + 1
        difficulty_text = self.font.render(f"Level: {difficulty_level}", True, BLACK)
        self.screen.blit(difficulty_text, (10, 90))
        
        # Draw instructions
        if not self.game_over:
            instruction_text = self.font.render("Use LEFT/RIGHT arrows to move basket", True, BLACK)
            self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Restart instruction
        restart_text = self.font.render("Press SPACE to play again or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            running = False
            
            if not self.game_over:
                self.handle_input()
                self.spawn_fruit()
                self.update_fruits()
            
            # Draw everything
            self.screen.fill(WHITE)
            
            if not self.game_over:
                # Draw game objects
                self.basket.draw(self.screen)
                for fruit in self.fruits:
                    fruit.draw(self.screen)
            
            self.draw_ui()
            
            if self.game_over:
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
