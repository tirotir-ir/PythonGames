import pygame, sys, random
pygame.init(); pygame.mixer.init()

W, H = 400, 600
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mini Car – PNG")
clock = pygame.time.Clock()
WHITE, GRAY, BLACK, RED = (255,255,255), (50,50,50), (0,0,0), (255,0,0)
BLUE = (53, 55, 135)
car = pygame.image.load("car.png").convert_alpha()
car_rect = car.get_rect(center=(W//2, H-100))
car_speed = 5

engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)

obs_size, obs_speed, spawn = 50, 5, 30
line_w, line_h, gap, offset = 10, 50, 30, 0
font_big = pygame.font.SysFont(None, 48)
font = pygame.font.SysFont(None, 28)

def start_screen():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(font_big.render("Mini Car Game", True, BLACK), (W//2-120, H//3))
        scr.blit(font.render("Press ENTER to start", True, BLACK), (W//2-110, H//2))
        pygame.display.flip(); clock.tick(60)

def game_loop():
    global offset
    obstacles, frame, score = [], 0, 0
    car_rect.center = (W//2, H-100)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        keys = pygame.key.get_pressed()
        moving = False
        car_rect.x += (keys[pygame.K_RIGHT]-keys[pygame.K_LEFT]) * car_speed; moving |= keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]
        car_rect.y += (keys[pygame.K_DOWN]-keys[pygame.K_UP])   * car_speed; moving |= keys[pygame.K_DOWN]  or keys[pygame.K_UP]
        car_rect.clamp_ip(scr.get_rect())

        if moving and not pygame.mixer.get_busy(): engine.play(-1)
        if not moving and pygame.mixer.get_busy(): engine.stop()

        frame += 1
        if frame % spawn == 0:
            obstacles.append(pygame.Rect(random.randint(0, W-obs_size), -obs_size, obs_size, obs_size))
        for r in obstacles: r.y += obs_speed

        offset = (offset + obs_speed) % (line_h + gap)

        scr.fill(GRAY)
        for y in range(-line_h, H, line_h + gap):
            pygame.draw.rect(scr, WHITE, (W//2 - line_w//2, y + offset, line_w, line_h))
        for r in obstacles:
            pygame.draw.rect(scr, BLACK, r)
            if car_rect.colliderect(r):
                engine.stop()
                return score

        scr.blit(car, car_rect)
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        score += 1

        pygame.display.flip()
        clock.tick(60)

def game_over_screen(score):
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(font_big.render("Game Over!", True, BLUE), (W//2-110, H//3))
        scr.blit(font.render(f"Score: {score}", True, BLACK), (W//2-55, H//2))
        scr.blit(font.render("Press ENTER to restart", True, BLACK), (W//2-120, H*2//3))
        pygame.display.flip(); clock.tick(60)

while True:
    start_screen()
    score = game_loop()
    game_over_screen(score)
