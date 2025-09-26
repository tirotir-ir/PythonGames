import pygame, sys, random, os                               # بازی، خروج، تصادفی، مسیر فایل‌ها
pygame.init(); pygame.mixer.init()                           # راه‌اندازی Pygame و موتور صدا

W, H = 400, 600                                              # ابعاد پنجره
scr = pygame.display.set_mode((W, H))                        # ساخت پنجره‌ی بازی
pygame.display.set_caption("Ultimate Arcade Car – Minimal (assets/)")  # عنوان پنجره
clock = pygame.time.Clock()                                  # کنترل FPS
WHITE, BLACK, RED = (255,255,255), (0,0,0), (255,0,0)        # چند رنگ پرکاربرد

ASSETS = "assets"                                            # پوشه‌ی دارایی‌ها (تصاویر/صداها)
road = pygame.transform.scale(                               # بارگذاری و اسکیل بک‌گراند جاده
    pygame.image.load(os.path.join(ASSETS,"road.png")).convert(), (W, H)
)
car  = pygame.transform.smoothscale(                         # بارگذاری و اسکیل نرم ماشین
    pygame.image.load(os.path.join(ASSETS,"car.png")).convert_alpha(), (50,100)
)
obsI = pygame.transform.smoothscale(                         # بارگذاری/اسکیل مانع
    pygame.image.load(os.path.join(ASSETS,"obstacle.png")).convert_alpha(), (50,50)
)
coinI= pygame.transform.smoothscale(                         # بارگذاری/اسکیل سکه
    pygame.image.load(os.path.join(ASSETS,"coin.png")).convert_alpha(), (30,30)
)

engine = pygame.mixer.Sound(os.path.join(ASSETS,"car_engine.wav")); engine.set_volume(0.5)  # صدای موتور + ولوم
crash  = pygame.mixer.Sound(os.path.join(ASSETS,"collision.wav"))                           # صدای تصادف
coinS  = pygame.mixer.Sound(os.path.join(ASSETS,"coin.wav"))                                # صدای گرفتن سکه
eng_ch = pygame.mixer.Channel(0)                                     # کانال اختصاصی برای موتور

font = pygame.font.SysFont(None, 30); big = pygame.font.SysFont(None, 50)                   # فونت‌ها
lanes = [W//6, W//2, 5*W//6]                                            # مرکز سه لاین: چپ/وسط/راست

def start_screen():                                                        # صفحه‌ی شروع
    while True:
        for e in pygame.event.get():                                       # رویدادها
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()              # بستن پنجره
            if e.type==pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return  # شروع بازی
        scr.fill(WHITE)                                                    # پس‌زمینه سفید
        scr.blit(big.render("Ultimate Car Game", True, BLACK), (W//2-140, H//3))  # تیتر
        scr.blit(big.render("Press ENTER", True, BLACK), (W//2-110, H//2))        # راهنما
        pygame.display.flip(); clock.tick(60)                              # نمایش و محدودسازی FPS

def game_over_screen(s):                                                   # صفحه‌ی پایان بازی
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return  # شروع مجدد
        scr.fill(WHITE)
        scr.blit(big.render("Game Over!", True, RED), (W//2-110, H//3))    # تیتر پایان
        scr.blit(big.render(f"Score: {s}", True, BLACK), (W//2-90, H//2))  # نمایش امتیاز
        pygame.display.flip(); clock.tick(60)

def game_loop():                                                           # یک دور بازی (تا تصادف)
    lane, car_rect = 1, car.get_rect(midbottom=(lanes[1], H-20))           # شروع از لاین وسط
    obstacles, coins, frame, score, spd, spawn, scroll = [], [], 0, 0, 5, 40, 0  # متغیرهای دنیا/امتیاز
    while True:
        for e in pygame.event.get():                                       # رویدادها
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()                                    # وضعیت کلیدها
        moved = False                                                       # آیا این فریم تغییر لاین داشتیم؟
        if keys[pygame.K_LEFT]  and lane>0: lane-=1; moved=True            # یک لاین به چپ (اگر ممکن)
        if keys[pygame.K_RIGHT] and lane<2: lane+=1; moved=True            # یک لاین به راست (اگر ممکن)
        if moved and not eng_ch.get_busy(): eng_ch.play(engine, loops=-1)  # پخش موتور هنگام جابه‌جایی
        if not moved and eng_ch.get_busy(): eng_ch.stop()                  # قطع موتور وقتی ساکن شدیم

        scroll = (scroll + spd) % H                                        # اسکرول بک‌گراند جاده (لوپ)
        scr.blit(road, (0, scroll-H)); scr.blit(road, (0, scroll))         # کشیدن دو کاشی پس‌زمینه

        car_rect.midbottom = (lanes[lane], H-20)                           # جای ماشین بر اساس لاین
        scr.blit(car, car_rect)                                            # رسم ماشین

        frame += 1                                                         # شمارنده فریم
        if frame % spawn == 0:                                             # هر N فریم: دشمن/سکه بساز
            r = obsI.get_rect(midtop=(random.choice(lanes), -obsI.get_height())); obstacles.append(r)
            if random.random()<0.3:
                c = coinI.get_rect(midtop=(random.choice(lanes), -coinI.get_height())); coins.append(c)

        for r in obstacles[:]:                                             # حرکت/رسم موانع
            r.y += spd; scr.blit(obsI, r)
            if r.top > H: obstacles.remove(r)                              # حذف مانع خارج از صفحه
            elif car_rect.colliderect(r): eng_ch.stop(); crash.play(); return score  # برخورد → پایان

        for c in coins[:]:                                                 # حرکت/رسم سکه‌ها
            c.y += spd; scr.blit(coinI, c)
            if c.top > H: coins.remove(c)                                  # حذف سکه خارج از صفحه
            elif car_rect.colliderect(c): score += 50; coins.remove(c); coinS.play() # گرفتن سکه

        if score and score % 500 == 0: spd += 0.5                          # افزایش تدریجی سختی
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10,10)); score += 1   # HUD + امتیاز زمان‌محور

        pygame.display.flip(); clock.tick(60)                               # نمایش فریم و قفل FPS

while True:                                                                 # چرخه‌ی کلی برنامه
    start_screen()                                                          # صفحه‌ی شروع
    s = game_loop()                                                         # اجرای بازی و دریافت امتیاز
    game_over_screen(s)                                                     # صفحه‌ی پایان/شروع مجدد
