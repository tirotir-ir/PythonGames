import pygame, sys                                  # کتابخانه‌ Pygame و ماژول خروج از برنامه

pygame.init()                                       # راه‌اندازی همهٔ ماژول‌های اصلی پی‌گیم
pygame.mixer.init()                                 # راه‌اندازی موتور صدا (Mixer) برای پخش wav/mp3

W, H = 400, 300                                     # عرض و ارتفاع پنجره
screen = pygame.display.set_mode((W, H))            # ساخت پنجرهٔ بازی با اندازهٔ مشخص
clock = pygame.time.Clock()                         # ساعت برای محدود کردن FPS و روانی حرکت

car = pygame.image.load("car.png").convert_alpha()  # بارگذاری تصویر و حفظ شفافیت (alpha)
rect = car.get_rect(center=(W//2, H//2))            # مستطیل جایگاه تصویر؛ مرکز در وسط پنجره
engine = pygame.mixer.Sound("car_engine.wav")       # بارگذاری صدای موتور ماشین
ch = pygame.mixer.Channel(0)                        # انتخاب یک کانال پخش اختصاصی (کانال شمارهٔ 0)
speed = 5                                           # سرعت حرکت بر حسب پیکسل در هر فریم

running = True                                      # پرچم اجرای حلقهٔ اصلی
while running:                                      # حلقهٔ بازی
    for e in pygame.event.get():                    # رسیدگی به رویدادها (بستن پنجره/کیبورد/ماوس)
        if e.type == pygame.QUIT or (               # اگر کاربر پنجره را بست یا
            e.type == pygame.KEYDOWN and            # اگر کلیدی فشرده شد و آن کلید
            e.key == pygame.K_ESCAPE                # Escape بود
        ):
            running = False                         # حلقه تمام شود

    keys = pygame.key.get_pressed()                 # وضعیت همهٔ کلیدها (بولی)
    moving = False                                  # آیا ماشین در این فریم حرکت کرده؟
    if keys[pygame.K_LEFT]:  rect.x -= speed; moving = True   # حرکت به چپ
    if keys[pygame.K_RIGHT]: rect.x += speed; moving = True   # حرکت به راست
    if keys[pygame.K_UP]:    rect.y -= speed; moving = True   # حرکت به بالا
    if keys[pygame.K_DOWN]:  rect.y += speed; moving = True   # حرکت به پایین
    rect.clamp_ip(screen.get_rect())                # نگه‌داشتن تصویر داخل مرزهای پنجره

    if moving and not ch.get_busy():                # اگر حرکت می‌کنیم و صدا پخش نمی‌شود
        ch.play(engine, loops=-1)                   # پخش پیوسته (لوپ بی‌نهایت) صدای موتور
    if not moving and ch.get_busy():                # اگر توقف کردیم و صدا هنوز در حال پخش است
        ch.stop()                                   # قطع صدا

    screen.fill((255, 255, 255))                    # پاک کردن صفحه با پس‌زمینهٔ سفید
    screen.blit(car, rect)                          # کشیدن تصویر ماشین در جای rect
    pygame.display.flip()                           # نمایش فریمِ جدید
    clock.tick(60)                                  # محدود کردن نرخ فریم به 60 (حرکت روان)

pygame.quit()                                       # بستن ماژول‌های پی‌گیم
sys.exit()                                          # خروج تمیز از برنامهٔ پایتون


'''
نکته‌های کوچک:

فایل‌های car.png و car_engine.wav باید کنار اسکریپت باشند یا مسیر درست بدهید.

می‌توانید بلندی صدا را کنترل کنید: engine.set_volume(0.4) (بین 0 تا 1).

اگر قطع و وصل صدا «تق‌تق» دارد، به‌جای stop() از محو کردن استفاده کنید: ch.fadeout(150) و برای شروع: ch.play(engine, loops=-1, fade_ms=150).
'''