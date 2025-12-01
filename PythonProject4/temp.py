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


def draw_main_menu():
    screen.fill(red)
    title = title_font.render("Slope Game", True, black)
    start = menu_font.render("Press ENTER to Play", True, black)
    quit_game = menu_font.render("Press ESC to Quit", True, black)
    screen.blit(title, (width // 2 - title.get_width() // 2, 150))
    screen.blit(start, (width // 2 - start.get_width() // 2, 330))
    screen.blit(quit_game, (width // 2 - quit_game.get_width() // 2, 380))
    pygame.display.flip()


player_radius = 20
player_speed = 2

lane_left = int(width * 0.25)
lane_right = int(width * 0.75)

track_center = 500
track_speed = 6

player_h = 50
player_w = 50
spawn = random.randint(track_center - 200 + 30, track_center + 200 - 30)

screen1 = pygame.display.set_mode((1000, 600))
bg_surface = pygame.image.load("sprites/Bg1.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (1200, 600))
track_surface = pygame.image.load("sprites/Track.png").convert()
track_surface = pygame.transform.scale(track_surface, (400, 600))
ball_sur = pygame.image.load("sprites/Player1.png").convert_alpha()
ball_sur = pygame.transform.scale(ball_sur, (player_w, player_h))
target_sur = pygame.image.load("sprites/BlockFrame1.png").convert_alpha()
target_sur = pygame.transform.scale(target_sur, (64, 82))
Block_sur = pygame.image.load("sprites/BlockFrame1.png").convert_alpha()
Block_sur = pygame.transform.scale(Block_sur, (64, 64))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/Player1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (player_w, player_h))
        self.posx = 500
        self.posy = 550
        self.rect = self.image.get_rect(center=(self.posx, self.posy))
        self.rect = self.rect.inflate(-10, -10)
        self.character = None

    def reset_position(self):
        self.rect.center = (self.posx, self.posy)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        self.image = pygame.image.load("sprites/BlockFrame1.png").convert_alpha()
        self.spawnx = x_pos
        self.posy = -50
        self.rect = self.image.get_rect(center=(self.spawnx, self.posy))
        self.rect = self.rect.inflate(-5, -5)
        self.number = 0

    def update(self):
        self.rect.move_ip(0, track_speed)
        self.posy += track_speed
        if self.posy > height + 50:
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


self = Player()

enemies = pygame.sprite.Group()

track = Track()

ball_rect = pygame.draw.circle(screen, (0, 0, 0), (500, 500), player_radius, 45)
target_rect = target_sur.get_rect(center=(spawn, 300))
track_rect = track.surface.get_rect()

running = True
spawned = 0
enemy = []

spawn_timer = 0
spawn_frequency = 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                    self.reset_position()
                    enemies.empty()
                    spawned = 0
                if event.key == pygame.K_ESCAPE:
                    running = False

    if game_state == MENU:
        draw_main_menu()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()

    x_velocity = 0
    y_velocity = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x_velocity = -player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x_velocity = player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        y_velocity = -player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y_velocity = player_speed

    self.rect.move_ip(x_velocity, y_velocity)

    track_rect.x = track_center - 200
    track_rect.y = 0

    screen1.blit(bg_surface, (0, 0))
    screen.blit(track.surface, (track_center - 200, track.y))
    screen.blit(track.surface, (track_center - 200, track.y - track.track_height))
    track.move()

    spawn_timer += 1
    if spawn_timer >= spawn_frequency:
        track_left_bound = track_center - 200
        track_right_bound = track_center + 200
        spawn_x = random.randint(track_left_bound + 40, track_right_bound - 40)
        block1 = Enemy(spawn_x)
        enemy.append(block1)
        enemies.add(block1)
        spawn_timer = 0

    enemies.update()
    enemies.draw(screen)

    if pygame.sprite.spritecollideany(self, enemies):
        running = False

    screen1.blit(self.image, self.rect)

    player_center_x = self.rect.centerx
    if player_center_x < (track_center - 200 + 10) or player_center_x > (track_center + 200 - 10):
        running = False

        # if left_block.colliderect(player_box) or right_block.colliderect(player_box):
    #    game_state = MENU

    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
