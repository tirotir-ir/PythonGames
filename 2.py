import pygame, sys, os

pygame.init()
W, H = 400, 300
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Car PNG – Minimal")
clock = pygame.time.Clock()

# Load car.png from the script's folder (works no matter where you run it)
car = pygame.image.load(os.path.join(os.path.dirname(__file__), "car.png")).convert_alpha()
rect = car.get_rect(center=(W//2, H//2))
speed = 5

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  rect.x -= speed
    if keys[pygame.K_RIGHT]: rect.x += speed
    if keys[pygame.K_UP]:    rect.y -= speed
    if keys[pygame.K_DOWN]:  rect.y += speed
    rect.clamp_ip(screen.get_rect())

    screen.fill((255,255,255))
    screen.blit(car, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
