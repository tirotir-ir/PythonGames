import pygame, sys, random
pygame.init(); pygame.mixer.init()

# --- Window ---
W, H = 400, 600
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Arcade Car – PNG Lanes")
clock = pygame.time.Clock()
WHITE, GRAY, BLACK, RED = (255,255,255), (50,50,50), (0,0,0), (255,0,0)

# --- Assets ---
car = pygame.image.load("car.png").convert_alpha()
car_rect = car.get_rect(center=(W//2, H-90))
engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)
crash  = pygame.mixer.Sound("collision.wav")
ch = pygame.mixer.Channel(0)  # dedicated channel for engine

# --- Lanes & game vars ---
lane_centers = [W//6, W//2, W*5//6]
lane = 1
slide_speed = 12
obs_size, obs_speed, spawn = 50, 5, 28
obstacles, frame, score = [], 0, 0
font = pygame.font.SysFont(None, 32)
big  = pygame.font.SysFont(None, 56)

def start_screen():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Arcade Car", True, BLACK), (W//2-110, H//3))
        scr.blit(font.render("Press ENTER to start", True, BLACK), (W//2-120, H//2))
        pygame.display.flip(); clock.tick(60)

def game_over_screen(s):
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Game Over!", True, RED), (W//2-120, H//3))
        scr.blit(font.render(f"Score: {s}", True, BLACK), (W//2-50, H//2))
        scr.blit(font.render("Press ENTER to restart", True, BLACK), (W//2-140, H*2//3))
        pygame.display.flip(); clock.tick(60)

def game_loop():
    global lane, obstacles, frame, score, obs_speed
    lane, obstacles, frame, score, obs_speed = 1, [], 0, 0, 5
    car_rect.center = (lane_centers[lane], H-90)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT  and lane > 0: lane -= 1
                if e.key == pygame.K_RIGHT and lane < 2: lane += 1
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

        # Slide toward target lane center (engine plays while sliding)
        target_x = lane_centers[lane]
        dx = target_x - car_rect.centerx
        moving = abs(dx) > 1
        if moving:
            car_rect.centerx += max(-slide_speed, min(slide_speed, dx))

        if moving and not ch.get_busy(): ch.play(engine, loops=-1)
        if not moving and ch.get_busy(): ch.stop()

        # Spawn/move obstacles
        frame += 1
        if frame % spawn == 0:
            r = pygame.Rect(0, 0, obs_size, obs_size)
            r.centerx = random.choice(lane_centers)
            r.y = -obs_size
            obstacles.append(r)
        for r in obstacles: r.y += obs_speed

        # Draw
        scr.fill(GRAY)
        pygame.draw.line(scr, WHITE, (W//3, 0), (W//3, H), 5)
        pygame.draw.line(scr, WHITE, (2*W//3, 0), (2*W//3, H), 5)
        for r in obstacles:
            pygame.draw.rect(scr, BLACK, r)
            if car_rect.colliderect(r):
                ch.stop(); crash.play()
                return score

        scr.blit(car, car_rect)
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        score += 1
        if score % 240 == 0: obs_speed += 0.5  # ramp difficulty

        pygame.display.flip()
        clock.tick(60)

while True:
    start_screen()
    s = game_loop()
    game_over_screen(s)
