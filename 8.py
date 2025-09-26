import pygame, sys, random, os
pygame.init(); pygame.mixer.init()

W, H = 400, 600
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ultimate Arcade Car – Minimal (assets/)")
clock = pygame.time.Clock()
WHITE, BLACK, RED = (255,255,255), (0,0,0), (255,0,0)

ASSETS = "assets"
road = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS,"road.png")).convert(), (W, H))
car  = pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSETS,"car.png")).convert_alpha(), (50,100))
obsI = pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSETS,"obstacle.png")).convert_alpha(), (50,50))
coinI= pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSETS,"coin.png")).convert_alpha(), (30,30))

engine = pygame.mixer.Sound(os.path.join(ASSETS,"car_engine.wav")); engine.set_volume(0.5)
crash  = pygame.mixer.Sound(os.path.join(ASSETS,"collision.wav"))
coinS  = pygame.mixer.Sound(os.path.join(ASSETS,"coin.wav"))
eng_ch = pygame.mixer.Channel(0)

font = pygame.font.SysFont(None, 30); big = pygame.font.SysFont(None, 50)
lanes = [W//6, W//2, 5*W//6]

def start_screen():
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Ultimate Car Game", True, BLACK), (W//2-140, H//3))
        scr.blit(big.render("Press ENTER", True, BLACK), (W//2-110, H//2))
        pygame.display.flip(); clock.tick(60)

def game_over_screen(s):
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Game Over!", True, RED), (W//2-110, H//3))
        scr.blit(big.render(f"Score: {s}", True, BLACK), (W//2-90, H//2))
        pygame.display.flip(); clock.tick(60)

def game_loop():
    lane, car_rect = 1, car.get_rect(midbottom=(lanes[1], H-20))
    obstacles, coins, frame, score, spd, spawn, scroll = [], [], 0, 0, 5, 40, 0
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]  and lane>0: lane-=1; moved=True
        if keys[pygame.K_RIGHT] and lane<2: lane+=1; moved=True
        if moved and not eng_ch.get_busy(): eng_ch.play(engine, loops=-1)
        if not moved and eng_ch.get_busy(): eng_ch.stop()

        scroll = (scroll + spd) % H
        scr.blit(road, (0, scroll-H)); scr.blit(road, (0, scroll))

        car_rect.midbottom = (lanes[lane], H-20)
        scr.blit(car, car_rect)

        frame += 1
        if frame % spawn == 0:
            r = obsI.get_rect(midtop=(random.choice(lanes), -obsI.get_height())); obstacles.append(r)
            if random.random()<0.3:
                c = coinI.get_rect(midtop=(random.choice(lanes), -coinI.get_height())); coins.append(c)

        for r in obstacles[:]:
            r.y += spd; scr.blit(obsI, r)
            if r.top > H: obstacles.remove(r)
            elif car_rect.colliderect(r): eng_ch.stop(); crash.play(); return score

        for c in coins[:]:
            c.y += spd; scr.blit(coinI, c)
            if c.top > H: coins.remove(c)
            elif car_rect.colliderect(c): score += 50; coins.remove(c); coinS.play()

        if score and score % 500 == 0: spd += 0.5
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10,10)); score += 1

        pygame.display.flip(); clock.tick(60)

while True:
    start_screen()
    s = game_loop()
    game_over_screen(s)
