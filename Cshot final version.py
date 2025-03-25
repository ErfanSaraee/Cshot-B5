import pygame
import random
import time
import math
from abc import ABC, abstractmethod
import sqlite3
import tkinter as tk
from tkinter import messagebox

# دیتابیس رو راه می‌ندازیم برای ذخیره اطلاعات بازیکنا
conn = sqlite3.connect('players.db')
c = conn.cursor()

# جدول بازیکنا رو می‌سازیم، فقط اسم و یه آیدی ساده
c.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

# جدول امتیازات، با اسم و جزئیات برد و باخت و اینا
c.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        draws INTEGER DEFAULT 0
    )
''')
conn.commit()

# اینجا pygame رو راه می‌ندازیم، آماده بازی بشیم
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("bluetarget.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Cshot")

# یه چندتا رنگ ساده تعریف کردیم
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)

# صدا و تصویر رو بارگذاری می‌کنیم
pygame.mixer.init()
background_sound = pygame.mixer.Sound("background.mp3")
shoot_sound = pygame.mixer.Sound("reload.mp3")
hit_sound = pygame.mixer.Sound("headshot.mp3")
blood_image = pygame.image.load("blood.png")
blood_image = pygame.transform.scale(blood_image, (30, 30))

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Aim(Drawable):
    def __init__(self, controls, bullet_color, name):
        self._x = random.randint(100, WIDTH - 100)
        self._y = random.randint(100, HEIGHT - 100)
        self._color = WHITE
        self._bullets = 15  # هر بازیکن 15 تا گلوله داره شروع بازی
        self._score = 0
        self._controls = controls
        self._bullet_color = bullet_color
        self._time_left = 60  # 60 ثانیه وقت داری، عجله کن!
        self._last_shot_time = time.time()
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def x(self): return self._x
    @property
    def y(self): return self._y
    @property
    def color(self): return self._color
    @property
    def bullets(self): return self._bullets
    @bullets.setter
    def bullets(self, value): self._bullets = max(0, value)
    @property
    def score(self): return self._score
    @score.setter
    def score(self, value): self._score = max(0, value)
    @property
    def time_left(self): return self._time_left
    @time_left.setter
    def time_left(self, value): self._time_left = max(0, value)

    def move(self, keys):
        # حرکت با کلیدای مشخص شده، مثلاً A و D و اینا
        if keys[self._controls["left"]]: self._x = max(0, self._x - 5)
        if keys[self._controls["right"]]: self._x = min(WIDTH, self._x + 5)
        if keys[self._controls["up"]]: self._y = max(0, self._y - 5)
        if keys[self._controls["down"]]: self._y = min(HEIGHT, self._y + 5)

    def shoot(self):
        current_time = time.time()
        # شلیک فقط اگه گلوله داشته باشی و 0.5 ثانیه گذشته باشه
        if self._bullets > 0 and current_time - self._last_shot_time >= 0.5 and self._time_left > 0:
            self._bullets -= 1
            bullets.append(Bullet(self._x, self._y, self._bullet_color))
            self._last_shot_time = current_time
            shoot_sound.play()

    def draw(self):
        pygame.draw.circle(screen, self._color, (self._x, self._y), 5)

    def update_time(self):
        if self._time_left > 0:
            self._time_left -= 1 / 30  # هر فریم یه کم از وقت کم میشه

    @property
    def controls(self):
        return self._controls

class Bullet(Drawable):
    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self): return self._x
    @property
    def y(self): return self._y
    @property
    def color(self): return self._color

    def draw(self):
        pygame.draw.circle(screen, self._color, (self._x, self._y), 5)

class Target(Drawable):
    def __init__(self):
        self._x = random.randint(0, WIDTH - 30)
        self._y = random.randint(100, HEIGHT - 30)
        self._hit_time = None
        try:
            self._image = pygame.image.load("redtarget.png")
            self._image = pygame.transform.scale(self._image, (30, 30))
        except pygame.error:
            self._image = None  # اگه عکس نبود، بی‌خیال میشیم

    @property
    def x(self): return self._x
    @property
    def y(self): return self._y

    def draw(self):
        if self._image:
            screen.blit(self._image, (self._x, self._y))
        if self._hit_time:
            current_time = pygame.time.get_ticks()
            if current_time - self._hit_time <= 2000:  # خون 2 ثانیه نشون داده میشه
                screen.blit(blood_image, (self._x - 10, self._y - 10))

    def hit_target(self):
        self._hit_time = pygame.time.get_ticks()

def update_score(player_name, score, result):
    # امتیازات رو آپدیت می‌کنیم تو دیتابیس
    c.execute("SELECT score, wins, losses, draws FROM scores WHERE name=?", (player_name,))
    result_data = c.fetchone()
    
    if result_data:
        new_score = result_data[0] + score
        wins = result_data[1] + (1 if result == 'win' else 0)
        losses = result_data[2] + (1 if result == 'loss' else 0)
        draws = result_data[3] + (1 if result == 'draw' else 0)
        c.execute("UPDATE scores SET score=?, wins=?, losses=?, draws=? WHERE name=?",
                  (new_score, wins, losses, draws, player_name))
    else:
        wins = 1 if result == 'win' else 0
        losses = 1 if result == 'loss' else 0
        draws = 1 if result == 'draw' else 0
        c.execute("INSERT INTO scores (name, score, wins, losses, draws) VALUES (?, ?, ?, ?, ?)",
                  (player_name, score, wins, losses, draws))
    conn.commit()

def show_leaderboard():
    # لیدربورد رو نشون میدیم، ببین کی بالاتره!
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("600x400")
    leaderboard_window.config(bg="#2E4053")

    c.execute("SELECT name, score, wins, losses, draws FROM scores ORDER BY score DESC")
    scores = c.fetchall()

    tk.Label(leaderboard_window, text="🏆 Leaderboard 🏆", font=("Arial", 24, "bold"), fg="#F4D03F", bg="#2E4053").pack(pady=20)
    frame = tk.Frame(leaderboard_window, bg="#2E4053")
    frame.pack()

    header_labels = ["Rank", "Name", "Score", "Wins", "Losses", "Draws"]
    for col, text in enumerate(header_labels):
        tk.Label(frame, text=text, font=("Arial", 12, "bold"), fg="#FDFEFE", bg="#34495E", padx=10, pady=5, width=10).grid(row=0, column=col)

    for idx, (name, score, wins, losses, draws) in enumerate(scores, start=1):
        data = [idx, name, score, wins, losses, draws]
        for col, value in enumerate(data):
            tk.Label(frame, text=str(value), font=("Arial", 12), fg="#FDFEFE", bg="#2E4053", padx=10, pady=5, width=10).grid(row=idx, column=col)

def run_game(player1_name, player2_name):
    global bullets, targets
    # دو تا بازیکن می‌سازیم با کنترلای مختلف
    player1 = Aim({"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "shoot": pygame.K_SPACE}, CYAN, player1_name)
    player2 = Aim({"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN, "shoot": pygame.K_RETURN}, MAGENTA, player2_name)

    bullets = []
    targets = [Target() for _ in range(3)]  # 3 تا هدف می‌ذاریم تو بازی
    clock = pygame.time.Clock()
    running = True
    background_sound.play()

    while running:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()

        # اگه وقت یا گلوله تموم بشه، بازی تمومه
        if (player1.time_left <= 0 and player2.time_left <= 0) or (player1.bullets <= 0 and player2.bullets <= 0) or \
           (player1.time_left <= 0 and player2.bullets <= 0) or (player2.time_left <= 0 and player1.bullets <= 0):
            winner_text = "Equal!"
            result1, result2 = "draw", "draw"
            if player1.score > player2.score:
                winner_text = f"{player1_name} Wins!"
                result1, result2 = "win", "loss"
            elif player2.score > player1.score:
                winner_text = f"{player2_name} Wins!"
                result1, result2 = "loss", "win"

            update_score(player1_name, player1.score, result1)
            update_score(player2_name, player2.score, result2)

            end_text = pygame.font.Font(None, 60).render(winner_text, True, GREEN)
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            break

        player1.move(keys)
        player2.move(keys)

        if keys[player1.controls["shoot"]]: player1.shoot()
        if keys[player2.controls["shoot"]]: player2.shoot()

        for bullet in bullets[:]:
            bullet.draw()
            for target in targets[:]:
                if target.x < bullet.x < target.x + 30 and target.y < bullet.y < target.y + 30:
                    bullets.remove(bullet)
                    target.hit_target()
                    target.draw()
                    targets.remove(target)
                    targets.append(Target())
                    hit_sound.play()

                    # یه جایزه تصادفی میدیم به بازیکن
                    distance = math.sqrt(((bullet.x - target.x) ** 2 + (bullet.y - target.y) ** 2) ** 0.5)
                    bonus = int(distance / 10)
                    result = random.choice(["score", "time", "bullets"])
                    player = player1 if bullet.color == CYAN else player2

                    if result == "score": player.score += 1 + bonus
                    elif result == "time": player.time_left += 5 + bonus
                    elif result == "bullets": player.bullets += 3 + bonus

        player1.draw()
        player2.draw()
        for target in targets: target.draw()

        # امتیاز و گلوله‌ها رو نشون میدیم
        score_text = pygame.font.Font(None, 30).render(
            f"{player1_name} Score: {player1.score}  Bullets: {player1.bullets} | {player2_name} Score: {player2.score}  Bullets: {player2.bullets}",
            True, BLACK
        )
        screen.blit(score_text, (20, 20))

        time_text1 = pygame.font.Font(None, 30).render(f"{player1_name} Time: {int(player1.time_left)}", True, BLACK)
        screen.blit(time_text1, (20, 50))
        time_text2 = pygame.font.Font(None, 30).render(f"| {player2_name} Time: {int(player2.time_left)}", True, BLACK)
        screen.blit(time_text2, (WIDTH - 493, 50))

        player1.update_time()
        player2.update_time()

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

def register_players(entry_player1, entry_player2):
    # ثبت‌نام بازیکنا، فقط چک می‌کنیم خالی نباشه
    player1_name = entry_player1.get().strip()
    player2_name = entry_player2.get().strip()

    if not player1_name or not player2_name:
        messagebox.showerror("Error", "Please enter player usernames.")
    else:
        c.execute("INSERT OR IGNORE INTO players (name) VALUES (?)", (player1_name,))
        c.execute("INSERT OR IGNORE INTO players (name) VALUES (?)", (player2_name,))
        conn.commit()
        messagebox.showinfo("Successful", "Players registered successfully. Go to login.")
        entry_player1.delete(0, tk.END)
        entry_player2.delete(0, tk.END)
        open_login_window()

def open_login_window():
    # پنجره لاگین رو باز می‌کنیم
    for widget in frame.winfo_children():
        widget.destroy()

    root.title("Login to Game")
    tk.Label(frame, text="Player 1 Username:", font=("Arial", 12), fg="#1C2833", bg="#D5DBDB").grid(row=0, column=0, pady=10, padx=10)
    entry_player1 = tk.Entry(frame, font=("Arial", 12))
    entry_player1.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame, text="Player 2 Username:", font=("Arial", 12), fg="#1C2833", bg="#D5DBDB").grid(row=1, column=0, pady=10, padx=10)
    entry_player2 = tk.Entry(frame, font=("Arial", 12))
    entry_player2.grid(row=1, column=1, pady=10, padx=10)

    tk.Button(frame, text="Login", command=lambda: login_players(entry_player1.get().strip(), entry_player2.get().strip()), font=("Arial", 12), bg="#2ECC71", fg="white", padx=20).grid(row=2, column=0, columnspan=2, pady=20)

def login_players(player1_name, player2_name):
    # لاگین کردن، چک می‌کنیم که اسم‌ها تو دیتابیس باشن
    if not player1_name or not player2_name:
        messagebox.showerror("Error", "Both usernames are required!")
        return
    
    c.execute("SELECT name FROM players WHERE name=?", (player1_name,))
    player1_exists = c.fetchone()
    c.execute("SELECT name FROM players WHERE name=?", (player2_name,))
    player2_exists = c.fetchone()

    if player1_exists and player2_exists:
        messagebox.showinfo("Login", "Login successful!")
        root.destroy()
        run_game(player1_name, player2_name)
    else:
        messagebox.showerror("Error", "One or both usernames do not exist. Please try again.")

# منوی اصلی بازی با tkinter
root = tk.Tk()
root.title("Game Menu")
root.geometry("450x350")
root.config(bg="#D5DBDB")
root.eval('tk::PlaceWindow . center')

frame = tk.Frame(root, bg="#D5DBDB")
frame.pack(padx=20, pady=20)

tk.Label(frame, text="Player 1 Username:", font=("Arial", 12), fg="#1C2833", bg="#D5DBDB").grid(row=0, column=0, pady=10, padx=10)
entry_player1 = tk.Entry(frame, font=("Arial", 12))
entry_player1.grid(row=0, column=1, pady=10, padx=10)

tk.Label(frame, text="Player 2 Username:", font=("Arial", 12), fg="#1C2833", bg="#D5DBDB").grid(row=1, column=0, pady=10, padx=10)
entry_player2 = tk.Entry(frame, font=("Arial", 12))
entry_player2.grid(row=1, column=1, pady=10, padx=10)

tk.Button(frame, text="Sign In", command=lambda: register_players(entry_player1, entry_player2), font=("Arial", 12), bg="#3498DB", fg="white", padx=20).grid(row=2, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Show Leaderboard", command=show_leaderboard, font=("Arial", 12), bg="#F39C12", fg="white", padx=20).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Login", command=open_login_window, font=("Arial", 12), bg="#27AE60", fg="white", padx=20).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
conn.close()  # دیتابیس رو می‌بندیم
