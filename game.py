import pgzrun
import random
from pygame.display import set_mode
import sys  # Programı kapatmak için sys modülünü ekliyoruz
from pygame import mixer  # Müzik çalma ve ses efektleri için

# Pygame mixer'ı başlat
mixer.init()

WIDTH = 800
HEIGHT = 800
set_mode((WIDTH, HEIGHT))

# Aktörler
background = Actor('background')
hero = Actor('hero', (WIDTH // 2, HEIGHT - 100))
enemies = [Actor('enemy', (random.randint(50, WIDTH - 50), -50)) for _ in range(3)]

# Oyun değişkenleri
hero_speed = 5
enemy_speed = 3
game_over = False
y_velocity = 0
enemy_direction = [random.choice([-1, 1]) for _ in range(3)]

# Menü değişkenleri
in_menu = True  # Başlangıçta menü ekranı aktif
start_button = Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
exit_button = Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

# Müzik ve ses efektleri
music_playing = False  # Başlangıçta müzik çalmıyor
music_button = Rect(20, 20, 120, 40)  # Müzik aç/kapat butonu
collision_sound = mixer.Sound('sounds/explosion.wav')  # Çarpışma sesi

def reset_game():
    global hero, enemies, game_over, y_velocity, enemy_direction
    hero.pos = (WIDTH // 2, HEIGHT - 100)
    y_velocity = 0
    enemies = [Actor('enemy', (random.randint(50, WIDTH - 50), -50)) for _ in range(3)]
    enemy_direction = [random.choice([-1, 1]) for _ in range(3)]
    game_over = False

# Update fonksiyonu
def update():
    global game_over, y_velocity, in_menu

    if in_menu:  # Menü aktifse
        return

    if not game_over:
        # Hareket kontrolleri
        if keyboard.a and hero.x > hero.width // 2:
            hero.x -= hero_speed
        if keyboard.d and hero.x < WIDTH - hero.width // 2:
            hero.x += hero_speed

        y_velocity += 0.5
        hero.y += y_velocity

        if hero.y >= HEIGHT - hero.height // 2:
            hero.y = HEIGHT - hero.height // 2
            y_velocity = 0

        # Zıplama
        if keyboard.w and hero.y == HEIGHT - hero.height // 2:
            y_velocity = -15

        for i, enemy in enumerate(enemies):
            # Düşman hareketleri
            enemy.y += enemy_speed
            enemy.x += enemy_direction[i] * 3

            if enemy.x <= enemy.width // 2 or enemy.x >= WIDTH - enemy.width // 2:
                enemy_direction[i] *= -1

            if enemy.y > HEIGHT:
                enemy.y = -enemy.height
                enemy.x = random.randint(enemy.width // 2, WIDTH - enemy.width // 2)

            if hero.colliderect(enemy):
                game_over = True
                collision_sound.play()  # Çarpışma sesini çal
    else:
        if keyboard.space:
            reset_game()

# Mouse tıklama olayı
def on_mouse_down(pos):
    global in_menu, music_playing

    if in_menu:
        if start_button.collidepoint(pos):
            in_menu = False  # Oyunu başlat
        elif exit_button.collidepoint(pos):
            sys.exit()  # Oyunu kapat

    # Müzik aç/kapat kontrolü
    if music_button.collidepoint(pos):
        if music_playing:
            mixer.music.stop()
        else:
            mixer.music.load('sounds/background_music.ogg')  # Arka plan müziği dosyasını yükle
            mixer.music.play(-1)  # Sonsuz döngüde çal
        music_playing = not music_playing

# Çizim fonksiyonu
def draw():
    if in_menu:
        screen.clear()
        screen.draw.text("Hoş Geldiniz!", center=(WIDTH // 2, HEIGHT // 2 - 120), fontsize=60, color="white")
        screen.draw.filled_rect(start_button, "green")
        screen.draw.text("Başla", center=start_button.center, fontsize=40, color="white")
        screen.draw.filled_rect(exit_button, "red")
        screen.draw.text("Çıkış", center=exit_button.center, fontsize=40, color="white")
    elif game_over:
        screen.clear()
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        screen.draw.text("Press SPACE to Restart", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")
    else:
        background.draw()
        hero.draw()
        for enemy in enemies:
            enemy.draw()

        # Müzik butonunu çiz
        screen.draw.filled_rect(music_button, "blue" if music_playing else "gray")
        screen.draw.text("Müzik" if music_playing else "Sessiz", center=music_button.center, fontsize=20, color="white")

pgzrun.go()
