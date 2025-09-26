import pygame, sys
pygame.init()

W, H = 400, 300
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Simple Pygame – Minimal")
clock = pygame.time.Clock()

WHITE, BLUE = (255,255,255), (0,0,255)
rect = pygame.Rect(W//2-25, H//2-25, 50, 50)  # x, y, w, h
speed = 5

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed
    rect.y += (keys[pygame.K_DOWN]  - keys[pygame.K_UP])   * speed
    rect.clamp_ip(screen.get_rect())

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
