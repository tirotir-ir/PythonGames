import pygame, sys, os

# ---------- Init ----------
pygame.init()

# Try to init audio (fail-soft on PCs without sound device)
SOUND_OK = True
try:
    pygame.mixer.init()  # you can pass (44100, -16, 2, 512) if needed
except Exception:
    SOUND_OK = False

# ---------- Window ----------
WIDTH, HEIGHT = 400, 300
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car PNG Game with Sound")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)

# Helper to load files next to this .py
BASE = os.path.dirname(__file__)
def asset(*p): return os.path.join(BASE, *p)

# ---------- Load car image ----------
car = pygame.image.load(asset("car.png")).convert_alpha()

# (Optional) scale if too large
MAX_H = 60
if car.get_height() > MAX_H:
    scale = MAX_H / car.get_height()
    car = pygame.transform.smoothscale(car, (int(car.get_width()*scale), MAX_H))

car_rect = car.get_rect(center=(WIDTH // 2, HEIGHT // 2))
player_speed = 5

# ---------- Load engine sound ----------
engine_sound = None
engine_ch = None
volume = 0.5
muted = False

if SOUND_OK:
    try:
        # Put car_engine.wav next to this script (or rename below)
        engine_sound = pygame.mixer.Sound(asset("car_engine.wav"))
        engine_ch = pygame.mixer.Channel(0)  # dedicated channel for engine
        engine_ch.set_volume(volume)
    except Exception:
        engine_sound = None

# ---------- Game loop ----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Optional: mute & volume controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if SOUND_OK and engine_sound:
                if event.key == pygame.K_m:  # mute toggle
                    muted = not muted
                    if engine_ch:
                        engine_ch.set_volume(0.0 if muted else volume)
                if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):  # louder
                    volume = min(1.0, volume + 0.1)
                    if engine_ch and not muted:
                        engine_ch.set_volume(volume)
                if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS, pygame.K_UNDERSCORE):  # quieter
                    volume = max(0.0, volume - 0.1)
                    if engine_ch and not muted:
                        engine_ch.set_volume(volume)

    # Movement
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT]:
        car_rect.x -= player_speed
        moving = True
    if keys[pygame.K_RIGHT]:
        car_rect.x += player_speed
        moving = True
    if keys[pygame.K_UP]:
        car_rect.y -= player_speed
        moving = True
    if keys[pygame.K_DOWN]:
        car_rect.y += player_speed
        moving = True

    # Keep inside window
    car_rect.clamp_ip(window.get_rect())

    # Engine sound logic: loop while moving, stop when idle (with tiny fade)
    if SOUND_OK and engine_sound and engine_ch:
        if moving:
            if not engine_ch.get_busy():
                engine_ch.play(engine_sound, loops=-1, fade_ms=120)
                engine_ch.set_volume(0.0 if muted else volume)
        else:
            # fade out slightly to avoid click
            if engine_ch.get_busy():
                engine_ch.fadeout(150)

    # Draw
    window.fill(WHITE)
    window.blit(car, car_rect)

    # (Optional) draw simple HUD text without font file
    hud = f"[Arrows] Move   [M] Mute: {'ON' if muted else 'OFF'}   Vol: {int(volume*100)}%"
    pygame.display.set_caption("Car PNG Game with Sound  |  " + hud)

    pygame.display.flip()
    clock.tick(60)

# ---------- Quit ----------
pygame.quit()
sys.exit()

