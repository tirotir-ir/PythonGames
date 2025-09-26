import pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
plane = pygame.image.load("plane64.png").convert_alpha()  # یا plane48.png
rect = plane.get_rect(center=(200, 150))

clock = pygame.time.Clock()
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    screen.fill((20, 30, 40))
    screen.blit(plane, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
