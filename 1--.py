import pygame
pygame.init()
s = pygame.display.set_mode((400, 300))
car = pygame.image.load("car.png").convert_alpha()
r = car.get_rect(center=(200, 150))
clock = pygame.time.Clock()

# smooth steering params
x, y = float(r.x), float(r.y)
vx = vy = 0.0
ACCEL = 900.0     # px/s^2
FRICTION = 0.90   # 0..1 (higher = longer glide)
MAX_V = 300.0     # px/s

run = True
while run:
    dt = clock.tick(60) / 1000.0
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False

    k = pygame.key.get_pressed()
    ax = (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * ACCEL
    ay = (k[pygame.K_DOWN]  - k[pygame.K_UP])   * ACCEL

    vx = (vx + ax * dt) * (FRICTION if ax == 0 else 1.0)
    vy = (vy + ay * dt) * (FRICTION if ay == 0 else 1.0)
    vx = max(-MAX_V, min(MAX_V, vx))
    vy = max(-MAX_V, min(MAX_V, vy))

    x += vx * dt; y += vy * dt
    r.x, r.y = int(x), int(y)
    r.clamp_ip(s.get_rect()); x, y = r.x, r.y

    s.fill((255,255,255)); s.blit(car, r); pygame.display.flip()

pygame.quit()
