import pygame, sys, os                                   # وارد کردن کتابخانه‌های بازی، خروج، و مسیر فایل‌ها

pygame.init()                                            # راه‌اندازی ماژول‌های Pygame
W, H = 400, 300                                          # عرض و ارتفاع پنجره
screen = pygame.display.set_mode((W, H))                 # ساخت پنجره‌ی بازی با اندازه‌ی مشخص
pygame.display.set_caption("Car PNG – Minimal")          # گذاشتن عنوان روی نوار بالای پنجره
clock = pygame.time.Clock()                              # ساخت ساعت برای کنترل نرخ فریم (FPS)

# Load car.png from the script's folder (works no matter where you run it)
car = pygame.image.load(                                 # بارگذاری تصویر ماشین از دیسک
    os.path.join(os.path.dirname(__file__), "car.png")   # مسیرِ فایل کنار همین اسکریپت
).convert_alpha()                                        # تبدیل تصویر با حفظ شفافیت (alpha)
rect = car.get_rect(center=(W//2, H//2))                 # مستطیل جایگاهِ تصویر؛ مرکز در وسط پنجره
speed = 5                                                # سرعت حرکت بر حسب پیکسل در هر فریم

running = True                                           # پرچم اجرای حلقه‌ی اصلی
while running:                                           # حلقه‌ی بازی تا وقتی running=True
    for e in pygame.event.get():                         # خواندن رویدادهای سیستم (کیبورد/ماوس/بستن)
        if e.type == pygame.QUIT or (                    # اگر پنجره بسته شد یا...
            e.type == pygame.KEYDOWN and                 # کلیدی فشرده شد و آن کلید...
            e.key == pygame.K_ESCAPE                     # Escape بود
        ):
            running = False                              # خروج از حلقه

    keys = pygame.key.get_pressed()                      # وضعیت همه‌ی کلیدها به‌صورت آرایه‌ی بولی
    if keys[pygame.K_LEFT]:  rect.x -= speed             # اگر ← فشرده است: حرکت به چپ
    if keys[pygame.K_RIGHT]: rect.x += speed             # اگر → فشرده است: حرکت به راست
    if keys[pygame.K_UP]:    rect.y -= speed             # اگر ↑ فشرده است: حرکت به بالا
    if keys[pygame.K_DOWN]:  rect.y += speed             # اگر ↓ فشرده است: حرکت به پایین
    rect.clamp_ip(screen.get_rect())                     # نگه‌داشتن مستطیل داخل مرزهای پنجره (In-Place)

    screen.fill((255,255,255))                           # پاک کردن صفحه و رنگ پس‌زمینه‌ی سفید
    screen.blit(car, rect)                               # کشیدن تصویرِ ماشین روی صفحه در جای rect
    pygame.display.flip()                                # نمایش فریمِ تازه روی صفحه
    clock.tick(60)                                       # محدود کردن نرخ فریم به 60 FPS

pygame.quit()                                            # بستن ماژول‌های Pygame و آزادسازی منابع
sys.exit()                                               # خروج تمیز از برنامه‌ی پایتون


'''
نکته‌ها:

اگر کد را در محیطی اجرا می‌کنید که __file__ ندارد (مثل بعضی شِل‌ها/نوت‌بوک‌ها)، به‌جای آن می‌توانید از مسیر نسبی ساده "car.png" استفاده کنید یا مسیر کامل بدهید.

rect.clamp_ip تضمین می‌کند تصویر از چارچوب پنجره بیرون نرود.

clock.tick(60) حرکت را یکنواخت و مصرف CPU را کمتر می‌کند.
'''