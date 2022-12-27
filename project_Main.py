import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image




player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

FPS = 50
WIDTH = 550
HEIGHT = 550
STEP = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('tank1.png')

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        self.rect = None

    def get_event(self, event):
        pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.image_orig = self.image
        self.rot = ''
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        Player.rotation_pl(self)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)

    def rotation_pl(self):
        rotation_pers = 0
        self.image = self.image_orig
        if stor == 'l':
            self.rot = 'l'
            rotation_pers = -90
        elif stor == 'u':
            self.rot = 'u'
            rotation_pers = -180
        elif stor == 'r':
            self.rot = 'r'
            rotation_pers = 90
        self.image = pygame.transform.rotate(self.image, rotation_pers)


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def start_screen():
    pygame.init()
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50

    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    x = 100
    y = 100
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
            pygame.display.flip()
            clock.tick(FPS)


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and (level_map[y - 1][x] == '.' or level_map[y - 1][x] == '@'):
            hero.move(x, y - 1)
    elif movement == 'down':
        if y > 0 and (level_map[y + 1][x] == '.' or level_map[y + 1][x] == '@'):
            hero.move(x, y + 1)
    elif movement == 'left':
        if y > 0 and (level_map[y][x - 1] == '.' or level_map[y][x - 1] == '@'):
            hero.move(x - 1, y)
    elif movement == 'right':
        if y > 0 and (level_map[y][x + 1] == '.' or level_map[y][x + 1] == '@'):
            hero.move(x + 1, y)


start_screen()
map1 = 'map.txt'
level_map = load_level(map1)
player, level_x, level_y = generate_level(load_level(map1))
rot = ''
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                stor = 'l'
                move(player, 'left')
            if event.key == pygame.K_RIGHT:
                stor = 'r'
                move(player, 'right')
            if event.key == pygame.K_UP:
                stor = 'u'
                move(player, 'up')
            if event.key == pygame.K_DOWN:
                stor = 'd'
                move(player, 'down')
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()
