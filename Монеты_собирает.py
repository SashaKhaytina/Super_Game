import random
import sqlite3
import pygame
import os
import sys
pygame.init()
con = sqlite3.connect('data/побег')
cur = con.cursor()
log = 'Test'
otvet = cur.execute('''SELECT game FROM Reg WHERE login IS (?)''', (log, )).fetchall()
person_clici = str(otvet[0][0]).split(' ')
size = width, height = 1200, 650
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
game_music = pygame.mixer.Sound('data/game.mp3')
game_music.set_volume(0.025)
clici = [0, 0, 0, 0, 0]
money_player_obshii = cur.execute('''SELECT money FROM Reg WHERE login IS (?)''', (log, )).fetchall()
money_player_obshii = money_player_obshii[0][0]
money_player = 0
money_brag = 0


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
            Records()
        if 500 < x < 700 and 215 < y < 245:
            New_Game()
        if 510 < x < 685 and 340 < y < 375:
            Education()
        if 295 < x < 900 and 460 < y < 495:
            Information()


class Records: #рекорды
    def __init__(self):
        pass


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
        while True:
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


money_group = pygame.sprite.Group()
tile_images = {'wall': load_image('box.png'),
              'empty': load_image('grass.png'),
               'end': load_image('end.jpg'),
               'money': load_image('монета.png')}
player_image = load_image('mar.png')
tile_width = tile_height = 50
money = 0


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
        line = ["Вам не доступен этот персонаж, ", "веберите другого персонажа."]
    elif set == 4:
        font = pygame.font.Font(None, 30)
        line = ["Вам не доступен этот враг, ", "веберите другого врага."]
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


def generate_level(level):
    money = [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    k = 0
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
                new_player = Player(x, y)
                level[y][x] = '.'
            elif level[y][x] == '*':
                Tile('end', x, y)
    return new_player, x + 1, y + 1


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



'''class Money(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sprite_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

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
        self.image = self.frames[self.cur_frame]

   # dragon = Money(load_image("pygame-8-1.png"), 8, 2, 50, 50)'''


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 90, tile_height * pos_y + 80)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 90,
                                               tile_height * self.pos[1] + 80)


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


'''def Money_kac(person, x, y):
    if person == 'hero':
        Tile('empty', x, y)'''


def Dvech(hero, xod):
    global money_player
    x, y = hero.pos
    if xod == 'up':
        if y > 0:
            if level_map[y - 1][x] == '.':
                hero.move(x, y - 1)
            if level_map[y - 1][x] == '*':
                hero.move(x, y - 1)
                End()
            if level_map[y - 1][x] == '$':
                hero.move(x, y - 1)
                # Money_kac('hero', x, y - 1)
                Tile('empty', x, y - 1)
                level_map[y - 1][x] = '.'
                money_player += 1
    elif xod == 'down':
        if y < max_y - 1:
            if level_map[y + 1][x] == '.':
                hero.move(x, y + 1)
            if level_map[y + 1][x] == '*':
                hero.move(x, y + 1)
                End()
            if level_map[y + 1][x] == '$':
                hero.move(x, y + 1)
                Tile('empty', x, y + 1)
                level_map[y + 1][x] = '.'
                money_player += 1
            # hero.move(x, y + 1)
    elif xod == 'left':
        if x > 0:
            if level_map[y][x - 1] == '.':
                hero.move(x - 1, y)
            if level_map[y][x - 1] == '*':
                hero.move(x - 1, y)
                End()
            if level_map[y][x - 1] == '$':
                hero.move(x - 1, y)
                Tile('empty', x - 1, y)
                level_map[y][x - 1] = '.'
                money_player += 1
    elif xod == 'right':
        if x < max_x - 1:
            if level_map[y][x + 1] == '.':
                hero.move(x + 1, y)
            if level_map[y][x + 1] == '*':
                hero.move(x + 1, y)
                End()
            if level_map[y][x + 1] == '$':
                hero.move(x + 1, y)
                Tile('empty', x + 1, y)
                level_map[y][x + 1] = '.'
                money_player += 1
                '''font = pygame.font.Font(None, 40)
                string_rendered = font.render(f'X{money_player}', 1, (255, 242, 0))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = 30
                intro_rect.x = 65
                screen.blit(string_rendered, intro_rect)'''


class Game:
    def __init__(self):
        global money_player
        money_brag = 0
        fon = pygame.transform.scale(load_image('fon_game.jpg'), size)
        screen.blit((fon), (0, 0))
        image = pygame.transform.scale(load_image('монета.png'), (40, 40))
        screen.blit((image), (22, 22))
        screen.blit((image), (1078, 22))
        xp = 15
        for i in range(xp):
            pygame.draw.rect(screen, (0, 128, 0), (i * 15 + 200, 22, 10, 40))
        font = pygame.font.Font(None, 40)
        string_rendered = font.render(f'X{money_player}', 1, (255, 242, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 30
        intro_rect.x = 65
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render(f'X{4}', 1, (255, 242, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 30
        intro_rect.x = 65
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render(f'X{money_brag}', 1, (255, 242, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 30
        intro_rect.x = 1120
        screen.blit(string_rendered, intro_rect)
        player = None
        running = True
        global level_map, max_x, max_y
        level_map = load_level('map')
        player, max_x, max_y = generate_level(level_map)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        Dvech(player, 'up')
                    if event.key == pygame.K_DOWN:
                        Dvech(player, 'down')
                    if event.key == pygame.K_RIGHT:
                        Dvech(player, 'right')
                    if event.key == pygame.K_LEFT:
                        Dvech(player, 'left')
            string_rendered = font.render(f'X{money_player}', 1, (255, 242, 0))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 30
            intro_rect.x = 65
            screen.blit(string_rendered, intro_rect)
            sprite_group.draw(screen)
            hero_group.draw(screen)
            pygame.display.flip()


class End:
    def __init__(self):
        global person_clici
        for i in range(3):
            if int(person_clici[i]) < 3:
                t = int(person_clici[i])
                person_clici[i] = str(t + 1)
                con = sqlite3.connect('data/побег')
                cur = con.cursor()
                cur.execute("""UPDATE Reg
                                    SET game = (?)
                                    WHERE login == (?)
                                   """, (' '.join(person_clici), 'Test'))
                con.commit()


class Education: #обучение
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


class Information: #информация о фрагах и персонажах
    def __init__(self):
        pass


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


if __name__ == '__main__':
    pygame.display.set_caption('Побег из хранилища')
    running = True
    Music()
    start_screen()
    Menu_screen()
