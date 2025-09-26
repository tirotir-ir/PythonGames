import pygame, sys, random                              # کتابخانه‌ی بازی، خروج تمیز، و اعداد تصادفی
pygame.init(); pygame.mixer.init()                      # راه‌اندازی گرافیک/رویداد و موتور صدا

W, H = 400, 600                                         # اندازه‌ی پنجره (عرض، ارتفاع)
scr = pygame.display.set_mode((W, H))                   # ساخت پنجره‌ی بازی با این اندازه
pygame.display.set_caption("Mini Car – PNG")            # عنوان پنجره
clock = pygame.time.Clock()                             # ساعت برای کنترل FPS
WHITE, GRAY, BLACK, RED = (255,255,255), (50,50,50), (0,0,0), (255,0,0)  # رنگ‌ها
BLUE = (53, 55, 135)                                    # رنگ آبی برای تیتر پایان بازی

car = pygame.image.load("car.png").convert_alpha()      # بارگذاری تصویر ماشین با شفافیت
car_rect = car.get_rect(center=(W//2, H-100))           # مستطیل جایگاه تصویر؛ شروع نزدیک پایین وسط
car_speed = 5                                           # سرعت جابه‌جایی ماشین

engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)  # صدای موتور و تنظیم بلندی

obs_size, obs_speed, spawn = 50, 5, 30                  # اندازه مانع، سرعت سقوط، فاصلهٔ ساخت مانع (بر حسب فریم)
line_w, line_h, gap, offset = 10, 50, 30, 0             # ابعاد خط‌چین وسط جاده و جابه‌جایی عمودی الگو
font_big = pygame.font.SysFont(None, 48)                # فونت تیتر
font = pygame.font.SysFont(None, 28)                    # فونت متن/امتیاز

def start_screen():                                     # صفحه‌ی شروع: تا Enter/Space فشرده نشود، منتظر بمان
    while True:
        for e in pygame.event.get():                    # رسیدگی به رویدادها
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()   # بستن پنجره
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return  # شروع بازی
        scr.fill(WHITE)                                 # پس‌زمینه سفید
        scr.blit(font_big.render("Mini Car Game", True, BLACK), (W//2-120, H//3))  # تیتر
        scr.blit(font.render("Press ENTER to start", True, BLACK), (W//2-110, H//2))  # راهنما
        pygame.display.flip(); clock.tick(60)           # نمایش و محدودسازی FPS

def game_loop():                                        # حلقه‌ی اصلی بازی (اجرای یک دور)
    global offset
    obstacles, frame, score = [], 0, 0                  # لیست موانع، شمارنده‌ی فریم، امتیاز
    car_rect.center = (W//2, H-100)                     # ریست جای ماشین
    while True:
        for e in pygame.event.get():                    # رویدادها
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()    # بستن پنجره
        keys = pygame.key.get_pressed()                 # وضعیت کلیدها
        moving = False                                  # آیا در این فریم حرکت داریم؟
        car_rect.x += (keys[pygame.K_RIGHT]-keys[pygame.K_LEFT]) * car_speed; moving |= keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]  # افقی
        car_rect.y += (keys[pygame.K_DOWN]-keys[pygame.K_UP])   * car_speed; moving |= keys[pygame.K_DOWN]  or keys[pygame.K_UP]      # عمودی
        car_rect.clamp_ip(scr.get_rect())               # محدود به داخل پنجره

        if moving and not pygame.mixer.get_busy(): engine.play(-1)  # اگر حرکت می‌کنیم و صدایی پخش نمی‌شود → پخش موتور (لوپ)
        if not moving and pygame.mixer.get_busy(): engine.stop()     # اگر ایستادیم و صدا پخش است → توقف

        frame += 1                                      # یک فریم گذشت
        if frame % spawn == 0:                          # هر N فریم یک مانع بساز
            obstacles.append(pygame.Rect(random.randint(0, W-obs_size), -obs_size, obs_size, obs_size))
        for r in obstacles: r.y += obs_speed            # پایین آمدن همه‌ی موانع

        offset = (offset + obs_speed) % (line_h + gap)  # حرکت الگوی خط‌چین برای حس حرکت جاده

        scr.fill(GRAY)                                  # پس‌زمینه‌ی خاکستری (جاده)
        for y in range(-line_h, H, line_h + gap):       # رسم خط‌چین‌های وسط جاده
            pygame.draw.rect(scr, WHITE, (W//2 - line_w//2, y + offset, line_w, line_h))
        for r in obstacles:
            pygame.draw.rect(scr, BLACK, r)             # رسم مانع به صورت مستطیل سیاه
            if car_rect.colliderect(r):                 # برخورد ماشین با مانع؟
                engine.stop()                           # قطع صدا
                return score                            # خروج از حلقه‌ی بازی و برگرداندن امتیاز

        scr.blit(car, car_rect)                         # کشیدن ماشین
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))  # نمایش امتیاز
        score += 1                                      # افزایش امتیاز (زمان-محور)

        pygame.display.flip()                           # نمایش فریم جدید
        clock.tick(60)                                  # FPS=60

def game_over_screen(score):                            # صفحه‌ی پایان بازی با امتیاز
    while True:
        for e in pygame.event.get():                    # رویدادها
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()    # بستن
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return  # شروع مجدد
        scr.fill(WHITE)                                 # پس‌زمینه سفید
        scr.blit(font_big.render("Game Over!", True, BLUE), (W//2-110, H//3))  # تیتر پایان
        scr.blit(font.render(f"Score: {score}", True, BLACK), (W//2-55, H//2)) # امتیاز
        scr.blit(font.render("Press ENTER to restart", True, BLACK), (W//2-120, H*2//3))  # راهنما
        pygame.display.flip(); clock.tick(60)           # نمایش و محدودسازی FPS

while True:                                             # چرخه‌ی کل بازی: شروع → بازی → پایان → تکرار
    start_screen()                                      # صفحه‌ی شروع
    score = game_loop()                                 # اجرای بازی و گرفتن امتیاز نهایی
    game_over_screen(score)                             # نمایش پایان بازی و انتظار برای شروع دوباره
