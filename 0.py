import pygame
pygame.init()
s = pygame.display.set_mode((400, 300))
car = pygame.image.load("car.png").convert_alpha()
r = car.get_rect(center=(200, 150))
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False
    s.fill((255,255,255)); s.blit(car, r); pygame.display.flip()
pygame.quit()
