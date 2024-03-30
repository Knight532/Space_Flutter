import os
import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

HEIGHT = 800
WIDTH = 1200

pygame.init()

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load('images/background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3
score = 0
font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self, health):
        super().__init__()
        self.health = health
        self.image = pygame.transform.scale(pygame.image.load('images/player/player.png').convert_alpha(), (125, 75))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 15
        self.rect.centery = HEIGHT // 2

    def update(self, keys):
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect = self.rect.move(0, 4)
        if keys[K_UP] and self.rect.top > 0:
            self.rect = self.rect.move(0, -4)
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect = self.rect.move(-4, 0)
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect = self.rect.move(4, 0)

    @staticmethod
    def draw_health_bar_player(surface, health):
        bar_length = 200
        bar_height = 20
        health_bar = pygame.Rect(10, 10, bar_length, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), health_bar)
        current_health = max(health, 0)
        bar_width = int(bar_length * current_health / 100)
        health_bar.width = bar_width
        pygame.draw.rect(surface, (0, 255, 0), health_bar)

class EnemyAsteroid(pygame.sprite.Sprite):
    def __init__(self, health, attack):
        super().__init__()
        self.health = health
        self.attack = attack
        self.images = [
            pygame.transform.scale(pygame.image.load('images/enemy/asteroid/asteroid-1.png').convert_alpha(), (50, 50)),
            pygame.transform.scale(pygame.image.load('images/enemy/asteroid/asteroid-2.png').convert_alpha(), (50, 50)),
            pygame.transform.scale(pygame.image.load('images/enemy/asteroid/asteroid-3.png').convert_alpha(), (50, 50)),
            pygame.transform.scale(pygame.image.load('images/enemy/asteroid/asteroid-4.png').convert_alpha(), (50, 50)),
            pygame.transform.scale(pygame.image.load('images/enemy/asteroid/asteroid-5.png').convert_alpha(), (50, 50)),
            pygame.transform.scale(pygame.image.load('images/enemy/asteroid/asteroid-6.png').convert_alpha(), (50, 50)),
            pygame.transform.scale(pygame.image.load('images/enemy/asteroid/asteroid-7.png').convert_alpha(), (50, 50)),
            pygame.transform.scale(pygame.image.load('images/enemy/asteroid/asteroid-8.png').convert_alpha(), (50, 50))
]
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.right = random.randint(WIDTH, WIDTH + 200)
        self.rect.top = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, explosion_images):
        super().__init__()
        self.explosion_images = explosion_images
        self.image = self.explosion_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_images):
                self.kill()
            else:
                self.image = self.explosion_images[self.frame]
                self.rect = self.image.get_rect(center=self.rect.center)

explosion_images = [
    pygame.transform.scale(pygame.image.load('images/enemy/animation/explosion-1.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('images/enemy/animation/explosion-2.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('images/enemy/animation/explosion-3.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('images/enemy/animation/explosion-4.png').convert_alpha(), (50, 50)),
]

class Bonus_hp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.transform.scale(pygame.image.load('images/bonuses/hp.png').convert_alpha(), (50, 50)),
        ]
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(WIDTH, WIDTH + 200)
        self.rect.top = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

bonus_timer = 0
bonus_interval = pygame.time.get_ticks() + random.randint(3000, 5000)

pygame.init()

FPS = pygame.time.Clock()

player = Player(100)
asteroid = EnemyAsteroid(50, 20)
bonus_hp = Bonus_hp()

MAX_ENEMIES = 10
MIN_ENEMIES = 5

enemies = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
explosions = pygame.sprite.Group()

playing = True

while playing:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()
    player.update(keys)
    main_display.blit(player.image, player.rect)

    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            player.health -= enemy.attack
            score += 10
            enemy.kill()
            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, explosion_images)
            explosions.add(explosion)

    explosions.update()
    explosions.draw(main_display)

    for bonus in bonuses:
        bonus.update()
        main_display.blit(bonus.image, bonus.rect)
        if pygame.sprite.collide_rect(player, bonus):
            player.health += 10
            if player.health > 100:
                player.health = 100
            bonus.kill()

    enemies.update()
    enemies.draw(main_display)

    if len(enemies) < MIN_ENEMIES:
        while len(enemies) < MIN_ENEMIES:
            enemy = EnemyAsteroid(50, 25)
            enemies.add(enemy)
    elif len(enemies) < MAX_ENEMIES:
        while len(enemies) < MAX_ENEMIES:
            enemy = EnemyAsteroid(50, 25)
            enemies.add(enemy)

    bonus_timer += FPS.get_rawtime()
    if bonus_timer >= bonus_interval:
        bonus = Bonus_hp()
        bonuses.add(bonus)
        bonus_timer = 0
        bonus_interval = pygame.time.get_ticks() + random.randint(3000, 5000)

    
   
    Player.draw_health_bar_player(main_display, player.health)
    pygame.display.flip()
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))  # Отримуємо текст
    score_rect = score_text.get_rect(centerx=WIDTH // 2, top=10)  # Отримуємо прямокутник тексту
    main_display.blit(score_text, score_rect)  # Відображаємо текст за допомогою прямокутника
        

pygame.quit()
