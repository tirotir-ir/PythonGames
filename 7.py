import pygame, sys, random
pygame.init(); pygame.mixer.init()

# --- Window / constants ---
W, H = 400, 600
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ultimate Arcade Car – Smooth + Size")
clock = pygame.time.Clock()
WHITE, GRAY, BLACK, RED = (255,255,255), (50,50,50), (0,0,0), (255,0,0)

# --- Assets ---
road = pygame.transform.scale(pygame.image.load("road.png").convert(), (W, H))
car_src = pygame.image.load("car.png").convert_alpha()  # unscaled; we scale by preset
obsI = pygame.transform.smoothscale(pygame.image.load("obstacle.png").convert_alpha(), (50, 50))
coinI= pygame.transform.smoothscale(pygame.image.load("coin.png").convert_alpha(), (30, 30))

engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)
crash  = pygame.mixer.Sound("collision.wav")
coinS  = pygame.mixer.Sound("coin.wav")
eng_ch = pygame.mixer.Channel(0)  # dedicated engine channel

font = pygame.font.SysFont(None, 30)
big  = pygame.font.SysFont(None, 50)

# --- Car size presets (press 1/2/3 in-game) ---
PRESETS = [(30,60), (40,80), (50,100)]  # small/medium/large
car = pygame.transform.smoothscale(car_src, PRESETS[1])  # default: medium
car_w, car_h = car.get_size()

def set_car_size(idx):
    global car, car_w, car_h
    car = pygame.transform.smoothscale(car_src, PRESETS[idx])
    car_w, car_h = car.get_size()

def start_screen():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Ultimate Car Game", True, BLACK), (W//2-140, H//3))
        scr.blit(big.render("Press ENTER", True, BLACK), (W//2-110, H//2))
        pygame.display.flip(); clock.tick(60)

def game_over_screen(score):
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Game Over!", True, RED), (W//2-110, H//3))
        scr.blit(big.render(f"Score: {score}", True, BLACK), (W//2-90, H//2))
        scr.blit(font.render("Press ENTER to restart", True, BLACK), (W//2-120, 2*H//3))
        pygame.display.flip(); clock.tick(60)

def game_loop():
    # --- Smooth steering params ---
    x = W/2 - car_w/2
    y = H - 20 - car_h
    vx = 0.0
    ACCEL = 900.0     # px/s^2 when holding left/right
    MAX_VX = 260.0    # px/s max sideways speed
    FRICTION = 0.90   # coast slowdown when no input

    obstacles, coins = [], []
    spawn, scroll_speed, scroll, frame, score = 40, 5.0, 0.0, 0, 0

    while True:
        dt = clock.tick(60) / 1000.0  # seconds per frame

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                # quick size presets: 1/2/3
                if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    old_centerx = int(x + car_w/2)
                    idx = {pygame.K_1:0, pygame.K_2:1, pygame.K_3:2}[e.key]
                    set_car_size(idx)
                    # keep the car centered at same x
                    x = max(0, min(W - car_w, old_centerx - car_w/2))

        # --- Smooth steering ---
        keys = pygame.key.get_pressed()
        ax = (-ACCEL if keys[pygame.K_LEFT] else 0) + (ACCEL if keys[pygame.K_RIGHT] else 0)
        vx += ax * dt
        vx *= FRICTION if ax == 0 else 1.0
        vx = max(-MAX_VX, min(MAX_VX, vx))
        x += vx * dt
        x = max(0, min(W - car_w, x))

        # Engine sound only when actually moving
        moving = abs(vx) > 5
        if moving and not eng_ch.get_busy(): eng_ch.play(engine, loops=-1)
        if not moving and eng_ch.get_busy(): eng_ch.stop()

        # --- World update ---
        scroll = (scroll + scroll_speed) % H
        scr.blit(road, (0, scroll - H)); scr.blit(road, (0, scroll))

        car_rect = pygame.Rect(int(x), int(y), car_w, car_h)
        scr.blit(car, car_rect)

        # Spawn
        frame += 1
        if frame % spawn == 0:
            r = obsI.get_rect()
            r.x = random.randint(0, W - r.w); r.y = -r.h
            obstacles.append(r)
            if random.random() < 0.3:
                c = coinI.get_rect()
                c.x = random.randint(0, W - c.w); c.y = -c.h
                coins.append(c)

        # Move/draw obstacles
        for r in obstacles[:]:
            r.y += scroll_speed
            scr.blit(obsI, r)
            if r.top > H: obstacles.remove(r)
            elif car_rect.colliderect(r):
                eng_ch.stop(); crash.play()
                return score

        # Move/draw coins
        for c in coins[:]:
            c.y += scroll_speed
            scr.blit(coinI, c)
            if c.top > H: coins.remove(c)
            elif car_rect.colliderect(c):
                score += 50; coins.remove(c); coinS.play()

        # Difficulty ramp
        if score and score % 500 == 0: scroll_speed += 0.5

        # HUD
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        scr.blit(font.render("Size 1/2/3  |  ←/→ steer", True, WHITE), (10, 34))
        score += 1

        pygame.display.flip()

# --- Run ---
while True:
    start_screen()
    s = game_loop()
    game_over_screen(s)
