import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slope")

MENU = 0
PLAYING = 1
game_state = MENU

red = (255, 0, 0)
black = (0, 0, 0)
neon = (0, 255, 80)

title_font = pygame.font.SysFont("comicsans", 40)
menu_font = pygame.font.SysFont("comicsans", 24)

clock = pygame.time.Clock()

def draw_menu():
    screen.fill(red)
    title = title_font.render("Slope Game", True, black)
    start = menu_font.render("Press ENTER to Play", True, black)
    quit_game = menu_font.render("Press ESC to Quit", True, black)

    screen.blit(title, (width//2 - title.get_width()//2, 150))
    screen.blit(start, (width//2 - start.get_width()//2, 330))
    screen.blit(quit_game, (width//2 - quit_game.get_width()//2, 380))

    pygame.display.flip()

player_x = width // 2
player_y = height // 2
player_speed = 6
player_radius = 20

lane_left = int(width * 0.25)
lane_right = int(width * 0.75)

camera_offset_y = 0

block_left = pygame.Rect(lane_left + 40, 250, 40, 40)
block_right = pygame.Rect(lane_right - 80, 460, 40, 40)
#12 120 pixel tall lines
segment_h = 120
track_segments = [i * segment_h for i in range(12)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                    player_x = width // 2
                    player_y = height // 2
                    camera_offset_y = 0

                if event.key == pygame.K_ESCAPE:
                    running = False

    if game_state == MENU:
        draw_menu()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        camera_offset_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        camera_offset_y += player_speed

    min_x = lane_left + player_radius
    max_x = lane_right - player_radius

    if player_x < min_x:
        player_x = min_x
    if player_x > max_x:
        player_x = max_x

    screen.fill((0, 0, 0))

    for i in range(len(track_segments)):
        y = track_segments[i] - camera_offset_y#calculates segments screen position

        pygame.draw.line(screen, neon, (lane_left, y), (lane_left, y + segment_h), 4)
        pygame.draw.line(screen, neon, (lane_right, y), (lane_right, y + segment_h), 4)

        if y > height:
            track_segments[i] -= len(track_segments) * segment_h#below = moved upward by the total segment height
        if y + segment_h < 0:
            track_segments[i] += len(track_segments) * segment_h#same thing but above

    block_left.y = 250 - camera_offset_y
    block_right.y = 460 - camera_offset_y

    pygame.draw.rect(screen, red, block_left)
    pygame.draw.rect(screen, red, block_right)

    pygame.draw.circle(screen, neon, (player_x, player_y), player_radius, 2)

    player_rect = pygame.Rect(player_x - player_radius,
                              player_y - player_radius,
                              player_radius*2,
                              player_radius*2)

    if block_left.colliderect(player_rect) or block_right.colliderect(player_rect):
        game_state = MENU

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
