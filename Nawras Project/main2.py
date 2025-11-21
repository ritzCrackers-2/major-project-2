import pygame

pygame.init()
pygame.font.init()

width, height = 800, 600
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

x_velocity = width // 2
y_velocity = height - 80
player_radius = 20

lane_left = int(width * 0.25)
lane_right = int(width * 0.75)


lane_shift = 0


left_block = pygame.Rect(0, 250, 40, 40)
right_block = pygame.Rect(0, 460, 40, 40)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                    lane_shift = 0
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.key == pygame.K_a:
                x_velocity -= 6
            if event.key == pygame.K_d:
                x_velocity += 6
            if event.key == pygame.K_w:
                y_velocity -= 6
            if event.key == pygame.K_s:
                y_velocity += 6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_velocity += 6
            if event.key == pygame.K_d:
                x_velocity -= 6
            if event.key == pygame.K_w:
                y_velocity += 6
            if event.key == pygame.K_s:
                y_velocity -= 6

    if game_state == MENU:
        draw_main_menu()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        lane_shift += 6
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        lane_shift -= 6


    lane_left_actual = lane_left + lane_shift
    lane_right_actual = lane_right + lane_shift


    track_width = lane_right_actual - lane_left_actual

    left_block.x = lane_left_actual + 40
    right_block.x = lane_right_actual - 40 - right_block.width

    screen.fill((0, 0, 0))

    neon_green = (0, 255, 80)
    pygame.draw.line(screen, neon_green, (lane_left_actual, 0), (lane_left_actual, height), 4)
    pygame.draw.line(screen, neon_green, (lane_right_actual, 0), (lane_right_actual, height), 4)




    pygame.draw.rect(screen, (255, 40, 40), left_block)
    pygame.draw.rect(screen, (255, 40, 40), right_block)

    pygame.draw.circle(screen, neon_green, (x_velocity, y_velocity), player_radius, 2)

    player_box = pygame.Rect(x_velocity-player_radius, y_velocity-player_radius, player_radius*2, player_radius*2)

    if left_block.colliderect(player_box) or right_block.colliderect(player_box):
        game_state = MENU

    pygame.display.flip()
    clock.tick(60)

pygame.quit()