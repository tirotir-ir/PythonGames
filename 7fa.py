import pygame, sys, random                           # کتابخانه بازی، خروج، اعداد تصادفی
pygame.init(); pygame.mixer.init()                   # راه‌اندازی گرافیک/رویداد و موتور صدا

# --- Window / constants ---
W, H = 400, 600                                      # عرض و ارتفاع پنجره
scr = pygame.display.set_mode((W, H))                # ساخت پنجره با اندازه مشخص
pygame.display.set_caption("Ultimate Arcade Car – Smooth + Size")  # عنوان پنجره
clock = pygame.time.Clock()                          # کنترل نرخ فریم (FPS)
WHITE, GRAY, BLACK, RED = (255,255,255), (50,50,50), (0,0,0), (255,0,0)  # رنگ‌ها

# --- Assets ---
road = pygame.transform.scale(                       # بارگذاری/اسکیل بک‌گراند جاده به اندازه پنجره
    pygame.image.load("road.png").convert(), (W, H)
)
car_src = pygame.image.load("car.png").convert_alpha()  # تصویر اصلی ماشین (بدون اسکیل)
obsI = pygame.transform.smoothscale(                 # اسکیل نرم مانع به 50×50
    pygame.image.load("obstacle.png").convert_alpha(), (50, 50)
)
coinI = pygame.transform.smoothscale(                # اسکیل نرم سکه به 30×30
    pygame.image.load("coin.png").convert_alpha(), (30, 30)
)

engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)  # صدای موتور + ولوم
crash  = pygame.mixer.Sound("collision.wav")        # صدای تصادف
coinS  = pygame.mixer.Sound("coin.wav")             # صدای گرفتن سکه
eng_ch = pygame.mixer.Channel(0)                    # کانال اختصاصی برای پخش موتور

font = pygame.font.SysFont(None, 30)                # فونت نوشته HUD
big  = pygame.font.SysFont(None, 50)                # فونت تیترها

# --- Car size presets (press 1/2/3 in-game) ---
PRESETS = [(30,60), (40,80), (50,100)]              # سه اندازه: کوچک/متوسط/بزرگ
car = pygame.transform.smoothscale(car_src, PRESETS[1])  # اندازه پیش‌فرض: متوسط
car_w, car_h = car.get_size()                        # ذخیره عرض/ارتفاع فعلی ماشین

def set_car_size(idx):                                # تغییر سریع اندازه ماشین (کلیدهای 1/2/3)
    global car, car_w, car_h
    car = pygame.transform.smoothscale(car_src, PRESETS[idx])
    car_w, car_h = car.get_size()

def start_screen():                                   # صفحه شروع: تا ENTER/SPACE نزنی وارد بازی نمی‌شود
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Ultimate Car Game", True, BLACK), (W//2-140, H//3))
        scr.blit(big.render("Press ENTER", True, BLACK), (W//2-110, H//2))
        pygame.display.flip(); clock.tick(60)

def game_over_screen(score):                          # صفحه پایان: نمایش امتیاز و انتظار برای شروع دوباره
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Game Over!", True, RED), (W//2-110, H//3))
        scr.blit(big.render(f"Score: {score}", True, BLACK), (W//2-90, H//2))
        scr.blit(font.render("Press ENTER to restart", True, BLACK), (W//2-120, 2*H//3))
        pygame.display.flip(); clock.tick(60)

def game_loop():                                      # یک دور بازی تا لحظه تصادف؛ امتیاز برمی‌گرداند
    # --- Smooth steering params ---
    x = W/2 - car_w/2                                 # موقعیت افقی ماشین (float برای حرکت نرم)
    y = H - 20 - car_h                                # موقعیت عمودی ثابت نزدیک پایین
    vx = 0.0                                          # سرعت افقی (px/s)
    ACCEL = 900.0                                     # شتاب افقی هنگام نگه‌داشتن ←/→ (px/s^2)
    MAX_VX = 260.0                                    # سقف سرعت افقی
    FRICTION = 0.90                                   # کاهش سرعت وقتی کلیدی نگه نداشته‌ای (اصطکاک ساده)

    obstacles, coins = [], []                         # لیست موانع و سکه‌ها
    spawn, scroll_speed, scroll, frame, score = 40, 5.0, 0.0, 0, 0  # پارامترهای دنیا/اسکرول/امتیاز

    while True:
        dt = clock.tick(60) / 1000.0                  # مدت هر فریم به ثانیه (برای فیزیکِ زمان‌واقعی)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                # quick size presets: 1/2/3
                if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    old_centerx = int(x + car_w/2)    # حفظ مرکز فعلی هنگام تغییر اندازه
                    idx = {pygame.K_1:0, pygame.K_2:1, pygame.K_3:2}[e.key]
                    set_car_size(idx)
                    # تنظیم x تا ماشین بعد از تغییر سایز در همان مرکز بماند و از کادر بیرون نزند
                    x = max(0, min(W - car_w, old_centerx - car_w/2))

        # --- Smooth steering ---
        keys = pygame.key.get_pressed()               # وضعیت کلیدها (بولی)
        ax = (-ACCEL if keys[pygame.K_LEFT] else 0) + (ACCEL if keys[pygame.K_RIGHT] else 0)  # شتاب
        vx += ax * dt                                 # به‌روزرسانی سرعت: v = v + a*dt
        vx *= FRICTION if ax == 0 else 1.0            # اگر ورودی نیست، کمی سرعت را کم کن (ترمز طبیعی)
        vx = max(-MAX_VX, min(MAX_VX, vx))            # محدودکردن سرعت به بازه مجاز
        x += vx * dt                                  # به‌روزرسانی موقعیت: x = x + v*dt
        x = max(0, min(W - car_w, x))                 # جلوگیری از خروج از پنجره

        # Engine sound only when actually moving
        moving = abs(vx) > 5                          # اگر واقعاً حرکت افقی داریم
        if moving and not eng_ch.get_busy(): eng_ch.play(engine, loops=-1)  # پخش موتور
        if not moving and eng_ch.get_busy(): eng_ch.stop()                   # توقف موتور

        # --- World update ---
        scroll = (scroll + scroll_speed) % H          # مقدار اسکرول عمودی بک‌گراند (لوپ)
        scr.blit(road, (0, scroll - H)); scr.blit(road, (0, scroll))  # کشیدن دو کاشی جاده

        car_rect = pygame.Rect(int(x), int(y), car_w, car_h)  # مستطیل برخورد ماشین
        scr.blit(car, car_rect)                        # کشیدن ماشین

        # Spawn
        frame += 1
        if frame % spawn == 0:                         # هر N فریم یک مانع و گاهی سکه بساز
            r = obsI.get_rect()
            r.x = random.randint(0, W - r.w); r.y = -r.h
            obstacles.append(r)
            if random.random() < 0.3:
                c = coinI.get_rect()
                c.x = random.randint(0, W - c.w); c.y = -c.h
                coins.append(c)

        # Move/draw obstacles
        for r in obstacles[:]:                         # حرکت/رسم مانع‌ها
            r.y += scroll_speed
            scr.blit(obsI, r)
            if r.top > H: obstacles.remove(r)         # حذف موانع خارج از صفحه
            elif car_rect.colliderect(r):             # برخورد با ماشین؟
                eng_ch.stop(); crash.play()           # قطع موتور و پخش تصادف
                return score

        # Move/draw coins
        for c in coins[:]:                             # حرکت/رسم سکه‌ها
            c.y += scroll_speed
            scr.blit(coinI, c)
            if c.top > H: coins.remove(c)             # حذف سکه‌های خارج از صفحه
            elif car_rect.colliderect(c):             # اگر ماشین سکه را گرفت
                score += 50; coins.remove(c); coinS.play()

        # Difficulty ramp
        if score and score % 500 == 0:                 # هر ۵۰۰ امتیاز کمی سرعت دنیا را بیشتر کن
            scroll_speed += 0.5

        # HUD
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))  # نمایش امتیاز
        scr.blit(font.render("Size 1/2/3  |  ←/→ steer", True, WHITE), (10, 34))  # راهنما
        score += 1                                     # امتیاز زمان‌محور (زنده‌ماندن)

        pygame.display.flip()                          # نمایش فریم روی صفحه

# --- Run ---
while True:                                           # چرخه کلی: شروع → بازی → پایان → تکرار
    start_screen()
    s = game_loop()
    game_over_screen(s)
