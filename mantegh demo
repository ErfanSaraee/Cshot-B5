import pygame
import random
import time
import math


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("bluetarget.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Cshot")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)

pygame.mixer.init()
background_sound = pygame.mixer.Sound("background.mp3")
shoot_sound = pygame.mixer.Sound("reload.mp3")
hit_sound = pygame.mixer.Sound("headshot.mp3")

blood_image = pygame.image.load("blood.png")
blood_image = pygame.transform.scale(blood_image, (30, 30))

class Aim:
    def __init__(self, controls, bullet_color):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.color = WHITE
        self.bullets = 20
        self.score = 0
        self.controls = controls
        self.bullet_color = bullet_color
        self.time_left = 60
        self.last_shot_time = time.time()
        self.can_shoot = True

    def move(self, keys):
        if keys[self.controls["left"]]: self.x = max(0, self.x - 5)
        if keys[self.controls["right"]]: self.x = min(WIDTH, self.x + 5)
        if keys[self.controls["up"]]: self.y = max(0, self.y - 5)
        if keys[self.controls["down"]]: self.y = min(HEIGHT, self.y + 5)

    def shoot(self):
        current_time = time.time()
        if self.bullets > 0 and current_time - self.last_shot_time >= 0.5 and self.time_left > 0:
            self.bullets -= 1
            bullets.append(Bullet(self.x, self.y, self.bullet_color))
            self.last_shot_time = current_time
            shoot_sound.play()

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 8)

    def update_time(self):
        if self.time_left > 0:
            self.time_left -= 1 / 30

class Bullet:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)

class Target:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        try:
            self.image = pygame.image.load("redtarget.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
        except pygame.error:
            self.image = None
        self.hit_time = None

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
    
        if self.hit_time:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time <= 2000:
                screen.blit(blood_image, (self.x - 10, self.y - 10))
    def hit_target(self):
        self.hit_time = pygame.time.get_ticks()
        


player1 = Aim({"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "shoot": pygame.K_SPACE}, CYAN)
player2 = Aim({"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN, "shoot": pygame.K_RETURN}, MAGENTA)

bullets = []
targets = [Target() for _ in range(3)]
clock = pygame.time.Clock()
running = True
background_sound.play()


while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    if (player1.time_left <= 0 and player2.time_left <= 0) or (player1.bullets <= 0 and player2.bullets <= 0) or \
        (player1.time_left <= 0 and player2.bullets <= 0) or (player2.time_left <= 0 and player1.bullets <= 0):
        winner_text = "Equal!"
        if player1.score > player2.score:
            winner_text = "Player 1 Wins!"
        elif player2.score > player1.score:
            winner_text = "Player 2 Wins!"

        end_text = pygame.font.Font(None, 60).render(winner_text, True, GREEN)
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        break

    player1.move(keys)
    player2.move(keys)

    if keys[player1.controls["shoot"]]:
        player1.shoot()
    if keys[player2.controls["shoot"]]:
        player2.shoot()

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

                if bullets:
                    distance = math.sqrt(((bullets[-1].x - target.x) ** 2 + (bullets[-1].y - target.y) ** 2)**0.5)
                    bonus = int(distance / 10)

                    result = random.choice(["score", "time", "bullets"])

                    if result == "score":
                        if bullet.color == CYAN:
                            player1.score += 1 + bonus
                        else:
                            player2.score += 1 + bonus
                    elif result == "time":
                        if bullet.color == CYAN:
                            player1.time_left += 5 + bonus
                        else:
                            player2.time_left += 5 + bonus
                    elif result == "bullets":
                        if bullet.color == CYAN:
                            player1.bullets += 3 + bonus
                        else:
                            player2.bullets += 3 + bonus


                result = random.choice(["score", "time", "bullets"])

                if result == "score":
                    if bullet.color == CYAN:
                        player1.score += 1
                    else:
                        player2.score += 1
                elif result == "time":
                    if bullet.color == CYAN:
                        player1.time_left += 5
                    else:
                        player2.time_left += 5
                elif result == "bullets":
                    if bullet.color == CYAN:
                        player1.bullets += 3
                    else:
                        player2.bullets += 3


    player1.draw()
    player2.draw()
    for target in targets:
        target.draw()

    score_text = pygame.font.Font(None, 30).render(
        f"Player 1 Score: {player1.score}  Bullets: {player1.bullets} | Player 2 Score: {player2.score}  Bullets: {player2.bullets}",
        True, BLACK
    )
    screen.blit(score_text, (20, 20))

    time_text1 = pygame.font.Font(None, 30).render(
        f"Player 1 Time: {int(player1.time_left)}", True, BLACK
    )
    screen.blit(time_text1, (20, 50))

    time_text2 = pygame.font.Font(None, 30).render(
        f"Player 2 Time: {int(player2.time_left)}", True, BLACK
    )
    screen.blit(time_text2, (WIDTH - 480, 50))

    player1.update_time()
    player2.update_time()

    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
