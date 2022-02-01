import random
import sqlite3
import pygame
import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5 import uic

pygame.init()
size = width, height = 1200, 650
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
game_music = pygame.mixer.Sound('data/game.mp3')
game_music.set_volume(0.025)
clici = [0, 0, 0, 0, 0]
person_clici = [1, 2, 2, 0, 0]
person_login = ''
person_money = 0 #для теста, потом изменится
money_brag = 0
tile_width = tile_height = 50
money_record = 0
time_record = 0
ymnosh = 1 #при всяких баффов
xp = 15
f = True
person_time = 0
end = False
x0 = 0
y0 = 0
vragg = None


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for i in self:
            i.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Reg(QMainWindow):
    def __init__(self):
        super().__init__()
        self.money = 50
        uic.loadUi('data/reg.ui', self)  # Загружаем дизайн
        self.db = sqlite3.connect("data/info.db")
        self.sql = self.db.cursor()
        self.sql.execute("""CREATE TABLE IF NOT EXISTS users(
                    login TEXT,
                    password TEXT,
                    current_money INT,
                    clici TEXT)""")
        self.sql.execute("""CREATE TABLE IF NOT EXISTS records(
                            login TEXT,
                            money INTEGER,
                            time INTEGER)""")
        self.db.commit()
        self.show()
        self.pushButton.clicked.connect(self.check)

    def check(self):
        self.l = self.lineEdit.text()
        self.p = self.lineEdit_2.text()
        if self.l == '' or self.p == '':
            self.label_3.setText("Заполните поля!")
            self.label_3.adjustSize()
        else:
            result = self.sql.execute("""SELECT * FROM users WHERE login = (?)""",
                                      (self.l,)).fetchall()
            if len(result) > 0:
                if result[0][1] == self.p:
                    global person_clici, person_money, person_login, money_record, time_record
                    records_data = self.sql.execute("""SELECT * FROM records WHERE login = (?)""",
                                                    (self.l,)).fetchall()
                    person_clici = [int(i) for i in result[0][3].split(' ')]
                    person_money = result[0][2]
                    person_login = self.l
                    money_record = records_data[0][1]
                    time_record = records_data[0][2]
                    self.close()
                else:
                    self.label_3.setText("Неправильный пароль!")
                    self.label_3.adjustSize()
                    self.lineEdit_2.setText("")
            else:
                self.sql.execute("""INSERT INTO users(login, password, current_money, clici)
                                    VALUES (?, ?, ?, ?)""",
                                 (str(self.l), str(self.p), int(self.money), '1 2 2 0 0'))
                self.db.commit()
                person_clici = [1, 2, 2, 0, 0]
                person_money = self.money
                person_login = self.l
                global f
                f = False
                self.close()


def start_screen():
    fon = pygame.transform.scale(load_image('fon1.jpg'), size)
    screen.blit((fon), (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


class Menu_screen:
    def __init__(self):
        fon = pygame.transform.scale(load_image('fon2.jpg'), size)
        screen.blit((fon), (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 0
        intro_text = ['Рекорды', 'Новая игра', 'Обучение', "Информация о врагах/персонажах"]
        for line in range(len(intro_text)):
            string_rendered = font.render(intro_text[line], 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 90
            intro_rect.top = text_coord
            intro_rect.x = (1200 - intro_rect.width)//2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Menu_screen.on_click(self, event.pos)
            pygame.display.flip()

    def on_click(self, cell_coords):
        x = cell_coords[0]
        y = cell_coords[1]
        if 520 < x < 680 and 85 < y < 120:
            try:
                w2 = Record()
                w2.show()
                sys.exit(app.exec_())
            except SystemExit as b:
                pygame.display.set_caption('Побег из хранилища')
                Music()
                Menu_screen()
        if 500 < x < 700 and 215 < y < 245:
            New_Game()
        if 510 < x < 685 and 340 < y < 375:
            Education()
        if 295 < x < 900 and 460 < y < 495:
            Information()


def VRAG(x0, y0):
    # pic = load_image('mar.png')
    x = x0
    y = y0
    Tile('vrag', x, y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y, s):
        super().__init__(hero_group)
        global clici, ymnosh, xp
        if s == 'i':
            self.image = player_image[str(clici[1])]
        else:
            self.image = player_image[str(clici[1])]
        if clici[1] == 2:
            ymnosh = 1.5
        elif clici[1] == 3:
            xp = 20
        self.rect = self.image.get_rect().move(tile_width * pos_x + 90, tile_height * pos_y + 80)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 90,
                                               tile_height * self.pos[1] + 80)

    def my_shag(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 90,
                                               tile_height * self.pos[1] + 80)


class New_Game: #настройки игры
    def __init__(self):
        slova = ['Выберите сложность', 'Карта:', 'Персонаж:', 'Враг:', 'Количество врагов:',
                 'Интервал появления врагов:']
        var = [[], ['1', '2', '3'], ['1', '2', '3'], ['1', '2', '3'], ['1', '2'], ['1 ход', '2 хода', '3 хода']]
        fon = pygame.transform.scale(load_image('fon_settings.jpg'), size)
        screen.blit((fon), (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (900, 550, 280, 80))
        im = pygame.image.load('data/кменю.png')
        screen.blit((im), (20, 590))
        font = pygame.font.Font(None, 60)
        heig = 15
        weig = 15
        heig2 = 15
        weig2 = 670
        global clici
        clici = [0, 0, 0, 0, 0]
        for i in range(len(slova)):
            string_rendered = font.render(slova[i], 1, (226, 225, 253))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = heig
            intro_rect.x = weig
            heig += 80
            weig2 = 670
            screen.blit(string_rendered, intro_rect)
            for n in range(len(var[i])):
                pygame.draw.rect(screen, (255, 255, 255), (weig2 - 35, heig2 + 5, 30, 30))
                string_rendered = font.render(var[i][n], 1, (226, 225, 253))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = heig2
                intro_rect.x = weig2
                screen.blit(string_rendered, intro_rect)
                weig2 += 180
            heig2 += 80
        line = "Начать игру"
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 560
        intro_rect.x = 910
        screen.blit(string_rendered, intro_rect)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    New_Game.on_click(self, event.pos)
            pygame.display.flip()
        pygame.quit()

    def on_click(self, cell_coords):
        x = cell_coords[0]
        y = cell_coords[1]
        no = (255, 255, 255)
        yes = (0, 255, 0)
        global clici
        if 900 < x < 1180 and 550 < y < 630:
            set = setting()
            if set is True:
                pygame.mixer.music.pause()
                game_music.play(-1)
                Game()
            else:
                Ochib(set)
        elif 20 < x < 70 and 590 < y < 640:
            Menu_screen()
        elif 670 - 35 < x < 670 - 5 and 95 + 5 < y < 95 + 30:
            pygame.draw.rect(screen, yes, (670 - 35, 95 + 5, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5, 30, 30))
            pygame.draw.rect(screen, no, (670 + 360 - 35, 95 + 5, 30, 30))
            clici[0] = 1
            Ochib(0)
        elif 670 - 35 + 180 < x < 670 + 180 - 5 and 95 + 5 < y < 95 + 30:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5, 30, 30))
            pygame.draw.rect(screen, yes, (670 - 35 + 180, 95 + 5, 30, 30))
            pygame.draw.rect(screen, no, (670 + 360 - 35, 95 + 5, 30, 30))
            clici[0] = 2
            Ochib(0)
        elif 670 - 35 + 360 < x < 670 + 360 - 5 and 95 + 5 < y < 95 + 30:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5, 30, 30))
            pygame.draw.rect(screen, yes, (670 + 360 - 35, 95 + 5, 30, 30))
            clici[0] = 3
            Ochib(0)
        elif 670 - 35 < x < 670 - 5 and 95 + 5 + 80 < y < 95 + 30 + 80:
            pygame.draw.rect(screen, yes, (670 - 35, 95 + 5 + 80, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5 + 80, 30, 30))
            pygame.draw.rect(screen, no, (670 + 360 - 35, 95 + 5 + 80, 30, 30))
            clici[1] = 1
            Ochib(0)
        elif 670 - 35 + 180 < x < 670 + 180 - 5 and 95 + 5 + 80 < y < 95 + 30 + 80:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5 + 80, 30, 30))
            pygame.draw.rect(screen, yes, (670 - 35 + 180, 95 + 5 + 80, 30, 30))
            pygame.draw.rect(screen, no, (670 + 360 - 35, 95 + 5 + 80, 30, 30))
            clici[1] = 2
            Ochib(0)
        elif 670 - 35 + 360 < x < 670 + 360 - 5 and 95 + 5 + 80 < y < 95 + 30 + 80:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5 + 80, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5 + 80, 30, 30))
            pygame.draw.rect(screen, yes, (670 + 360 - 35, 95 + 5 + 80, 30, 30))
            clici[1] = 3
            Ochib(0)
        elif 670 - 35 < x < 670 - 5 and 95 + 160 + 5 < y < 95 + 160 + 30:
            pygame.draw.rect(screen, yes, (670 - 35, 95 + 5 + 160, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5 + 160, 30, 30))
            pygame.draw.rect(screen, no, (670 + 360 - 35, 95 + 5 + 160, 30, 30))
            clici[2] = 1
            Ochib(0)
        elif 670 - 35 + 180 < x < 670 + 180 - 5 and 95 + 160 + 5 < y < 95 + 160 + 30:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5 + 160, 30, 30))
            pygame.draw.rect(screen, yes, (670 - 35 + 180, 95 + 5 + 160, 30, 30))
            pygame.draw.rect(screen, no, (670 + 360 - 35, 95 + 5 + 160, 30, 30))
            clici[2] = 2
            Ochib(0)
        elif 670 - 35 + 360 < x < 670 + 360 - 5 and 95 + 5 + 160 < y < 95 + 30 + 160:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5 + 160, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5 + 160, 30, 30))
            pygame.draw.rect(screen, yes, (670 + 360 - 35, 95 + 5 + 160, 30, 30))
            clici[2] = 3
            Ochib(0)
        elif 670 - 35 < x < 670 - 5 and 95 + 5 + 240 < y < 95 + 30 + 240:
            pygame.draw.rect(screen, yes, (670 - 35, 95 + 5 + 240, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5 + 240, 30, 30))
            clici[3] = 1
            Ochib(0)
        elif 670 - 35 + 180 < x < 670 + 180 - 5 and 95 + 5 + 240 < y < 95 + 30 + 240:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5 + 240, 30, 30))
            pygame.draw.rect(screen, yes, (670 - 35 + 180, 95 + 5 + 240, 30, 30))
            clici[3] = 2
            Ochib(0)
        elif 670 - 35 < x < 670 - 5 and 95 + 5 + 320 < y < 95 + 30 + 320:
            pygame.draw.rect(screen, yes, (670 - 35, 95 + 5 + 320, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5 + 320, 30, 30))
            pygame.draw.rect(screen, no, (670 + 360 - 35, 95 + 5 + 320, 30, 30))
            clici[4] = 1
            Ochib(0)
        elif 670 - 35 + 180 < x < 670 + 180 - 5 and 95 + 5 + 320 < y < 95 + 30 + 320:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5 + 320, 30, 30))
            pygame.draw.rect(screen, yes, (670 - 35 + 180, 95 + 5 + 320, 30, 30))
            pygame.draw.rect(screen, no, (670 + 360 - 35, 95 + 5 + 320, 30, 30))
            clici[4] = 2
            Ochib(0)
        elif 670 - 35 + 360 < x < 670 + 360 - 5 and 95 + 5 + 320 < y < 95 + 30 + 320:
            pygame.draw.rect(screen, no, (670 - 35, 95 + 5 + 320, 30, 30))
            pygame.draw.rect(screen, no, (670 - 35 + 180, 95 + 5 + 320, 30, 30))
            pygame.draw.rect(screen, yes, (670 + 360 - 35, 95 + 5 + 320, 30, 30))
            clici[4] = 3
            Ochib(0)


money_player = 0


class Game:
    def __init__(self):
        money_brag = 0
        fon = pygame.transform.scale(load_image('fon_game.jpg'), size)
        screen.blit((fon), (0, 0))
        image = pygame.transform.scale(load_image('монета.png'), (40, 40))
        screen.blit((image), (22, 22))
        screen.blit((image), (1078, 22))
        for i in range(xp):
            pygame.draw.rect(screen, (0, 128, 0), (i * 15 + 200, 22, 10, 40))
        font = pygame.font.Font(None, 40)
        change_money()
        string_rendered = font.render(f'X{money_brag}', 1, (255, 242, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 30
        intro_rect.x = 1120
        screen.blit(string_rendered, intro_rect)
        player = None
        self.running = True
        global level_map, max_x, max_y, end, clici
        level_map = load_level(levers[clici[0]])
        player, max_x, max_y = generate_level(level_map, 1)
        self.time_start = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        Dvech(player, 'up')
                    if event.key == pygame.K_DOWN:
                        Dvech(player, 'down')
                    if event.key == pygame.K_RIGHT:
                        Dvech(player, 'right')
                    if event.key == pygame.K_LEFT:
                        Dvech(player, 'left')
            if end:
                self.End()
            pygame.draw.rect(screen, (10, 10, 10), (25, 600, 150, 25))
            self.change_time()
            pygame.display.update()
            sprite_group.draw(screen)
            hero_group.draw(screen)
            pygame.display.flip()

    def End(self):
        screen.fill((0, 0, 0))
        self.running = False
        #fon = pygame.transform.scale(load_image('fon_settings.jpg'), size)
        #screen.blit((fon), (0, 0))
        im = pygame.image.load('data/кменю.png')
        screen.blit((im), (20, 590))
        self.db = sqlite3.connect("data/info.db")
        self.sql = self.db.cursor()
        global person_clici, money_player, person_login, person_time, time_record, money_record, person_money
        for i in range(3):
            if int(person_clici[i]) < 3:
                person_clici[i] += 1
        self.sql.execute("""UPDATE users 
        SET clici = (?) 
        WHERE login == (?)""", (' '.join([str(i) for i in person_clici]), person_login))
        self.db.commit()
        if time_record < person_time:
            time_record = person_time
        if money_record < money_player * ymnosh:
            money_record = money_player * ymnosh
        person_money = person_money + (money_player * ymnosh)

    def change_time(self):
        itog_time = round(time.time() - self.time_start, 2)
        font = pygame.font.Font(None, 40)
        string_rendered = font.render(f'time:{itog_time}', 1, (255, 255, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 600
        intro_rect.x = 30
        screen.blit(string_rendered, intro_rect)


def change_money():
    font = pygame.font.Font(None, 40)
    string_rendered = font.render(f'X{money_player}', 1, (255, 242, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 30
    intro_rect.x = 65
    pygame.draw.rect(screen, (56, 56, 56), (80, 13, 40, 55))
    screen.blit(string_rendered, intro_rect)


class Education:  # обучение
    def __init__(self):
        fon = pygame.transform.scale(load_image('fonchik.jpg'), size)
        screen.blit((fon), (0, 0))
        font = pygame.font.Font(None, 30)
        im = pygame.image.load('data/кменю.png')
        screen.blit((im), (20, 590))
        im = pygame.image.load('data/кигре.png')
        screen.blit((im), (1080, 590))
        lines = ['Обучение:',
                 'Игрок передвигается с помощью стрелочек. Задача игрока - выйти из хранилища.',
                 'Для этого нужно собирать монеты, но будьте внимательны, охранники хранилища будут вам мешать!',
                 'Чтобы выйти из хранилища надо заплатить. Только собрав определенное количество монет хранилище',
                 'выпустит вас.',
                 '                                 Удачи!']
        # МОЖНО МЕНЯТЬ lines
        for i in range(len(lines)):
            string_rendered = font.render(lines[i], 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 50 * (i + 1)
            intro_rect.x = 50
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Education.on_click(self, event.pos)
            pygame.display.flip()
        pygame.quit()

    def on_click(self, cell_coords):
        x = cell_coords[0]
        y = cell_coords[1]
        if 20 < x < 120 and 590 < y < 640:
            Menu_screen()
        elif 1080 < x < 1180 and 590 < y < 640:
            New_Game()


class Information:  # информация о фрагах и персонажах
    def __init__(self):
        fon = pygame.transform.scale(load_image('fonchik.jpg'), size)
        enemy = pygame.transform.scale(load_image('enemy.png'), (300, 300))
        hero1 = pygame.transform.scale(load_image('герой1.png'), (60, 60))
        hero2 = pygame.transform.scale(load_image('герой2.png'), (60, 60))
        hero3 = pygame.transform.scale(load_image('герой3.png'), (60, 60))
        screen.blit((fon), (0, 0))
        screen.blit((enemy), (900, 210))

        screen.blit((hero1), (910, 60))
        screen.blit((hero2), (980, 60))
        screen.blit((hero3), (1070, 60))
        font = pygame.font.Font(None, 30)
        im = pygame.image.load('data/кменю.png')
        screen.blit((im), (20, 590))
        im = pygame.image.load('data/кигре.png')
        screen.blit((im), (1080, 590))
        lines = ['Главный герой: ',
                 'Различают три типа главного героя, которые вы можете открывать постепенно,',
                 'за определенное количество монет!',
                 '',
                 'Враги:',
                 'Враги также могут отличаться не только картинкой, но и скоростью появления,',
                 'своим количеством. Это все создано, чтобы вам было интересней играть!',
                 '',
                 '                                                                         Желаем удачи!']
        for i in range(len(lines)):
            string_rendered = font.render(lines[i], 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 50 * (i + 1)
            intro_rect.x = 50
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Information.on_click(self, event.pos)
            pygame.display.flip()
        pygame.quit()

    def on_click(self, cell_coords):
        x = cell_coords[0]
        y = cell_coords[1]
        if 20 < x < 120 and 590 < y < 640:
            Menu_screen()
        elif 1080 < x < 1180 and 590 < y < 640:
            New_Game()


class Record(QMainWindow):
    def __init__(self):
        super().__init__()
        global person_login, time_record, money_record
        uic.loadUi('data/record.ui', self)
        self.db = sqlite3.connect("data/info.db")
        self.sql = self.db.cursor()
        result = self.sql.execute("""SELECT * FROM records WHERE login = ?""",
                                  (person_login,)).fetchall()
        if len(result) > 0:
            if result[0][1] < money_record:
                self.sql.execute(f"""UPDATE records
                                    SET money = {money_record}                                    
                                    WHERE login = '{person_login}'""")
                self.db.commit()
            if result[0][2] < time_record:
                self.sql.execute(f"""UPDATE records
                                    SET time = {time_record}
                                    WHERE login = '{person_login}'""")
                self.db.commit()
        else:
            self.sql.execute(f"""INSERT INTO records(login, money, time) 
            VALUES('{person_login}', {money_record}, {time_record})""")
            self.db.commit()
        self.show_db()
        self.radioButton.clicked.connect(self.show_db)
        self.radioButton_2.clicked.connect(self.show_db)

    def show_db(self):
        self.textBrowser.clear()
        vid = 'money' if self.radioButton.isChecked() else 'time'
        result = self.sql.execute(f"""SELECT * FROM records ORDER BY {vid} desc""")
        output = []
        for i in result:
            output.append('  -  '.join([str(k) for k in i]))
        self.textBrowser.setText('\n'.join(output))


def Music():
    # + надо изменение музыки когда враг близко
    pygame.init()
    pygame.mixer.music.load('data/star_musik.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.025)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


money_group = pygame.sprite.Group()
tile_images = {'wall': load_image('box.png'),
              'empty': load_image('grass.png'),
               'end': load_image('end.jpg'),
               'money': load_image('монета.png'),
               'vrag': load_image('герой3.png')}
player_image = {'1': load_image('герой1.png'),
                '2': load_image('герой2.png'),
                '3': load_image('герой3.png')}
levers = {1: 'level1', 2: "level2", 3: 'level3'}


def Ochib(set):
    font = pygame.font.Font(None, 60)
    line = ['']
    pygame.draw.rect(screen, (0, 0, 0), (900, 550, 280, 80))
    if set == 0:
        line = ["Начать игру"]
    elif set == 1:
        font = pygame.font.Font(None, 30)
        line = ["Не выбран элемент ", "(нажмите что бы выбрать)"]
    elif set == 2:
        font = pygame.font.Font(None, 30)
        line = ["Вам не доступен этот уровень,", "пройдите уровень меньше. "]
    elif set == 3:
        font = pygame.font.Font(None, 30)
        line = ["Вам не доступен этот персонаж,", "выберите другого персонажа."]
    elif set == 4:
        font = pygame.font.Font(None, 30)
        line = ["Вам не доступен этот враг,", "выберите другого врага."]
    h = 560
    for i in range(len(line)):
        string_rendered = font.render(line[i], 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = h
        intro_rect.x = 910
        screen.blit(string_rendered, intro_rect)
        h += 30


def setting():
    global clici, person_clici
    if 0 in clici:
        return 1
    elif clici[0] > int(person_clici[0]):
        return 2
    elif clici[1] > int(person_clici[1]):
        return 3
    elif clici[2] > int(person_clici[2]):
        return 4
    else:
        return True


def generate_level(level, nom):
    global x0
    global y0
    global vragg
    if nom == 1:
        money = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif nom == 2:
        money = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif nom == 3:
        money = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                elem = random.randint(1, len(money))
                el = money[elem - 1]
                money.pop(elem - 1)
                if el == 0:
                    level[y][x] = '.'
                else:
                    level[y][x] = '$'
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '$':
                Tile('empty', x, y)
                Tile('money', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y, 'i')
                level[y][x] = '.'
            elif level[y][x] == '*':
                Tile('end', x, y)
            else:
                Tile('empty', x, y)
                vragg = Player(x, y, 'v')
                x0 = x
                y0 = y
                level[y][x] = '.'
    return new_player, x + 1, y + 1


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 75, tile_height * pos_y + 75)


class Money(Sprite): #у меня не получилось подключить анимацию
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sprite_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * x + 75, tile_height * y + 75)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame] #


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


level_map = None
player, max_x, max_y = None, None, None

k = 0
def Dvech(hero, xod):
    global money_player
    global x0
    global y0
    global vragg
    global k
    if level_map[y0 - 1][x0] == '.' and k == 0:
        vragg.my_shag(x0, y0 - 1)
        y0 -= 1
    elif level_map[y0 + 1][x0] != '#':
        vragg.my_shag(x0, y0 + 1)
        y0 += 1
        k = 1
    else:
        k = 0
    x, y = hero.pos
    global money_player, end
    if xod == 'up':
        if y > 0:
            if level_map[y - 1][x] == '.':
                hero.move(x, y - 1)
            if level_map[y - 1][x] == '*':
                hero.move(x, y - 1)
                if money_player >= 20:
                    end = True
                else:
                    Not_Money()
            if level_map[y - 1][x] == '$':
                level_map[y-1][x] = '.'
                Tile('empty', x, y - 1)
                hero.move(x, y - 1)
                money_player += 1
                change_money()
    elif xod == 'down':
        if y < max_y - 1:
            if level_map[y + 1][x] == '.':
                hero.move(x, y + 1)
            if level_map[y + 1][x] == '*':
                hero.move(x, y + 1)
                if money_player >= 20:
                    end = True
                else:
                    Not_Money()
            if level_map[y + 1][x] == '$':
                hero.move(x, y + 1)
                level_map[y + 1][x] = '.'
                Tile('empty', x, y + 1)
                money_player += 1
                change_money()
    elif xod == 'left':
        if x > 0:
            if level_map[y][x - 1] == '.':
                hero.move(x - 1, y)
            if level_map[y][x - 1] == '*':
                hero.move(x - 1, y)
                if money_player >= 20:
                    end = True
                else:
                    Not_Money()
            if level_map[y][x - 1] == '$':
                hero.move(x - 1, y)
                level_map[y][x - 1] = '.'
                Tile('empty', x - 1, y)
                money_player += 1
                change_money()
    elif xod == 'right':
        if x < max_x - 1:
            if level_map[y][x + 1] == '.':
                hero.move(x + 1, y)
            if level_map[y][x + 1] == '*':
                hero.move(x + 1, y)
                if money_player >= 20:
                    end = True
                else:
                    Not_Money()
            if level_map[y][x + 1] == '$':
                hero.move(x + 1, y)
                level_map[y][x + 1] = '.'
                Tile('empty', x + 1, y)
                money_player += 1
                change_money()


def Not_Money():
    pass


if __name__ == '__main__':
    try:
        start_screen()
        app = QApplication(sys.argv)
        w = Reg()
        w.show()
        sys.exit(app.exec_())
    except SystemExit as e:
        pygame.display.set_caption('Побег из хранилища')
        running = True
        Music()
        start_screen()
        Menu_screen()
