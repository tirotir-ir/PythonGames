import pygame, sys, random                         # Pygame برای بازی، sys برای خروج، random برای اعداد تصادفی
pygame.init(); pygame.mixer.init()                 # راه‌اندازی ماژول‌های گرافیک/رویداد و صدا

W, H = 400, 600                                    # عرض و ارتفاع پنجره
scr = pygame.display.set_mode((W, H))              # ساخت پنجره‌ی بازی
pygame.display.set_caption("Mini Car (PNG + Sound)") # عنوان پنجره
clock = pygame.time.Clock()                        # ساعت برای محدود کردن FPS

GRAY, WHITE, BLACK = (200,200,200), (255,255,255), (0,0,0)   # رنگ‌های پرکاربرد

car = pygame.image.load("car.png").convert_alpha() # بارگذاری تصویر ماشین با شفافیت
car_rect = car.get_rect(center=(W//2, H-100))      # قرار دادن ماشین نزدیک پایین وسط
car_speed = 5                                      # سرعت حرکت ماشین

engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)  # صدای موتور و تنظیم بلندی

obs_size, obs_speed, spawn = 50, 5, 30             # اندازه مانع، سرعت سقوط، هر چند فریم یک‌بار ساخت مانع
obstacles, frame, score = [], 0, 0                 # لیست موانع، شمارنده فریم‌ها، امتیاز

line_w, line_h, gap, offset = 10, 50, 30, 0        # اندازه خط‌چین وسط جاده و فاصله‌ها و جابه‌جایی عمودی
font = pygame.font.SysFont(None, 24)               # فونت پیش‌فرض با اندازه ۲۴

running = True                                     # پرچم اجرای حلقه
while running:                                     # حلقه اصلی بازی
    for e in pygame.event.get():                   # پردازش رویدادها
        if e.type == pygame.QUIT or (e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE):
            running = False                        # بستن پنجره یا زدن ESC → خروج از حلقه

    keys = pygame.key.get_pressed()                # وضعیت کلیدها (بولی برای هر کلید)
    moving = False                                 # آیا در این فریم حرکت داریم؟
    car_rect.x += (keys[pygame.K_RIGHT]-keys[pygame.K_LEFT]) * car_speed; moving |= keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]
    car_rect.y += (keys[pygame.K_DOWN] -keys[pygame.K_UP])   * car_speed; moving |= keys[pygame.K_DOWN]  or keys[pygame.K_UP]
    car_rect.clamp_ip(scr.get_rect())              # نگه‌داشتن ماشین داخل مرزهای پنجره

    if moving and not pygame.mixer.get_busy(): engine.play(-1) # اگر در حال حرکت و صدایی در حال پخش نیست → پخش موتور (لوپ)
    if not moving and pygame.mixer.get_busy(): engine.stop()   # اگر ایستادیم و صدا در حال پخش است → توقف صدا

    offset = (offset + obs_speed) % (line_h + gap) # حرکت دادن الگوی خط‌چین با سرعت مانع (حس حرکت جاده)
    frame += 1                                     # یک فریم گذشت
    if frame % spawn == 0:                         # هر «spawn» فریم…
        obstacles.append(pygame.Rect(random.randint(0, W - obs_size), -obs_size, obs_size, obs_size))
                                                   # …یک مانع مربع‌شکل در بالای صفحه با x تصادفی بساز
    for r in obstacles:
        r.y += obs_speed                           # پایین آمدن موانع در هر فریم

    scr.fill(GRAY)                                 # پس‌زمینه خاکستری (جاده)
    for y in range(-line_h, H, line_h + gap):      # رسم خط‌چین‌های وسط جاده با فاصله‌ی یکنواخت
        pygame.draw.rect(scr, WHITE, (W//2 - line_w//2, y + offset, line_w, line_h))
    for r in obstacles:
        pygame.draw.rect(scr, BLACK, r)            # رسم هر مانع (مستطیل/مربع سیاه)
        if car_rect.colliderect(r):                # برخورد ماشین با مانع؟
            engine.stop()                          # قطع صدا
            print("Game Over! Score:", score)      # چاپ نتیجه در کنسول
            running = False                        # پایان بازی

    scr.blit(car, car_rect)                        # کشیدن تصویر ماشین
    scr.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))  # نمایش امتیاز
    score += 1                                     # افزایش امتیاز در هر فریم زنده‌ماندن

    pygame.display.flip()                          # نمایش فریم جدید
    clock.tick(30)                                 # قفل کردن FPS روی ۳۰

pygame.quit(); sys.exit()                          # بستن پی‌گیم و خروج تمیز از برنامه
