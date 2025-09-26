import pygame, sys, random
pygame.init(); pygame.mixer.init()

W, H = 400, 600
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mini Car (PNG + Sound)")
clock = pygame.time.Clock()

GRAY, WHITE, BLACK = (200,200,200), (255,255,255), (0,0,0)

car = pygame.image.load("car.png").convert_alpha()
car_rect = car.get_rect(center=(W//2, H-100))
car_speed = 5

engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)

obs_size, obs_speed, spawn = 50, 5, 30
obstacles, frame, score = [], 0, 0

line_w, line_h, gap, offset = 10, 50, 30, 0
font = pygame.font.SysFont(None, 24)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE): running = False

    keys = pygame.key.get_pressed()
    moving = False
    car_rect.x += (keys[pygame.K_RIGHT]-keys[pygame.K_LEFT]) * car_speed; moving |= keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]
    car_rect.y += (keys[pygame.K_DOWN]-keys[pygame.K_UP])   * car_speed; moving |= keys[pygame.K_DOWN]  or keys[pygame.K_UP]
    car_rect.clamp_ip(scr.get_rect())

    if moving and not pygame.mixer.get_busy(): engine.play(-1)
    if not moving and pygame.mixer.get_busy(): engine.stop()

    offset = (offset + obs_speed) % (line_h + gap)
    frame += 1
    if frame % spawn == 0:
        obstacles.append(pygame.Rect(random.randint(0, W - obs_size), -obs_size, obs_size, obs_size))
    for r in obstacles:
        r.y += obs_speed

    scr.fill(GRAY)
    for y in range(-line_h, H, line_h + gap):
        pygame.draw.rect(scr, WHITE, (W//2 - line_w//2, y + offset, line_w, line_h))
    for r in obstacles:
        pygame.draw.rect(scr, BLACK, r)
        if car_rect.colliderect(r):
            engine.stop()
            print("Game Over! Score:", score)
            running = False

    scr.blit(car, car_rect)
    scr.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
    score += 1

    pygame.display.flip()
    clock.tick(30)

pygame.quit(); sys.exit()
