import pygame
import sys
from pygame.locals import *
from pygame.time import Clock
from random import choice

check_errors = pygame.init()
if check_errors[1] > 0:
    print('[!] {check_errors} game macam tra bisa jalan kah')
else:
    print('[+] game bisa jalan sayang')

lebar = 480
tinggi = 600
FPS = 30
putih = ((255, 255, 255))
hitam = ((0, 0, 0))
merah = ((255, 0, 0))
hijau = ((0, 255, 0))
biru = ((0, 0, 255))

logo = pygame.image.load("burung.png")
pygame.display.set_icon(logo)

pygame.init()
screen = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption('Burung tabrak-tabrak')
jam = pygame.time.Clock()

gravitasi = 0
nilai = 0
pos_list = [[-300, 350], [-400, 250], [-200, 450], [-450, 150], [-50, 550]]


def create_pipa():
    y_pos = choice(pos_list)
    p1 = TOP(y_pos[0])
    p2 = Bottom(y_pos[1])
    detection = Detectionpoint(p2.rect.x, y_pos[1])
    pipas.add(p1)
    pipas.add(p2)
    all_sprites.add(p1)
    all_sprites.add(p2)
    detect_group.add(detection)
    all_sprites.add(detection)


def show_text(text, font_size, font_color, x, y):
    font = pygame.font.SysFont(None, font_size)
    font_surface = font.render(text, True, font_color)
    screen.blit(font_surface, (x, y))


def game_over_screen():
    screen.fill(hitam)
    show_text("KO Mampus", 40, merah, lebar//2 - 65, tinggi//4)
    show_text("Ko Pu Nilai Selama Main Nih : {}".format(
        nilai), 25, putih, lebar//2 - 80, tinggi//4 + 100)
    show_text("ko tekan tombol apa saja untuk lanjut",
              25, putih, lebar//2 - 95, tinggi//4 + 50)
    pygame.display.flip()
    waiting_game_over = True
    while waiting_game_over:
        # Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == quit:
                sys.exit()
            if event.type == KEYUP:
                waiting_game_over = False


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(merah)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = lebar // 2

    def update(self):
        global game_over
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y > tinggi:
            game_over = True
            selesai_sound.play()


class pipa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 500))
        self.image.fill(hijau)
        self.rect = self.image.get_rect()
        self.rect.x = lebar + 10

    def update(self):
        self.rect.x -= 4
        if self.rect.x < -20:
            self.kill()


class TOP(pipa):
    def __init__(self, y):
        super().__init__()
        self.rect.y = y


class Bottom(pipa):
    def __init__(self, y):
        super().__init__()
        self.rect.y = y


class Detectionpoint(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 120))
        self.image.set_colorkey(hitam)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.hit = False

    def update(self):
        self.rect.x -= 4
        if self.rect.x < -20:
            self.kill()


score_sound = pygame.mixer.Sound('mixkit-unlock-game-notification-253.wav')
selesai_sound = pygame.mixer.Sound('mixkit-sad-game-over-trombone-471.wav')


all_sprites = pygame.sprite.Group()
pipas = pygame.sprite.Group()
detect_group = pygame.sprite.Group()
Player = player()

create_pipa()

all_sprites.add(Player)

game_over = False


while True:
    if game_over:
        game_over_screen()
        all_sprites = pygame.sprite.Group()
        pipas = pygame.sprite.Group()
        detect_group = pygame.sprite.Group()
        Player = player()

        create_pipa()

        all_sprites.add(Player)
        nilai = 0
        game_over = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                gravitasi = 0
                gravitasi -= 5

    gravitasi += 0.15
    Player.rect.y += gravitasi

    bird_hit_point = pygame.sprite.spritecollide(Player, detect_group, False)
    if bird_hit_point and not bird_hit_point[0].hit:
        nilai += 1
        bird_hit_point[0].hit = True
        score_sound.play()

    bird_hit_pipa = pygame.sprite.spritecollide(Player, pipas, False)
    if bird_hit_pipa:
        game_over = True
        selesai_sound.play()

    if len(pipas) <= 0:
        create_pipa()

    all_sprites.update()
    screen.fill(hitam)
    all_sprites.draw(screen)
    show_text(str(nilai), 32, putih, lebar//2, tinggi//4 - 100)
    pygame.time.Clock().tick(30)
    pygame.display.update()
