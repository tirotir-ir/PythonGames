import pygame, sys, random, os                      # بازی (pygame)، خروج (sys)، تصادفی، مسیر فایل‌ها
pygame.init(); pygame.mixer.init()                  # راه‌اندازی گرافیک/رویداد و موتور صدا

# -------- Window / constants --------
W, H = 400, 600                                     # عرض و ارتفاع پنجره بازی
scr = pygame.display.set_mode((W, H))               # ساخت پنجره با این اندازه
pygame.display.set_caption("Ultimate Arcade Car – Smooth Steering")  # عنوان پنجره
clock = pygame.time.Clock()                         # کنترل نرخ فریم (FPS)
WHITE, BLACK, RED = (255,255,255), (0,0,0), (255,0,0)  # چند رنگ پرکاربرد
ASSETS = "assets"                                   # پوشهٔ دارایی‌ها (تصاویر/صداها)

font = pygame.font.SysFont(None, 28)                # فونت متن کوچک
big  = pygame.font.SysFont(None, 48)                # فونت تیتر

# -------- Load base assets (scale later for car) --------
road = pygame.transform.scale(                      # بارگذاری پس‌زمینه جاده و اسکیل به اندازه پنجره
    pygame.image.load(os.path.join(ASSETS,"road.png")).convert(), (W, H)
)
car_base = pygame.image.load(                       # تصویر ماشین (نسخهٔ پایه بدون اسکیل)
    os.path.join(ASSETS,"car.png")
).convert_alpha()
obs_img  = pygame.transform.smoothscale(            # تصویر مانع (اسکیل نرم 50×50)
    pygame.image.load(os.path.join(ASSETS,"obstacle.png")).convert_alpha(), (50,50)
)
coin_img = pygame.transform.smoothscale(            # تصویر سکه (اسکیل نرم 30×30)
    pygame.image.load(os.path.join(ASSETS,"coin.png")).convert_alpha(), (30,30)
)

engine = pygame.mixer.Sound(os.path.join(ASSETS,"car_engine.wav")); engine.set_volume(0.5)  # صدای موتور
crash  = pygame.mixer.Sound(os.path.join(ASSETS,"collision.wav"))                           # صدای تصادف
coinS  = pygame.mixer.Sound(os.path.join(ASSETS,"coin.wav"))                                # صدای گرفتن سکه
eng_ch = pygame.mixer.Channel(0)                      # یک کانال اختصاصی برای پخش موتور

# -------- Settings --------
CAR_SIZES = [(30,60), (40,80), (50,100)]           # اندازه‌های آماده ماشین: کوچک/متوسط/بزرگ
SCROLLS   = [200, 260, 320]                        # سرعت اسکرول جاده و سقوط اجسام (px/s)
DIFFS     = [("Easy", 46, 40), ("Normal", 36, 60), ("Hard", 26, 80)]  # (فاصله فریم ساخت، میزان رمپ)
STEERS    = [600, 900, 1200]                       # شتاب فرمان‌پذیری (px/s^2)

settings = {"car_idx":0, "speed_idx":1, "diff_idx":1, "steer_idx":0, "sound":True}  # تنظیمات فعلی

def summary(s):                                     # ساخت یک رشتهٔ خلاصه از تنظیمات برای HUD
    size = CAR_SIZES[s["car_idx"]]; spd = SCROLLS[s["speed_idx"]]
    diff = ["Easy","Normal","Hard"][s["diff_idx"]]; steer = ["Slow","Med","Fast"][s["steer_idx"]]
    snd  = "On" if s["sound"] else "Off"
    return f"Size:{size[0]}x{size[1]}  Scroll:{spd}  Diff:{diff}  Steer:{steer}  Sound:{snd}"

def draw_center(text, y, f=font, col=BLACK):        # نوشتن متن وسط-چین در y مشخص
    img = f.render(text, True, col); scr.blit(img, img.get_rect(center=(W//2, y)))

def start_screen():                                 # صفحه شروع: ENTER/SPACE = شروع، S = تنظیمات
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

def settings_menu():                                # منوی تنظیمات با حرکت ↑/↓ و تغییر ←/→
    items = ["Car Size","Scroll Speed","Difficulty","Steer Speed","Sound","Back"]; idx = 0
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: return
                if e.key==pygame.K_UP:   idx = (idx-1)%len(items)   # انتخاب مورد قبلی
                if e.key==pygame.K_DOWN: idx = (idx+1)%len(items)   # انتخاب مورد بعدی
                if e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE):
                    step = 1 if e.key==pygame.K_RIGHT else -1       # تغییر مقدار به چپ/راست
                    if items[idx]=="Car Size":    settings["car_idx"] = (settings["car_idx"]+step)%len(CAR_SIZES)
                    elif items[idx]=="Scroll Speed": settings["speed_idx"] = (settings["speed_idx"]+step)%len(SCROLLS)
                    elif items[idx]=="Difficulty": settings["diff_idx"] = (settings["diff_idx"]+step)%len(DIFFS)
                    elif items[idx]=="Steer Speed":settings["steer_idx"] = (settings["steer_idx"]+step)%len(STEERS)
                    elif items[idx]=="Sound":     settings["sound"] = not settings["sound"]
                    elif items[idx]=="Back":      return
        scr.fill(WHITE)
        draw_center("Settings", 100, big)
        vals = {                                      # متنِ مقدار هر آیتم برای نمایش
            "Car Size": f"{CAR_SIZES[settings['car_idx']][0]}x{CAR_SIZES[settings['car_idx']][1]}",
            "Scroll Speed": f"{SCROLLS[settings['speed_idx']]} px/s",
            "Difficulty": ["Easy","Normal","Hard"][settings["diff_idx"]],
            "Steer Speed": ["Slow","Med","Fast"][settings["steer_idx"]],
            "Sound": "On" if settings["sound"] else "Off",
            "Back": "Save & Return"
        }
        y=200
        for i,name in enumerate(items):
            prefix = "▶ " if i==idx else "  "        # فلش کنار آیتم انتخاب‌شده
            draw_center(f"{prefix}{name}: {vals[name]}", y); y+=36
        pygame.display.flip(); clock.tick(60)

def game_over_screen(score):                         # صفحه پایان: امتیاز و راهنمای کلیدها
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

def game_loop():                                    # اجرای یک دور بازی (برگشت امتیاز در صورت تصادف)
    # Apply settings
    car_w, car_h = CAR_SIZES[settings["car_idx"]]   # اندازهٔ انتخابی ماشین
    car = pygame.transform.smoothscale(car_base, (car_w, car_h))
    scroll_speed = float(SCROLLS[settings["speed_idx"]])      # سرعت اسکرول (px/s)
    _, spawn_frames, ramp = DIFFS[settings["diff_idx"]]       # فاصلهٔ ساخت مانع و شیب سختی
    accel = float(STEERS[settings["steer_idx"]])              # شتاب فرمان‌پذیری (چپ/راست)
    sound_on = settings["sound"]                              # وضعیت صدا

    # State
    x = W/2 - car_w/2; y = H-20 - car_h            # موقعیت اولیهٔ ماشین (پایین صفحه)
    vx = 0.0; MAX_VX = 260.0; FRICTION = 0.90      # سرعت افقی، سقف سرعت، اصطکاک ساده
    obstacles, coins = [], []                      # لیست موانع و سکه‌ها
    frame, score, scroll = 0, 0, 0.0               # شمارنده فریم/امتیاز/اسکرول پس‌زمینه

    while True:
        dt = clock.tick(60) / 1000.0               # فاصله زمان بین فریم‌ها به ثانیه

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()

        # --- Smooth steering ---
        keys = pygame.key.get_pressed()            # وضعیت کلیدها
        ax = (-accel if keys[pygame.K_LEFT] else 0) + (accel if keys[pygame.K_RIGHT] else 0)  # شتاب افقی
        vx += ax * dt                               # به‌روزرسانی سرعت با توجه به شتاب
        vx *= FRICTION if ax==0 else 1.0            # کاهش طبیعی سرعت وقتی کلیدی نگه نداشتی
        vx = max(-MAX_VX, min(MAX_VX, vx))          # محدود کردن سرعت در بازهٔ مجاز
        x  += vx * dt                               # حرکت ماشین با توجه به سرعت
        x  = max(0, min(W - car_w, x))              # جلوگیری از خروج از صفحه

        # Engine sound when actually moving
        moving = abs(vx) > 5                        # اگر واقعاً حرکت افقی داریم
        if sound_on and moving and not eng_ch.get_busy(): eng_ch.play(engine, loops=-1)  # پخش موتور
        if (not moving or not sound_on) and eng_ch.get_busy(): eng_ch.stop()             # توقف موتور

        # --- World update ---
        scroll = (scroll + scroll_speed*dt) % H     # اسکرول عمودی پس‌زمینه به‌صورت حلقه
        scr.blit(road, (0, scroll - H)); scr.blit(road, (0, scroll))  # کشیدن دو کاشی جاده

        car_rect = pygame.Rect(int(x), int(y), car_w, car_h)  # مستطیل برخورد ماشین
        scr.blit(car, car_rect)                    # رسم ماشین

        # Spawning (ساخت مانع و سکه)
        frame += 1
        if frame % spawn_frames == 0:
            r = obs_img.get_rect(); r.x = random.randint(0, W - r.w); r.y = -r.h
            obstacles.append(r)
            if random.random() < 0.30:
                c = coin_img.get_rect(); c.x = random.randint(0, W - c.w); c.y = -c.h
                coins.append(c)

        # Obstacles (حرکت و برخورد)
        dy = int(scroll_speed * dt)                 # جابجایی عمودی اجسام در این فریم
        for r in obstacles[:]:
            r.y += dy; scr.blit(obs_img, r)
            if r.top > H: obstacles.remove(r)       # حذف مانع خارج از صفحه
            elif car_rect.colliderect(r):           # برخورد با ماشین؟
                eng_ch.stop(); crash.play(); return score

        # Coins (حرکت و جمع‌کردن)
        for c in coins[:]:
            c.y += dy; scr.blit(coin_img, c)
            if c.top > H: coins.remove(c)           # حذف سکه خارج از صفحه
            elif car_rect.colliderect(c):
                score += 50; coins.remove(c); coinS.play()  # افزایش امتیاز و پخش صدا

        # Difficulty ramp (سخت‌تر شدن تدریجی)
        if score and score % 500 == 0:
            scroll_speed += ramp                    # سریع‌تر شدن اسکرول/سقوط

        # HUD (نمایش امتیاز و خلاصه تنظیمات)
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10,10))
        scr.blit(font.render(summary(settings), True, WHITE), (10,34))
        score += 1                                  # امتیاز زمان‌محور (هر فریم زنده‌ماندن)

        pygame.display.flip()                       # نمایش فریم روی صفحه

# -------- Main loop --------
while True:                                         # چرخهٔ کلی برنامه
    choice = start_screen()                         # صفحهٔ شروع → انتخاب بازی یا تنظیمات
    if choice == "settings":
        settings_menu(); continue                   # ورود به تنظیمات و برگشت
    s = game_loop()                                 # اجرای بازی و گرفتن امتیاز
    game_over_screen(s)                             # صفحهٔ پایان بازی
