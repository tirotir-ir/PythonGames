import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sounds
car_sound = pygame.mixer.Sound("car_engine.wav")
car_sound.set_volume(0.5)
collision_sound = pygame.mixer.Sound("collision.wav")  # optional

# Window setup
WIDTH, HEIGHT = 400, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Car Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
emoji_font = pygame.font.SysFont(None, 60)
score_font = pygame.font.SysFont(None, 30)
message_font = pygame.font.SysFont(None, 50)

# Game variables
player_speed = 5
obstacle_size = 50
obstacle_speed = 5
spawn_rate = 30

# Road lines setup
line_width = 10
line_height = 50
line_gap = 30
road_lines = [y for y in range(0, HEIGHT, line_height + line_gap)]

# ------------------- Functions -------------------
def draw_player(x, y):
    player_text = emoji_font.render("🚗", True, BLACK)
    window.blit(player_text, (x, y))

def draw_obstacle(x, y):
    obs_text = emoji_font.render("⚠️", True, RED)
    window.blit(obs_text, (x, y))

def draw_road():
    for i in range(len(road_lines)):
        road_lines[i] += obstacle_speed
        if road_lines[i] > HEIGHT:
            road_lines[i] = -line_height
        pygame.draw.rect(window, WHITE, (WIDTH//2 - line_width//2, road_lines[i], line_width, line_height))

def show_message(text, y):
    msg = message_font.render(text, True, BLACK)
    rect = msg.get_rect(center=(WIDTH//2, y))
    window.blit(msg, rect)

# ------------------- Main Game Loop -------------------
def game_loop():
    global road_lines
    player_x = WIDTH // 2
    player_y = HEIGHT - 100
    obstacles = []
    frame_count = 0
    score = 0
    running = True

    while running:
        window.fill(GRAY)
        draw_road()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
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

        # Engine sound
        if moving:
            if not pygame.mixer.get_busy():
                car_sound.play(-1)
        else:
            car_sound.stop()

        # Spawn obstacles
        frame_count += 1
        if frame_count % spawn_rate == 0:
            obs_x = random.randint(0, WIDTH - obstacle_size)
            obs_y = -obstacle_size
            obstacles.append([obs_x, obs_y])

        # Move obstacles
        for obs in obstacles:
            obs[1] += obstacle_speed
            draw_obstacle(obs[0], obs[1])

        # Draw player
        draw_player(player_x, player_y)

        # Collision detection
        for obs in obstacles:
            if (player_x < obs[0] + obstacle_size and
                player_x + 50 > obs[0] and
                player_y < obs[1] + obstacle_size and
                player_y + 50 > obs[1]):
                car_sound.stop()
                # Optional collision sound
                # collision_sound.play()
                return score

        # Update score
        score += 1
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        window.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# ------------------- Start Screen -------------------
def start_screen():
    waiting = True
    while waiting:
        window.fill(WHITE)
        show_message("🚗 Mini Car Game 🚗", HEIGHT//3)
        show_message("Press ENTER to Start", HEIGHT//2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# ------------------- Game Over Screen -------------------
def game_over_screen(score):
    waiting = True
    while waiting:
        window.fill(WHITE)
        show_message("Game Over!", HEIGHT//3)
        show_message(f"Score: {score}", HEIGHT//2)
        show_message("Press ENTER to Restart", HEIGHT*2//3)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# ------------------- Run the Game -------------------
while True:
    start_screen()
    final_score = game_loop()
    game_over_screen(final_score)
