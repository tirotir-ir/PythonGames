import pygame, sys, random
pygame.init(); pygame.mixer.init()

# --- Window / constants ---
W, H = 400, 600
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ultimate Arcade Car – Minimal PNG")
clock = pygame.time.Clock()
WHITE, GRAY, BLACK, RED = (255,255,255), (50,50,50), (0,0,0), (255,0,0)

# --- Assets ---
road = pygame.transform.scale(pygame.image.load("road.png").convert(), (W, H))
car  = pygame.transform.smoothscale(pygame.image.load("car.png").convert_alpha(), (50, 100))
obsI = pygame.transform.smoothscale(pygame.image.load("obstacle.png").convert_alpha(), (50, 50))
coinI= pygame.transform.smoothscale(pygame.image.load("coin.png").convert_alpha(), (30, 30))

engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)
crash  = pygame.mixer.Sound("collision.wav")
coinS  = pygame.mixer.Sound("coin.wav")
eng_ch = pygame.mixer.Channel(0)  # dedicated engine channel

font = pygame.font.SysFont(None, 30)
big  = pygame.font.SysFont(None, 50)

# Lanes (centers)
lanes = [W//6, W//2, 5*W//6]

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
    lane, y = 1, H-140
    car_rect = car.get_rect(center=(lanes[lane], y+50))
    obstacles, coins = [], []
    spawn, speed, scroll, frame, score = 40, 5, 0, 0, 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]  and lane > 0: lane -= 1; moved = True
        if keys[pygame.K_RIGHT] and lane < 2: lane += 1; moved = True

        # Engine loop while lane changing
        if moved and not eng_ch.get_busy(): eng_ch.play(engine, loops=-1)
        if not moved and eng_ch.get_busy(): eng_ch.stop()

        # Scroll road
        scroll = (scroll + speed) % H
        scr.blit(road, (0, scroll - H)); scr.blit(road, (0, scroll))

        # Car position
        car_rect.centerx = lanes[lane]
        car_rect.centery  = y + 50
        scr.blit(car, car_rect)

        # Spawn
        frame += 1
        if frame % spawn == 0:
            r = obsI.get_rect(); r.centerx = random.choice(lanes); r.y = -r.h
            obstacles.append(r)
            if random.random() < 0.3:
                c = coinI.get_rect(); c.centerx = random.choice(lanes); c.y = -c.h
                coins.append(c)

        # Move/draw obstacles
        for r in obstacles[:]:
            r.y += speed
            scr.blit(obsI, r)
            if r.top > H: obstacles.remove(r)
            elif car_rect.colliderect(r):
                eng_ch.stop(); crash.play()
                return score

        # Move/draw coins
        for c in coins[:]:
            c.y += speed
            scr.blit(coinI, c)
            if c.top > H: coins.remove(c)
            elif car_rect.colliderect(c):
                score += 50; coins.remove(c); coinS.play()

        # Difficulty ramp
        if score and score % 500 == 0: speed += 0.5

        # Score HUD
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        score += 1

        pygame.display.flip()
        clock.tick(60)

# --- Run ---
while True:
    start_screen()
    s = game_loop()
    game_over_screen(s)
