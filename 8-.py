import pygame
import sys
import random
import os

# -------------------- Initialization --------------------
pygame.init()
pygame.mixer.init()

# Window setup
WIDTH, HEIGHT = 400, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Arcade Car Game")

# Assets path
ASSETS = "assets"

# Load images
road_img = pygame.image.load(os.path.join(ASSETS, "road.png")).convert()
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))
car_img = pygame.image.load(os.path.join(ASSETS, "car.png")).convert_alpha()
car_img = pygame.transform.scale(car_img, (50, 100))
obstacle_img = pygame.image.load(os.path.join(ASSETS, "obstacle.png")).convert_alpha()
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))
coin_img = pygame.image.load(os.path.join(ASSETS, "coin.png")).convert_alpha()
coin_img = pygame.transform.scale(coin_img, (30, 30))

# Load sounds
car_sound = pygame.mixer.Sound(os.path.join(ASSETS, "car_engine.wav"))
car_sound.set_volume(0.5)
crash_sound = pygame.mixer.Sound(os.path.join(ASSETS, "collision.wav"))
coin_sound = pygame.mixer.Sound(os.path.join(ASSETS, "coin.wav"))

# Fonts
score_font = pygame.font.SysFont(None, 30)
message_font = pygame.font.SysFont(None, 50)

# Lanes (3 lanes)
lanes = [WIDTH//6, WIDTH//2 - 25, WIDTH*5//6 - 50]

# Game variables
player_y = HEIGHT - 150
player_speed = 1  # lane snap speed
spawn_rate = 40
initial_obstacle_speed = 5
scroll_y = 0

# -------------------- Functions --------------------
def draw_road():
    global scroll_y
    scroll_y += initial_obstacle_speed
    if scroll_y >= HEIGHT:
        scroll_y = 0
    window.blit(road_img, (0, scroll_y - HEIGHT))
    window.blit(road_img, (0, scroll_y))

def draw_player(lane):
    x = lanes[lane]
    window.blit(car_img, (x, player_y))

def draw_obstacle(obs):
    window.blit(obstacle_img, (obs[1], obs[2]))

def draw_coin(coin):
    window.blit(coin_img, (coin[1], coin[2]))

def start_screen():
    waiting = True
    while waiting:
        window.fill((255, 255, 255))
        text = message_font.render("Ultimate Car Game", True, (0,0,0))
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3))
        instr = message_font.render("Press ENTER to Start", True, (0,0,0))
        window.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def game_over_screen(score):
    waiting = True
    while waiting:
        window.fill((255, 255, 255))
        text = message_font.render("Game Over!", True, (255,0,0))
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3))
        score_text = message_font.render(f"Score: {score}", True, (0,0,0))
        window.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        instr = message_font.render("Press ENTER to Restart", True, (0,0,0))
        window.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT*2//3))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# -------------------- Main Game Loop --------------------
def game_loop():
    obstacles = []
    coins = []
    frame_count = 0
    score = 0
    obstacle_speed = initial_obstacle_speed
    running = True
    lane_pos = 1  # middle lane

    while running:
        window.fill((0,0,0))
        draw_road()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # Player lane control
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT] and lane_pos > 0:
            lane_pos -= 1
            moving = True
        if keys[pygame.K_RIGHT] and lane_pos < 2:
            lane_pos += 1
            moving = True

        # Engine sound
        if moving:
            if not pygame.mixer.get_busy():
                car_sound.play(-1)
        else:
            car_sound.stop()

        draw_player(lane_pos)

        # Spawn obstacles and coins
        frame_count += 1
        if frame_count % spawn_rate == 0:
            obs_lane = random.randint(0,2)
            obstacles.append(["obs", lanes[obs_lane], -50])
            if random.random() < 0.3:
                coin_lane = random.randint(0,2)
                coins.append(["coin", lanes[coin_lane], -50])

        # Move obstacles
        for obs in obstacles[:]:
            obs[2] += obstacle_speed
            draw_obstacle(obs)
            if obs[2] > HEIGHT:
                obstacles.remove(obs)
            if lane_pos == lanes.index(obs[1]) and player_y < obs[2]+50 and player_y+100 > obs[2]:
                car_sound.stop()
                crash_sound.play()
                return score

        # Move coins
        for coin in coins[:]:
            coin[2] += obstacle_speed
            draw_coin(coin)
            if coin[2] > HEIGHT:
                coins.remove(coin)
            if lane_pos == lanes.index(coin[1]) and player_y < coin[2]+30 and player_y+100 > coin[2]:
                score += 50
                coins.remove(coin)
                coin_sound.play()

        # Increase difficulty
        if score % 500 == 0:
            obstacle_speed += 0.5

        # Update score
        score += 1
        score_text = score_font.render(f"Score: {score}", True, (255,255,255))
        window.blit(score_text, (10,10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# -------------------- Run Game --------------------
while True:
    start_screen()
    final_score = game_loop()
    game_over_screen(final_score)
