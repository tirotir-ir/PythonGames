import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load car sound
car_sound = pygame.mixer.Sound("car_engine.wav")
car_sound.set_volume(0.5)

# Set up the game window
WIDTH, HEIGHT = 400, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Car Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Player setup
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 5
font = pygame.font.SysFont(None, 60)

# Obstacles setup
obstacle_size = 50
obstacles = []
obstacle_speed = 5
spawn_rate = 30  # Frames between obstacles

# Road lines setup
line_width = 10
line_height = 50
line_gap = 30
road_lines = [y for y in range(0, HEIGHT, line_height + line_gap)]

# Game variables
score = 0
frame_count = 0
running = True

while running:
    window.fill(GRAY)  # Road background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keys pressed
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
        moving = True
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
        moving = True
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
        moving = True
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
        player_y += player_speed
        moving = True

    # Play engine sound
    if moving:
        if not pygame.mixer.get_busy():
            car_sound.play(-1)
    else:
        car_sound.stop()

    # Draw road lines
    for i in range(len(road_lines)):
        road_lines[i] += obstacle_speed
        if road_lines[i] > HEIGHT:
            road_lines[i] = -line_height
        pygame.draw.rect(window, WHITE, (WIDTH//2 - line_width//2, road_lines[i], line_width, line_height))

    # Spawn obstacles
    frame_count += 1
    if frame_count % spawn_rate == 0:
        obs_x = random.randint(0, WIDTH - obstacle_size)
        obs_y = -obstacle_size
        obstacles.append([obs_x, obs_y])

    # Move obstacles
    for obs in obstacles:
        obs[1] += obstacle_speed
        obs_text = font.render("⚠️", True, BLACK)
        window.blit(obs_text, (obs[0], obs[1]))

    # Draw player car
    player_text = font.render("🚗", True, BLACK)
    window.blit(player_text, (player_x, player_y))

    # Collision detection
    for obs in obstacles:
        if (player_x < obs[0] + obstacle_size and
            player_x + 50 > obs[0] and
            player_y < obs[1] + obstacle_size and
            player_y + 50 > obs[1]):
            print("Game Over! Score:", score)
            running = False

    # Update score
    score += 1
    score_text = pygame.font.SysFont(None, 30).render(f"Score: {score}", True, BLACK)
    window.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
