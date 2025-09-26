import pygame, sys, random                      # Pygame برای گرافیک و صدا، sys برای خروج، random برای اعداد تصادفی
pygame.init(); pygame.mixer.init()              # راه‌اندازی ماژول‌های اصلی و صدای Pygame

# --- Window ---
W, H = 400, 600                                 # اندازهٔ پنجره (عرض، ارتفاع)
scr = pygame.display.set_mode((W, H))           # ساخت پنجرهٔ بازی
pygame.display.set_caption("Arcade Car – PNG Lanes")  # عنوان پنجره
clock = pygame.time.Clock()                     # ساعت برای محدود کردن FPS
WHITE, GRAY, BLACK, RED = (255,255,255), (50,50,50), (0,0,0), (255,0,0)  # رنگ‌های پرکاربرد

# --- Assets ---
car = pygame.image.load("car.png").convert_alpha()     # بارگذاری تصویر ماشین با شفافیت
car_rect = car.get_rect(center=(W//2, H-90))           # جای اولیهٔ ماشین: نزدیک پایین، مرکز افقی
engine = pygame.mixer.Sound("car_engine.wav"); engine.set_volume(0.5)  # صدای موتور + بلندی
crash  = pygame.mixer.Sound("collision.wav")           # صدای تصادف
ch = pygame.mixer.Channel(0)                           # یک کانال اختصاصی برای پخش موتور

# --- Lanes & game vars ---
lane_centers = [W//6, W//2, W*5//6]            # مرکز سه لاین جاده (چپ، وسط، راست)
lane = 1                                       # لاین شروع: وسط (ایندکس 1)
slide_speed = 12                               # سرعت سر خوردن ماشین به سمت لاین مقصد
obs_size, obs_speed, spawn = 50, 5, 28         # اندازه مانع، سرعت سقوط، هر چند فریم یک مانع
obstacles, frame, score = [], 0, 0             # لیست موانع، شمارنده فریم، امتیاز
font = pygame.font.SysFont(None, 32)           # فونت متن‌های معمولی
big  = pygame.font.SysFont(None, 56)           # فونت تیترها

def start_screen():                             # صفحهٔ شروع: تا ENTER/SPACE نزنی وارد بازی نمی‌شود
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Arcade Car", True, BLACK), (W//2-110, H//3))
        scr.blit(font.render("Press ENTER to start", True, BLACK), (W//2-120, H//2))
        pygame.display.flip(); clock.tick(60)

def game_over_screen(s):                         # صفحهٔ پایان: امتیاز را نشان می‌دهد و منتظر شروع دوباره می‌ماند
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE): return
        scr.fill(WHITE)
        scr.blit(big.render("Game Over!", True, RED), (W//2-120, H//3))
        scr.blit(font.render(f"Score: {s}", True, BLACK), (W//2-50, H//2))
        scr.blit(font.render("Press ENTER to restart", True, BLACK), (W//2-140, H*2//3))
        pygame.display.flip(); clock.tick(60)

def game_loop():                                 # یک دور بازی: تا تصادف ادامه دارد و امتیاز برمی‌گرداند
    global lane, obstacles, frame, score, obs_speed
    lane, obstacles, frame, score, obs_speed = 1, [], 0, 0, 5   # ریست متغیرها
    car_rect.center = (lane_centers[lane], H-90)                 # بازگرداندن ماشین به لاین وسط
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT  and lane > 0: lane -= 1   # با ← لاین به چپ (اگر ممکن است)
                if e.key == pygame.K_RIGHT and lane < 2: lane += 1   # با → لاین به راست (اگر ممکن است)
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

        # Slide toward target lane center (engine plays while sliding)
        target_x = lane_centers[lane]                 # مختصات x مقصد (مرکز لاین انتخابی)
        dx = target_x - car_rect.centerx              # فاصلهٔ افقی تا مقصد
        moving = abs(dx) > 1                          # آیا هنوز باید حرکت کند؟
        if moving:
            # حرکت نرم به سمت مقصد، با محدود کردن گام به slide_speed
            car_rect.centerx += max(-slide_speed, min(slide_speed, dx))

        # پخش صدای موتور فقط هنگام حرکت بین لاین‌ها
        if moving and not ch.get_busy(): ch.play(engine, loops=-1)
        if not moving and ch.get_busy(): ch.stop()

        # Spawn/move obstacles
        frame += 1
        if frame % spawn == 0:                        # هر N فریم، یک مانع جدید در یکی از لاین‌ها
            r = pygame.Rect(0, 0, obs_size, obs_size)
            r.centerx = random.choice(lane_centers)
            r.y = -obs_size
            obstacles.append(r)
        for r in obstacles: r.y += obs_speed          # سقوط موانع به سمت پایین

        # Draw
        scr.fill(GRAY)                                 # پس‌زمینهٔ خاکستری (جاده)
        pygame.draw.line(scr, WHITE, (W//3, 0), (W//3, H), 5)     # خط لاین چپ/وسط
        pygame.draw.line(scr, WHITE, (2*W//3, 0), (2*W//3, H), 5) # خط لاین وسط/راست
        for r in obstacles:
            pygame.draw.rect(scr, BLACK, r)            # رسم مانع (مربع سیاه)
            if car_rect.colliderect(r):                # برخورد ماشین و مانع؟
                ch.stop(); crash.play()                # قطع موتور و پخش صدای تصادف
                return score                           # پایان این دور و برگرداندن امتیاز

        scr.blit(car, car_rect)                        # کشیدن ماشین
        scr.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))  # نمایش امتیاز
        score += 1                                     # امتیاز زمان‌محور (هر فریم زنده می‌مانی)

        if score % 240 == 0: obs_speed += 0.5          # سخت‌تر شدن تدریجی بازی

        pygame.display.flip()                           # نمایش فریم
        clock.tick(60)                                  # محدود کردن به ۶۰ FPS

while True:                                            # چرخهٔ کلی: شروع → بازی → پایان → تکرار
    start_screen()
    s = game_loop()
    game_over_screen(s)
