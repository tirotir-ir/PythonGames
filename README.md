# Ultimate Arcade Car – FINAL

A fast, lightweight lane-dodging racer built with **Pygame**, inspired by _“F1 Racer Game using Pygame”_ (Submitted by **razormist**, Feb 2, 2021) and extended across 10 learning steps. This version adds a settings menu, power-ups, nitro, difficulty ramp, safe audio init, and local top-5 highscores.

---

## 🎮 Gameplay

- Drive left/right to avoid obstacles, collect coins, and survive as the speed ramps up.
    
- Power-ups:
    
    - **Shield**: blocks one crash
        
    - **Magnet**: pulls nearby coins
        
    - **Slow**: slows the world briefly
        
- **Nitro**: hold **Shift** while steering for faster response (uses energy bar).
    

---

## ⌨️ Controls

- **← / →**: steer
    
- **Shift**: nitro boost (consumes bar)
    
- **P**: pause / resume
    
- **Enter / Space**: confirm / start
    
- **Esc**: quit
    

---

## ⚙️ Settings (in-game)

From the **Start Screen**, press **S**:

- Car Size (Small/Med/Large)
    
- Scroll Speed (base world speed)
    
- Steer Speed (turn acceleration)
    
- Difficulty (Easy/Normal/Hard; affects spawn & ramp)
    
- Sound On/Off
    
- Reset Defaults / Back
    

A summary line shows the current configuration.

---

## 📦 Project Structure

```
project/
├─ main.py                # (this file)
├─ assets/                # images & sounds (optional; fallbacks included)
│  ├─ road.png
│  ├─ car.png
│  ├─ obstacle.png
│  ├─ coin.png
│  ├─ car_engine.wav
│  ├─ collision.wav
│  ├─ coin.wav
│  └─ power.wav
└─ save.json             # auto-created high scores
```

> If an asset is missing, the game draws a simple colored fallback and continues.  
> Audio is safely disabled if mixer init fails.

---

## 🚀 Run

**Requirements:** Python 3.8+ and `pygame`

```bash
pip install pygame
python main.py
```

---

## 🧠 Tech Notes

- **Resolution:** 400×600 window
    
- **Highscores:** keeps top 5 in `save.json`
    
- **Performance:** fixed to ~60 FPS; difficulty ramps each 500 score
    
- **Audio:** uses channel 0 for engine loop; safe init guards
    

---

## 🪙 Scoring

- +1 per frame survived
    
- +50 per coin
    
- Top scores shown on Start and Game Over screens
    

---

## 🛠️ Build (optional)

Create a one-file executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller -F -n "UltimateArcadeCar" main.py
```

---

## 📝 Credits & Attribution

- Original tutorial: **razormist — “F1 Racer Game using Pygame” (2021-02-02)**  

- This fork (10-step learning series): **Refactored UI, Settings, Power-ups, Nitro, Difficulty ramp, Safe audio init, Local Highscores.**  
  By **Daryoush Alipour (Tirotir AI / Hoosh Masnooe)**.

© 2025 **Tirotir AI — Hoosh Masnooe** · https://tirotir.ir

    

---

## 📄 License

Educational use.  (MIT) 
