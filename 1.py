import pygame
pygame.init()
s = pygame.display.set_mode((400, 300))
car = pygame.image.load("car.png").convert_alpha()
r = car.get_rect(center=(200, 150))
speed, run = 5, True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False
    k = pygame.key.get_pressed()
    r.x += (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * speed
    r.y += (k[pygame.K_DOWN]  - k[pygame.K_UP])   * speed
    r.clamp_ip(s.get_rect())
    s.fill((255,255,255)); s.blit(car, r); pygame.display.flip()
pygame.quit()
