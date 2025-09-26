import pygame, sys, random, os, json
pygame.init()

# ---------- Safe audio init ----------
SOUND_ON = True
try:
    pygame.mixer.init()
except Exception:
    SOUND_ON = False

# ---------- Window & constants ----------
W, H = 400, 600
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ultimate Arcade Car – FINAL | Tirotir AI")
clock = pygame.time.Clock()

WHITE, BLACK, RED, GRAY, YELLOW, BLUE, GREEN, ORANGE = (255,255,255), (0,0,0), (255,0,0), (60,60,60), (255,215,0), (70,120,255), (0,200,0), (255,140,0)
ASSETS = "assets"
SAVE_FILE = "save.json"

font  = pygame.font.SysFont(None, 26)
big   = pygame.font.SysFont(None, 48)
small = pygame.font.SysFont(None, 20)

# ---------- Helpers ----------
def draw_center(text, y, f=font, col=WHITE):
    img = f.render(text, True, col)
    scr.blit(img, img.get_rect(center=(W//2, y)))

def load_image(name, size=None, alpha=True, fallback_color=ORANGE):
    path = os.path.join(ASSETS, name)
    surf = None
    if os.path.exists(path):
        img = pygame.image.load(path)
        img = img.convert_alpha() if alpha else img.convert()
        if size: img = pygame.transform.smoothscale(img, size)
        surf = img
    else:
        # simple fallback
        w,h = size if size else (50,50)
        surf = pygame.Surface((w,h), pygame.SRCALPHA if alpha else 0)
        surf.fill(fallback_color)
        pygame.draw.rect(surf, BLACK, surf.get_rect(), 2)
    return surf

def load_sound(name, volume=0.6):
    if not SOUND_ON: return None
    path = os.path.join(ASSETS, name)
    if os.path.exists(path):
        s = pygame.mixer.Sound(path)
        s.set_volume(volume)
        return s
    return None

def play(sound):
    if sound and SOUND_ON:
        sound.play()

# ---------- Assets (with fallbacks) ----------
road = load_image("road.png", (W, H), alpha=False, fallback_color=GRAY)
car_base = load_image("car.png", (50,100), alpha=True, fallback_color=BLUE)  # base will be rescaled anyway
obstacle_img = load_image("obstacle.png", (50,50), alpha=True, fallback_color=BLACK)
coin_img = load_image("coin.png", (30,30), alpha=True, fallback_color=YELLOW)

engine_s = load_sound("car_engine.wav", 0.5)
crash_s  = load_sound("collision.wav", 0.8)
coin_s   = load_sound("coin.wav", 0.6)
power_s  = load_sound("power.wav", 0.7)
pause_s  = load_sound("pause.wav", 0.5)
eng_ch   = pygame.mixer.Channel(0) if SOUND_ON else None

# ---------- Settings ----------
CAR_SIZES = [(30,60), (40,80), (50,100)]      # Small / Medium / Large
SCROLLS   = [200, 260, 320]                   # px/s base world speed
STEERS    = [600, 900, 1200]                  # px/s^2 steering accel
DIFFS     = [("Easy",   46,  40),             # (spawn frames, ramp per threshold)
             ("Normal", 36,  60),
             ("Hard",   26,  80)]

settings = {"car_idx":1, "speed_idx":1, "steer_idx":1, "diff_idx":1, "sound":SOUND_ON}

def settings_summary():
    size = CAR_SIZES[settings["car_idx"]]
    spd  = SCROLLS[settings["speed_idx"]]
    steer= ["Slow","Med","Fast"][settings["steer_idx"]]
    diff = ["Easy","Normal","Hard"][settings["diff_idx"]]
    snd  = "On" if settings["sound"] else "Off"
    return f"Size:{size[0]}x{size[1]}  Scroll:{spd}  Steer:{steer}  Diff:{diff}  Sound:{snd}"

# ---------- High scores ----------
def load_save():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE,"r",encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"highscores":[0,0,0,0,0]}

def save_save(data):
    try:
        with open(SAVE_FILE,"w",encoding="utf-8") as f: json.dump(data,f)
    except: pass

save_data = load_save()

def update_highscores(score):
    hs = save_data["highscores"]
    hs.append(score)
    hs.sort(reverse=True)
    save_data["highscores"] = hs[:5]
    save_save(save_data)

# ---------- UI Screens ----------
def start_screen():
    tips = [
        "Tip: Hold SHIFT for Nitro (consumes bar).",
        "Tip: Shield saves you from one crash.",
        "Tip: Magnet pulls nearby coins for a short time.",
        "Tip: Press P to pause.",
    ]
    tip_idx, tip_timer = 0, 0
    while True:
        dt = clock.tick(60)
        tip_timer += dt
        if tip_timer > 3000:
            tip_timer = 0
            tip_idx = (tip_idx + 1) % len(tips)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): return "play"
                if e.key == pygame.K_s: return "settings"
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

        scr.blit(road, (0,0))
        pygame.draw.rect(scr, (0,0,0,160), (0,0,W,H))
        draw_center("Ultimate Arcade Car – FINAL", H//3, big)
        draw_center("ENTER: Play   S: Settings   ESC: Quit", H//2)
        draw_center(settings_summary(), H//2+38, small)
        draw_center(f"Top Scores: {save_data['highscores']}", H//2+70, small)
        draw_center(tips[tip_idx], H-40, small)
        pygame.display.flip()

def settings_menu():
    items = ["Car Size","Scroll Speed","Steer Speed","Difficulty","Sound","Reset Defaults","Back"]
    idx = 0
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: return
                if e.key==pygame.K_UP:   idx = (idx-1)%len(items)
                if e.key==pygame.K_DOWN: idx = (idx+1)%len(items)
                if e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE):
                    step = 1 if e.key==pygame.K_RIGHT else -1
                    name = items[idx]
                    if   name=="Car Size":     settings["car_idx"]  = (settings["car_idx"] + step) % len(CAR_SIZES)
                    elif name=="Scroll Speed": settings["speed_idx"]= (settings["speed_idx"] + step) % len(SCROLLS)
                    elif name=="Steer Speed":  settings["steer_idx"]= (settings["steer_idx"] + step) % len(STEERS)
                    elif name=="Difficulty":   settings["diff_idx"] = (settings["diff_idx"] + step) % len(DIFFS)
                    elif name=="Sound":        settings["sound"]    = not settings["sound"]
                    elif name=="Reset Defaults":
                        settings.update({"car_idx":1,"speed_idx":1,"steer_idx":1,"diff_idx":1,"sound":SOUND_ON})
                    elif name=="Back":         return

        scr.blit(road,(0,0))
        pygame.draw.rect(scr, (0,0,0,160), (0,0,W,H))
        draw_center("Settings", 90, big)
        vals = {
            "Car Size":     f"{CAR_SIZES[settings['car_idx']][0]}x{CAR_SIZES[settings['car_idx']][1]}",
            "Scroll Speed": f"{SCROLLS[settings['speed_idx']]} px/s",
            "Steer Speed":  ["Slow","Med","Fast"][settings["steer_idx"]],
            "Difficulty":   ["Easy","Normal","Hard"][settings["diff_idx"]],
            "Sound":        "On" if settings["sound"] else "Off",
            "Reset Defaults": "↺",
            "Back":         "Save & Return",
        }
        y = 170
        for i,name in enumerate(items):
            col = YELLOW if i==idx else WHITE
            draw_center(f"{'▶ ' if i==idx else '  '}{name}: {vals[name]}", y, font, col)
            y += 36
        draw_center(settings_summary(), H-36, small)
        pygame.display.flip(); clock.tick(60)

def pause_screen():
    play(pause_s)
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key in (pygame.K_p, pygame.K_RETURN, pygame.K_SPACE):
                    play(pause_s); return
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
        # dark overlay
        overlay = pygame.Surface((W,H), pygame.SRCALPHA)
        overlay.fill((0,0,0,160))
        scr.blit(overlay, (0,0))
        draw_center("PAUSED", H//2-10, big, YELLOW)
        draw_center("P/ENTER: Resume   ESC: Quit", H//2+30, font)
        pygame.display.flip(); clock.tick(60)

def game_over_screen(score):
    update_highscores(score)
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): return
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
        scr.blit(road,(0,0))
        pygame.draw.rect(scr, (0,0,0,160), (0,0,W,H))
        draw_center("Game Over!", H//3, big, RED)
        draw_center(f"Score: {score}", H//2, big)
        draw_center(f"Top Scores: {save_data['highscores']}", H//2+40, small)
        draw_center("ENTER: Restart   ESC: Quit", 2*H//3, font)
        pygame.display.flip(); clock.tick(60)

# ---------- Powerups ----------
# type: "shield" (1 hit), "magnet" (pull coins radius), "slow" (world slow for T sec)
POWER_TYPES = ["shield", "magnet", "slow"]
POWER_COLORS= {"shield":GREEN, "magnet":ORANGE, "slow":BLUE}

# ---------- Game loop ----------
def game_loop():
    # Apply settings
    car_w, car_h = CAR_SIZES[settings["car_idx"]]
    car = pygame.transform.smoothscale(car_base, (car_w, car_h))
    scroll_speed_base = float(SCROLLS[settings["speed_idx"]])
    _, spawn_frames_base, ramp_per = DIFFS[settings["diff_idx"]]
    accel = float(STEERS[settings["steer_idx"]])
    sound_on = settings["sound"]

    # State
    x = W/2 - car_w/2
    y = H - 20 - car_h
    vx, MAX_VX = 0.0, 260.0
    FRICTION = 0.90

    obstacles, coins, powerups = [], [], []
    frame, score, scroll = 0, 0, 0.0
    world_speed = scroll_speed_base

    # Difficulty ramp control
    last_ramp_block = 0  # increases at 500,1000,...
    spawn_frames = spawn_frames_base

    # Nitro
    nitro = 100.0  # percent
    NITRO_COST = 35.0  # per second when holding
    NITRO_REGEN = 12.0 # per second when idle
    NITRO_BOOST = 1.6  # multiplier on accel & MAX_VX when active

    # Power states
    shield_hits = 0
    magnet_t, slow_t = 0.0, 0.0
    MAGNET_RADIUS = 120
    SLOW_FACTOR   = 0.55
    SLOW_TIME     = 4.0
    POWER_SPAWN_CHANCE = 0.10  # 10% when spawning batch

    # Engine channel
    def engine_playing(): return eng_ch.get_busy() if eng_ch else False

    while True:
        dt = clock.tick(60) / 1000.0

        # events
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if e.key==pygame.K_p: pause_screen()

        # input
        keys = pygame.key.get_pressed()
        nitro_active = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        a = accel * (NITRO_BOOST if (nitro_active and nitro>0) else 1.0)
        max_v = MAX_VX * (NITRO_BOOST if (nitro_active and nitro>0) else 1.0)

        ax = (-a if keys[pygame.K_LEFT] else 0) + (a if keys[pygame.K_RIGHT] else 0)
        vx += ax * dt
        vx *= FRICTION if ax == 0 else 1.0
        vx = max(-max_v, min(max_v, vx))
        x  += vx * dt
        x  = max(0, min(W - car_w, x))

        # nitro energy
        if nitro_active and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and nitro>0:
            nitro = max(0.0, nitro - NITRO_COST * dt)
        else:
            nitro = min(100.0, nitro + NITRO_REGEN * dt)

        # engine sound
        moving = abs(vx) > 5
        if sound_on and engine_s and eng_ch:
            if moving and not engine_playing(): eng_ch.play(engine_s, loops=-1)
            if (not moving or not sound_on) and engine_playing(): eng_ch.stop()

        # world update & background
        if slow_t > 0:
            slow_t = max(0.0, slow_t - dt)
        slow_mul = SLOW_FACTOR if slow_t > 0 else 1.0
        scroll += world_speed * slow_mul * dt
        scroll %= H
        scr.blit(road, (0, scroll - H)); scr.blit(road, (0, scroll))

        car_rect = pygame.Rect(int(x), int(y), car_w, car_h)
        scr.blit(car, car_rect)

        # spawning
        frame += 1
        if frame % spawn_frames == 0:
            # obstacles
            for _ in range(1):  # can increase batch size if needed
                r = obstacle_img.get_rect()
                r.x = random.randint(0, W - r.w); r.y = -r.h
                obstacles.append(r)
            # coins
            if random.random() < 0.35:
                c = coin_img.get_rect()
                c.x = random.randint(0, W - c.w); c.y = -c.h
                coins.append(c)
            # powerups
            if random.random() < POWER_SPAWN_CHANCE:
                kind = random.choice(POWER_TYPES)
                pu = pygame.Rect(0,0,26,26)
                pu.x = random.randint(0, W - pu.w); pu.y = -pu.h
                powerups.append((kind, pu))

        # move & draw obstacles
        dy = int(world_speed * slow_mul * dt)
        for r in obstacles[:]:
            r.y += dy; scr.blit(obstacle_img, r)
            if r.top > H: obstacles.remove(r)
            elif car_rect.colliderect(r):
                if shield_hits > 0:
                    shield_hits -= 1
                    obstacles.remove(r)
                    play(power_s)
                else:
                    if eng_ch: eng_ch.stop()
                    play(crash_s)
                    return score

        # move & draw coins (magnet effect)
        for c in coins[:]:
            # magnet pull
            if magnet_t > 0:
                dx = (car_rect.centerx - c.centerx)
                dyc= (car_rect.centery - c.centery)
                if dx*dx + dyc*dyc < MAGNET_RADIUS*MAGNET_RADIUS:
                    # simple pull
                    c.centerx += int(200 * dt * (1 if dx>0 else -1))
                    c.centery += int(200 * dt * (1 if dyc>0 else -1))
            c.y += dy; scr.blit(coin_img, c)
            if c.top > H: coins.remove(c)
            elif car_rect.colliderect(c):
                score += 50; coins.remove(c); play(coin_s)

        # move & draw powerups
        for kind, r in powerups[:]:
            r.y += dy
            pygame.draw.rect(scr, POWER_COLORS[kind], r, border_radius=6)
            txt = small.render(kind[0].upper(), True, BLACK)
            scr.blit(txt, txt.get_rect(center=r.center))
            if r.top > H: powerups.remove((kind,r))
            elif car_rect.colliderect(r):
                powerups.remove((kind,r)); play(power_s)
                if kind == "shield": shield_hits = min(1, shield_hits+1)
                elif kind == "magnet": magnet_t = 5.0
                elif kind == "slow": slow_t = SLOW_TIME

        # timers decrease
        if magnet_t > 0: magnet_t = max(0.0, magnet_t - dt)

        # difficulty ramp (every 500 points, once)
        block = score // 500
        if block > last_ramp_block:
            last_ramp_block = block
            world_speed += ramp_per * 0.01   # small but noticeable boost
            spawn_frames = max(12, spawn_frames - 2)

        # HUD
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10,10))
        # nitro bar
        pygame.draw.rect(scr, WHITE, (10, 34, 120, 10), 1)
        pygame.draw.rect(scr, BLUE,  (11, 35, int(118*nitro/100), 8))
        scr.blit(small.render("Nitro", True, WHITE), (135,31))
        # shield indicator
        if shield_hits>0:
            pygame.draw.circle(scr, GREEN, (W-24, 22), 10); scr.blit(small.render("S",True,BLACK),(W-28,13))
        # magnet/slow timers
        if magnet_t>0: scr.blit(small.render(f"M:{magnet_t:0.0f}", True, YELLOW),(W-70, 40))
        if slow_t>0:   scr.blit(small.render(f"SL:{slow_t:0.0f}", True, ORANGE),(W-70, 58))
        # controls hint
        scr.blit(small.render("←/→ move | Shift nitro | P pause", True, WHITE),(10,H-22))

        score += 1
        pygame.display.flip()

# ---------- Main ----------
while True:
    choice = start_screen()
    if choice == "settings":
        settings_menu(); continue
    s = game_loop()
    game_over_screen(s)
