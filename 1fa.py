import pygame                                              # کتابخانه‌ی Pygame برای ساخت بازی‌ها
pygame.init()                                              # راه‌اندازی همهٔ ماژول‌های لازم

s = pygame.display.set_mode((400, 300))                    # ساخت پنجرهٔ 400×300 و گرفتن سطح رسم (Surface)

car = pygame.image.load("car.png").convert_alpha()         # بارگذاری تصویر ماشین و حفظ شفافیت (alpha)
r = car.get_rect(center=(200, 150))                        # مستطیل جایگاه تصویر؛ مرکز را وسط پنجره می‌گذارد

speed, run = 5, True                                       # سرعت حرکت پیکسل/فریم و پرچم اجرای حلقه
while run:                                                 # حلقهٔ اصلی بازی
    for e in pygame.event.get():                           # رسیدگی به رویدادها (بستن پنجره، کیبورد، ماوس و …)
        if e.type == pygame.QUIT: run = False              # اگر پنجره بسته شد، از حلقه خارج شو

    k = pygame.key.get_pressed()                           # وضعیت همهٔ کلیدها (فشرده/غیرفشرده) به صورت آرایهٔ بولی

    r.x += (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * speed  # حرکت افقی: راست=1، چپ=1 → تفاوت‌شان -1/0/1 می‌شود
    r.y += (k[pygame.K_DOWN]  - k[pygame.K_UP])   * speed  # حرکت عمودی: پایین مثبت، بالا منفی با همان منطق

    r.clamp_ip(s.get_rect())                               # محدودکردن جای ماشین به داخل کادر پنجره (in-place)

    s.fill((255,255,255))                                  # پاک‌کردن/پس‌زمینهٔ سفید
    s.blit(car, r)                                         # کشیدن تصویر ماشین در جای r
    pygame.display.flip()                                  # به‌روزرسانی فریم روی صفحه

pygame.quit()                                              # بستن ماژول‌ها و خروج تمیز
