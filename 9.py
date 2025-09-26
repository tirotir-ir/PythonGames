import pygame, sys, random, os
pygame.init(); pygame.mixer.init()

# -------- Window / constants --------
W, H = 400, 600
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ultimate Arcade Car – Smooth Steering")
clock = pygame.time.Clock()
WHITE, BLACK, RED = (255,255,255), (0,0,0), (255,0,0)
ASSETS = "assets"

font = pygame.font.SysFont(None, 28)
big  = pygame.font.SysFont(None, 48)

# -------- Load base assets (scale later for car) --------
road = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS,"road.png")).convert(), (W, H))
car_base = pygame.image.load(os.path.join(ASSETS,"car.png")).convert_alpha()
obs_img  = pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSETS,"obstacle.png")).convert_alpha(), (50,50))
coin_img = pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSETS,"coin.png")).convert_alpha(), (30,30))

engine = pygame.mixer.Sound(os.path.join(ASSETS,"car_engine.wav")); engine.set_volume(0.5)
crash  = pygame.mixer.Sound(os.path.join(ASSETS,"collision.wav"))
coinS  = pygame.mixer.Sound(os.path.join(ASSETS,"coin.wav"))
eng_ch = pygame.mixer.Channel(0)

# -------- Settings --------
CAR_SIZES = [(30,60), (40,80), (50,100)]         # Small / Medium / Large
SCROLLS   = [200, 260, 320]                      # px/s road + obstacle fall speed
DIFFS     = [("Easy", 46, 40), ("Normal", 36, 60), ("Hard", 26, 80)]  # (spawn frames, ramp per 500 score)
STEERS    = [600, 900, 1200]                     # px/s^2 (acceleration)

settings = {"car_idx":0, "speed_idx":1, "diff_idx":1, "steer_idx":0, "sound":True}

def summary(s):
    size = CAR_SIZES[s["car_idx"]]; spd = SCROLLS[s["speed_idx"]]
    diff = ["Easy","Normal","Hard"][s["diff_idx"]]; steer = ["Slow","Med","Fast"][s["steer_idx"]]
    snd  = "On" if s["sound"] else "Off"
    return f"Size:{size[0]}x{size[1]}  Scroll:{spd}  Diff:{diff}  Steer:{steer}  Sound:{snd}"

def draw_center(text, y, f=font, col=BLACK):
    img = f.render(text, True, col); scr.blit(img, img.get_rect(center=(W//2, y)))

def start_screen():
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): return "play"
                if e.key==pygame.K_s: return "settings"
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
        scr.fill(WHITE)
        draw_center("Ultimate Car Game", H//3, big)
        draw_center("ENTER: Play   S: Settings   ESC: Quit", H//2)
        draw_center(summary(settings), H//2+40)
        pygame.display.flip(); clock.tick(60)

def settings_menu():
    items = ["Car Size","Scroll Speed","Difficulty","Steer Speed","Sound","Back"]; idx = 0
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: return
                if e.key==pygame.K_UP:   idx = (idx-1)%len(items)
                if e.key==pygame.K_DOWN: idx = (idx+1)%len(items)
                if e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE):
                    step = 1 if e.key==pygame.K_RIGHT else -1
                    if items[idx]=="Car Size":    settings["car_idx"] = (settings["car_idx"]+step)%len(CAR_SIZES)
                    elif items[idx]=="Scroll Speed": settings["speed_idx"] = (settings["speed_idx"]+step)%len(SCROLLS)
                    elif items[idx]=="Difficulty": settings["diff_idx"] = (settings["diff_idx"]+step)%len(DIFFS)
                    elif items[idx]=="Steer Speed":settings["steer_idx"] = (settings["steer_idx"]+step)%len(STEERS)
                    elif items[idx]=="Sound":     settings["sound"] = not settings["sound"]
                    elif items[idx]=="Back":      return
        scr.fill(WHITE)
        draw_center("Settings", 100, big)
        vals = {
            "Car Size": f"{CAR_SIZES[settings['car_idx']][0]}x{CAR_SIZES[settings['car_idx']][1]}",
            "Scroll Speed": f"{SCROLLS[settings['speed_idx']]} px/s",
            "Difficulty": ["Easy","Normal","Hard"][settings["diff_idx"]],
            "Steer Speed": ["Slow","Med","Fast"][settings["steer_idx"]],
            "Sound": "On" if settings["sound"] else "Off",
            "Back": "Save & Return"
        }
        y=200
        for i,name in enumerate(items):
            prefix = "▶ " if i==idx else "  "
            draw_center(f"{prefix}{name}: {vals[name]}", y); y+=36
        pygame.display.flip(); clock.tick(60)

def game_over_screen(score):
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): return
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
        scr.fill(WHITE)
        draw_center("Game Over!", H//3, big, RED)
        draw_center(f"Score: {score}", H//2, big)
        draw_center("ENTER: Restart   ESC: Quit", 2*H//3)
        pygame.display.flip(); clock.tick(60)

def game_loop():
    # Apply settings
    car_w, car_h = CAR_SIZES[settings["car_idx"]]
    car = pygame.transform.smoothscale(car_base, (car_w, car_h))
    scroll_speed = float(SCROLLS[settings["speed_idx"]])   # px/s
    _, spawn_frames, ramp = DIFFS[settings["diff_idx"]]  # discard the name
    accel = float(STEERS[settings["steer_idx"]])           # px/s^2 (left/right)
    sound_on = settings["sound"]

    # State
    x = W/2 - car_w/2; y = H-20 - car_h
    vx = 0.0; MAX_VX = 260.0; FRICTION = 0.90
    obstacles, coins = [], []
    frame, score, scroll = 0, 0, 0.0

    while True:
        dt = clock.tick(60) / 1000.0  # seconds since last frame

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()

        # --- Smooth steering ---
        keys = pygame.key.get_pressed()
        ax = (-accel if keys[pygame.K_LEFT] else 0) + (accel if keys[pygame.K_RIGHT] else 0)
        vx += ax * dt
        vx *= FRICTION if ax==0 else 1.0
        vx = max(-MAX_VX, min(MAX_VX, vx))
        x += vx * dt

        # Clamp inside screen
        x = max(0, min(W - car_w, x))

        # Engine sound when actually moving
        moving = abs(vx) > 5
        if sound_on and moving and not eng_ch.get_busy(): eng_ch.play(engine, loops=-1)
        if (not moving or not sound_on) and eng_ch.get_busy(): eng_ch.stop()

        # --- World update ---
        scroll = (scroll + scroll_speed*dt) % H
        scr.blit(road, (0, scroll - H)); scr.blit(road, (0, scroll))

        car_rect = pygame.Rect(int(x), int(y), car_w, car_h)
        scr.blit(car, car_rect)

        # Spawning
        frame += 1
        if frame % spawn_frames == 0:
            r = obs_img.get_rect()
            r.x = random.randint(0, W - r.w); r.y = -r.h
            obstacles.append(r)
            if random.random() < 0.30:
                c = coin_img.get_rect()
                c.x = random.randint(0, W - c.w); c.y = -c.h
                coins.append(c)

        # Obstacles
        dy = int(scroll_speed * dt)
        for r in obstacles[:]:
            r.y += dy; scr.blit(obs_img, r)
            if r.top > H: obstacles.remove(r)
            elif car_rect.colliderect(r):
                eng_ch.stop(); crash.play(); return score

        # Coins
        for c in coins[:]:
            c.y += dy; scr.blit(coin_img, c)
            if c.top > H: coins.remove(c)
            elif car_rect.colliderect(c):
                score += 50; coins.remove(c); coinS.play()

        # Difficulty ramp
        if score and score % 500 == 0:
            scroll_speed += ramp  # faster fall/scroll

        # HUD
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10,10))
        scr.blit(font.render(summary(settings), True, WHITE), (10,34))
        score += 1

        pygame.display.flip()

# -------- Main loop --------
while True:
    choice = start_screen()
    if choice == "settings":
        settings_menu(); continue
    s = game_loop()
    game_over_screen(s)
