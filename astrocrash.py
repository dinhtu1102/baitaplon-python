import pygame
import random
import math
import os

# Khởi tạo Pygame
pygame.init()

# Màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astrocrash")

# Load ảnh
IMG_PATH = os.path.join("assets", "images")
SND_PATH = os.path.join("assets", "sounds")

ship_img = pygame.image.load(os.path.join(IMG_PATH, "ship.png"))
missile_img = pygame.image.load(os.path.join(IMG_PATH, "missile.png"))
asteroid_img = pygame.image.load(os.path.join(IMG_PATH, "asteroid.png"))
explosion_img = pygame.image.load(os.path.join(IMG_PATH, "explosion.png"))

# Âm thanh
pygame.mixer.music.load(os.path.join(SND_PATH, "background.mp3"))
shoot_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "shoot.wav"))
boom_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "boom.wav"))
pygame.mixer.music.play(-1)

# Clock và font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Lớp tàu
class Ship:
    def __init__(self):
        self.image = ship_img
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = 5
        self.health = 5

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.x = max(0, min(WIDTH - self.image.get_width(), self.x))
        self.y = max(0, min(HEIGHT - self.image.get_height(), self.y))

# Lớp tên lửa
class Missile:
    def __init__(self, x, y):
        self.image = missile_img
        self.x = x
        self.y = y
        self.dy = -10

    def update(self):
        self.y += self.dy

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Lớp thiên thạch
class Asteroid:
    def __init__(self):
        self.image = asteroid_img
        self.x = random.randint(0, WIDTH - 50)
        self.y = -50
        self.dy = random.uniform(1, 4)

    def update(self):
        self.y += self.dy
        if self.y > HEIGHT:
            self.__init__()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Lớp hiệu ứng nổ
class Explosion:
    def __init__(self, x, y):
        self.image = explosion_img
        self.x = x
        self.y = y
        self.timer = 20

    def update(self):
        self.timer -= 1

    def draw(self):
        screen.blit(self.image, (self.x - 32, self.y - 32))

# Màn hình bắt đầu

def show_start_screen():
    screen.fill((0, 0, 20))
    title = font.render("Bấm phím bất kỳ để bắt đầu", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Game loop

def game_loop():
    ship = Ship()
    missiles = []
    asteroids = [Asteroid() for _ in range(5)]
    explosions = []
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(60)
        screen.fill((0, 0, 20))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shoot_sound.play()
                missiles.append(Missile(ship.x + ship.image.get_width() // 2 - 5, ship.y))

        if not game_over:
            ship.update(keys)
            ship.draw()

            for m in missiles[:]:
                m.update()
                m.draw()
                if m.y < 0:
                    missiles.remove(m)

            for a in asteroids[:]:
                a.update()
                a.draw()
                for m in missiles[:]:
                    dist = math.hypot(a.x - m.x, a.y - m.y)
                    if dist < 32:
                        boom_sound.play()
                        explosions.append(Explosion(a.x, a.y))
                        missiles.remove(m)
                        asteroids.remove(a)
                        asteroids.append(Asteroid())
                        score += 10
                        break
                # Va chạm với tàu
                if abs(a.x - ship.x) < 40 and abs(a.y - ship.y) < 40:
                    ship.health -= 1
                    asteroids.remove(a)
                    asteroids.append(Asteroid())
                    if ship.health <= 0:
                        game_over = True

            for e in explosions[:]:
                e.update()
                e.draw()
                if e.timer <= 0:
                    explosions.remove(e)

            # Hiển thị điểm và máu
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            health_text = font.render(f"Health: {ship.health}", True, (255, 0, 0))
            screen.blit(score_text, (10, 10))
            screen.blit(health_text, (10, 40))

            # Thắng game
            if score >= 200:
                win_text = font.render("Bạn đã chiến thắng! Bấm ENTER để chơi lại", True, (0, 255, 0))
                screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
                game_over = True

        else:
            over_text = font.render("Game Over! ENTER để chơi lại, ESC để thoát", True, (255, 255, 255))
            screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
            if keys[pygame.K_RETURN]:
                return True
            if keys[pygame.K_ESCAPE]:
                return False

        pygame.display.flip()

# Chạy chương trình
while True:
    show_start_screen()
    play = game_loop()
    if not play:
        break

pygame.quit()
