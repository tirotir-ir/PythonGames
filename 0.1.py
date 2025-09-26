import pygame, sys
pygame.init()

W, H = 400, 300
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Step 2 – Move the Car")
clock = pygame.time.Clock()

car = pygame.image.load("car.png").convert_alpha()
rect = car.get_rect(center=(W//2, H//2))
speed = 5

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  rect.x -= speed
    if keys[pygame.K_RIGHT]: rect.x += speed
    if keys[pygame.K_UP]:    rect.y -= speed
    if keys[pygame.K_DOWN]:  rect.y += speed
    # (Challenge for kids) Keep the car inside the window:
    # rect.clamp_ip(screen.get_rect())

    screen.fill((255, 255, 255))
    screen.blit(car, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
