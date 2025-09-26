import pygame, sys

pygame.init()
pygame.mixer.init()

W, H = 400, 300
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

car = pygame.image.load("car.png").convert_alpha()
rect = car.get_rect(center=(W//2, H//2))
engine = pygame.mixer.Sound("car_engine.wav")
ch = pygame.mixer.Channel(0)
speed = 5

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT]:  rect.x -= speed; moving = True
    if keys[pygame.K_RIGHT]: rect.x += speed; moving = True
    if keys[pygame.K_UP]:    rect.y -= speed; moving = True
    if keys[pygame.K_DOWN]:  rect.y += speed; moving = True
    rect.clamp_ip(screen.get_rect())

    if moving and not ch.get_busy(): ch.play(engine, loops=-1)
    if not moving and ch.get_busy(): ch.stop()

    screen.fill((255, 255, 255))
    screen.blit(car, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
