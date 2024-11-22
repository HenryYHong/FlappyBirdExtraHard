import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
PIPE_WIDTH = 80
PIPE_GAP_BASE = 200  # Base gap size for pipes
PIPE_GAP_VARIATION = 50  # Range for gap variation
GRAVITY = 0.8
FLAP_STRENGTH = -10

# Colors
SKY_BLUE = (135, 206, 235)
DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Game Variables
bird_x = SCREEN_WIDTH // 4
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0

# Load Bird Sprite
bird_sprite = pygame.image.load("bird.png").convert_alpha()
bird_sprite = pygame.transform.scale(bird_sprite, (40, 30))

pipes = []
pipe_frequency = 1500  # milliseconds
last_pipe_time = pygame.time.get_ticks()

# Enemies
enemies = []
enemy_frequency = 3000  # milliseconds
last_enemy_time = pygame.time.get_ticks()
enemy_size = (30, 20)

score = 0
font = pygame.font.Font(None, 36)

# Ground Texture
ground_texture_color = (160, 82, 45)
ground_texture_lines = [((x, SCREEN_HEIGHT - GROUND_HEIGHT), (x + 20, SCREEN_HEIGHT - GROUND_HEIGHT + 20)) for x in range(0, SCREEN_WIDTH, 20)]

# Cloud settings
clouds = [(random.randint(50, SCREEN_WIDTH - 50), random.randint(30, SCREEN_HEIGHT // 3)) for _ in range(5)]

# Functions to draw clouds, ground, pipes, and enemies
def draw_clouds():
    for x, y in clouds:
        pygame.draw.circle(screen, WHITE, (x, y), 20)
        pygame.draw.circle(screen, WHITE, (x + 25, y + 5), 15)
        pygame.draw.circle(screen, WHITE, (x - 25, y + 5), 15)

def create_pipe():
    pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP_BASE - GROUND_HEIGHT)
    pipe_gap = PIPE_GAP_BASE + random.randint(-PIPE_GAP_VARIATION, PIPE_GAP_VARIATION)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + pipe_gap, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - pipe_gap - GROUND_HEIGHT)
    pipes.append((top_pipe, bottom_pipe))

def draw_pipes():
    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(screen, DARK_GREEN, top_pipe)
        pygame.draw.rect(screen, DARK_GREEN, bottom_pipe)
        pygame.draw.rect(screen, BLACK, top_pipe, 3)
        pygame.draw.rect(screen, BLACK, bottom_pipe, 3)

def move_pipes():
    global pipes, score
    pipes = [(top_pipe.move(-5, 0), bottom_pipe.move(-5, 0)) for top_pipe, bottom_pipe in pipes if top_pipe.x + PIPE_WIDTH > 0]
    for top_pipe, _ in pipes:
        if top_pipe.x + PIPE_WIDTH == bird_x:
            score += 1

def create_enemy():
    enemy_y = random.randint(50, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
    enemy_rect = pygame.Rect(SCREEN_WIDTH, enemy_y, *enemy_size)
    enemies.append(enemy_rect)

def draw_enemies():
    for enemy in enemies:
        # Rocket-like body
        pygame.draw.rect(screen, RED, enemy)
        # Rocket nose (triangle pointing forward in front of the rectangle)
        pygame.draw.polygon(screen, BLACK, [
            (enemy.x - 30, enemy.y + enemy.height // 2),  # Tip of the triangle
            (enemy.x + 10, enemy.y),  # Top corner
            (enemy.x + 10, enemy.y + enemy.height)  # Bottom corner
        ])

def move_enemies():
    global enemies
    enemies = [enemy.move(-6, 0) for enemy in enemies if enemy.x + enemy_size[0] > 0]

def draw_ground():
    pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    for start_pos, end_pos in ground_texture_lines:
        pygame.draw.line(screen, ground_texture_color, start_pos, end_pos, 2)

def check_collision():
    bird_rect = pygame.Rect(bird_x, bird_y, bird_sprite.get_width(), bird_sprite.get_height())
    for top_pipe, bottom_pipe in pipes:
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True
    for enemy in enemies:
        if bird_rect.colliderect(enemy):
            return True
    if bird_y <= 0 or bird_y + bird_sprite.get_height() >= SCREEN_HEIGHT - GROUND_HEIGHT:
        return True
    return False
    
# Game loop
running = True
while running:
    screen.fill(SKY_BLUE)
    draw_clouds()
    draw_ground()

    current_time = pygame.time.get_ticks()
    if current_time - last_pipe_time > pipe_frequency:
        create_pipe()
        last_pipe_time = current_time

    if current_time - last_enemy_time > enemy_frequency:
        create_enemy()
        last_enemy_time = current_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = FLAP_STRENGTH
            elif event.key == pygame.K_p:  # Press 'P' to take a screenshot
                screenshot_filename = f"screenshot_{pygame.time.get_ticks()}.png"
                pygame.image.save(screen, screenshot_filename)
                print(f"Screenshot saved as {screenshot_filename}")

    # Bird physics
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    # Move pipes and enemies, check for collision
    move_pipes()
    move_enemies()
    if check_collision():
        print(f"Game Over! Final Score: {score}")
        running = False

    # Draw elements
    screen.blit(bird_sprite, (bird_x, bird_y))  # Draw bird sprite
    draw_pipes()
    draw_enemies()

    # Score display
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Screenshot should be captured after all elements are drawn
    if pygame.key.get_pressed()[pygame.K_p]:  # Continuous check for 'P'
        screenshot_filename = f"screenshot_{pygame.time.get_ticks()}.png"
        pygame.image.save(screen, screenshot_filename)
        print(f"Screenshot saved as {screenshot_filename}")

    pygame.time.Clock().tick(30)

pygame.quit()
