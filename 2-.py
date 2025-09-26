import pygame, sys, os

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 400, 300
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car PNG Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

# Helper to load files next to this script (works anywhere you run it from)
BASE = os.path.dirname(__file__)
def asset(*p): return os.path.join(BASE, *p)

# --- Load the car image ---
# Put car.png in the same folder as this .py file
car = pygame.image.load(asset("car.png")).convert_alpha()

# (Optional) scale down if it's too large
MAX_H = 60
if car.get_height() > MAX_H:
    scale = MAX_H / car.get_height()
    car = pygame.transform.smoothscale(car, (int(car.get_width()*scale), MAX_H))

car_rect = car.get_rect(center=(WIDTH // 2, HEIGHT // 2))
player_speed = 5

# --- Game loop ---
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        car_rect.x += player_speed
    if keys[pygame.K_UP]:
        car_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        car_rect.y += player_speed

    # Keep inside window
    car_rect.clamp_ip(window.get_rect())

    # Draw
    window.fill(WHITE)
    window.blit(car, car_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
