import pygame
import sys
import random

# -------------------- Initialization --------------------
pygame.init()
pygame.mixer.init()

# Load sounds
car_sound = pygame.mixer.Sound("car_engine.wav")
car_sound.set_volume(0.5)
crash_sound = pygame.mixer.Sound("collision.wav")

# Window setup
WIDTH, HEIGHT = 400, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Car Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
emoji_font = pygame.font.SysFont(None, 60)
score_font = pygame.font.SysFont(None, 30)
message_font = pygame.font.SysFont(None, 50)

# Lanes (3 lanes)
lanes = [WIDTH//6, WIDTH//2 - 25, WIDTH*5//6 - 50]

# Game variables
player_speed = 10  # Snap to lane
obstacle_size = 50
spawn_rate = 30
initial_obstacle_speed = 5

# -------------------- Functions --------------------
def draw_player(x, y):
    player_text = emoji_font.render("🚗", True, BLACK)
    window.blit(player_text, (x, y))

def draw_obstacle(obs_type, x, y):
    obs_text = emoji_font.render(obs_type, True, RED)
    window.blit(obs_text, (x, y))

def show_message(text, y):
    msg = message_font.render(text, True, BLACK)
    rect = msg.get_rect(center=(WIDTH//2, y))
    window.blit(msg, rect)

def start_screen():
    waiting = True
    while waiting:
        window.fill(WHITE)
        show_message("🚗 Arcade Car Game 🚗", HEIGHT//3)
        show_message("Press ENTER to Start", HEIGHT//2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def game_loop():
    player_lane = 1  # start middle lane
    player_y = HEIGHT - 100
    obstacles = []
    frame_count = 0
    score = 0
    obstacle_speed = initial_obstacle_speed
    running = True

    while running:
        window.fill(GRAY)  # background road

        # Draw lanes
        lane_width = WIDTH // 3
        for i in range(1, 3):
            pygame.draw.line(window, WHITE, (i*lane_width, 0), (i*lane_width, HEIGHT), 5)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player lane control
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT] and player_lane > 0:
            player_lane -= 1
            moving = True
        if keys[pygame.K_RIGHT] and player_lane < 2:
            player_lane += 1
            moving = True

        # Engine sound
        if moving:
            if not pygame.mixer.get_busy():
                car_sound.play(-1)
        else:
            car_sound.stop()

        player_x = lanes[player_lane]
        draw_player(player_x, player_y)

        # Spawn obstacles
        frame_count += 1
        if frame_count % spawn_rate == 0:
            obs_lane = random.randint(0, 2)
            obs_type = random.choice(["⚠️", "💣", "🛑"])
            obstacles.append([obs_type, lanes[obs_lane], -obstacle_size])

        # Move obstacles
        for obs in obstacles:
            obs[2] += obstacle_speed
            draw_obstacle(obs[0], obs[1], obs[2])

        # Collision detection
        for obs in obstacles:
            if player_lane == lanes.index(obs[1]) and player_y < obs[2] + obstacle_size and player_y + 50 > obs[2]:
                car_sound.stop()
                crash_sound.play()
                return score

        # Increase difficulty over time
        if score % 200 == 0:
            obstacle_speed += 0.5

        # Update score
        score += 1
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        window.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# -------------------- Run the Game --------------------
while True:
    start_screen()
    final_score = game_loop()
    game_over_screen(final_score)
