import pygame, sys
pygame.init()

W, H = 400, 300
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Step 1 – Show the Car")
clock = pygame.time.Clock()

car = pygame.image.load("car.png").convert_alpha()
rect = car.get_rect(center=(W//2, H//2))

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(car, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
