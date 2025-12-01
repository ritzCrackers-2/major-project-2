import pygame
import random

pygame.init()
pygame.font.init()

width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slope")

MENU = 0
PLAYING = 1
game_state = MENU

sky = (135, 206, 235)
red = (255, 0, 0)
black = (0, 0, 0)

title_font = pygame.font.SysFont('comicsans', 40)
menu_font = pygame.font.SysFont('comicsans', 24)

clock = pygame.time.Clock()
running = True

def draw_main_menu():
    screen.fill(red)
    title = title_font.render("Slope Game", True, black)
    start = menu_font.render("Press ENTER to Play", True, black)
    quit_game = menu_font.render("Press ESC to Quit", True, black)
    screen.blit(title, (width // 2 - title.get_width() // 2, 150))
    screen.blit(start, (width // 2 - start.get_width() // 2, 330))
    screen.blit(quit_game, (width // 2 - quit_game.get_width() // 2, 380))
    pygame.display.flip()


x_velocity = 0
y_velocity = 0
player_radius = 20


lane_left = int(width * 0.25)
lane_right = int(width * 0.75)

camera_offset_x = 0
camera_offset_y = 0

track_center = 500
track_speed = 3
speed = 3

bg_speed =  track_speed/2

player_h = 50
player_w = 50
spawn = random.randint(track_center - 200 + 30, track_center + 200 - 30)

screen1 = pygame.display.set_mode((1000, 600))

#lowk this stuff not needed
track_surface = pygame.image.load("sprites/Track.png").convert()
track_surface = pygame.transform.scale(track_surface, (400, 600))
ball_sur = pygame.image.load("sprites/Player1.png").convert_alpha()
ball_sur = pygame.transform.scale(ball_sur, (player_w, player_h))
target_sur = pygame.image.load("sprites/BlockFrame1.png").convert_alpha()
target_sur = pygame.transform.scale(target_sur, (64, 82))
#stuff above

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/Player1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (player_w, player_h))
        self.posx = 500
        self.posy = 550
        self.rect = self.image.get_rect(center=(self.posx, self.posy)).inflate(-10, -10)
        self.character = None
    safe=False
    grounded=True

enemies = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, number, image):
        super().__init__()
        self.image = image
        self.spawnx = random.randint(track_center - 200 + 50, track_center + 200 - 50)
        self.posy = -100
        self.rect = self.image.get_rect(center=(self.spawnx, self.posy + 16))
        self.rect = self.rect.inflate(-5, -5)
        self.number = number

    def update(self):
        self.posy += track_speed
        self.rect.y = self.posy + 16

        if self.posy > 650:
            self.kill()


class Track(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("sprites/Track.png").convert()
        self.surface = pygame.transform.scale(self.surface, (400, 600))
        self.track_width, self.track_height = self.surface.get_size()
        self.y = 0

    def move(self):
        self.y += track_speed
        if self.y > self.track_height:
            self.y = 0

class BackGround(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("sprites/bg1.png").convert()
        self.surface = pygame.transform.scale(self.surface, (1200, 600))
        self.bg_width, self.bg_height = self.surface.get_size()
        self.y = 0

    def move(self):
        self.y += bg_speed
        if self.y > self.bg_height:
            self.y = 0



class SlowDown(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/Slow.png.png").convert()
        self.spawnx = random.randint(track_center - 200 + 50, track_center + 200 - 50)
        self.posy = -100
        self.rect = self.image.get_rect(center=(self.spawnx, self.posy))
        self.rect = self.rect.inflate(-5, -5)
        self.spawn_time = random.randint(2,5)*60

    def update(self):
        self.posy += track_speed
        self.rect.y = self.posy + 16

        if self.posy > 650:
            self.kill()


self = Player()
bg = BackGround()
track = Track()
Enemy_spawn_time = random.randint(1000, 6000)
last_spawn = 0

enemy_image = pygame.image.load("sprites/BlockFrame1.png").convert_alpha()

ball_rect = pygame.draw.circle(screen, (0, 0, 0), (500, 500), player_radius, 45)
target_rect = target_sur.get_rect(center=(spawn, 300)).inflate(-20, -20)
track_rect = track.surface.get_rect()
track_rect.inflate(0, 0)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                    camera_offset_x = 0
                    camera_offset_y = 0
                if event.key == pygame.K_ESCAPE:
                    running = False

    if game_state == MENU:
        draw_main_menu()
        clock.tick(60)
        continue

    now = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    boost = 120

    x_velocity = 0
    y_velocity = 0


    if now%boost==0:
        speed += 0.5
    track_speed = speed

    if keys[pygame.K_SPACE]:
        track_speed = track_speed*2

    bg_speed = track_speed / 2
    player_speed = track_speed

    if keys[pygame.K_RSHIFT]:
        player_speed = player_speed*2

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x_velocity = -player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x_velocity = player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        y_velocity = -player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y_velocity = player_speed





    track_rect.x = track_center - 200
    track_rect.y = 0

    screen1.blit(bg.surface, (0, bg.y))
    screen1.blit(bg.surface, (0, bg.y - bg.bg_height))
    bg.move()
    screen.blit(track.surface, (track_center - 200, track.y))
    screen.blit(track.surface, (track_center - 200, track.y - track.track_height))
    track.move()

    spawned = 0
    amount = random.randint(1, 3)

    enemy = []

    ENEMY=Enemy(spawned, enemy_image)





    if now - last_spawn > Enemy_spawn_time:
        spawned += 1
        Enemy_spawn_time = random.randint(1000, 6000)/(track_speed/3)
        amount = random.randint(1, 3)
        for x in range(amount):
            ENEMY = Enemy(spawned, enemy_image)
            enemies.add(ENEMY)
            last_spawn = now
            enemies.draw(screen1)

    if self.safe == False:
        if pygame.sprite.spritecollide(self, enemies, False):
            running = False

    enemies.update()
    enemies.draw(screen1)

    screen1.blit(self.image, self.rect)
    if self.grounded == True:
        if not self.rect.colliderect(track_rect):
            running = False

    self.rect.move_ip(x_velocity, y_velocity)
    target_rect.move_ip(0, track_speed)



    # if left_block.colliderect(player_box) or right_block.colliderect(player_box):
    #    game_state = MENU

    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
