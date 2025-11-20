import pygame
import sys

pygame.init()
pygame.font.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slope")


MENU = 0
PLAYING = 1
game_state = MENU


sky = (135, 206, 235)
black = (0, 0, 0)


title_font = pygame.font.SysFont('comicsans', 40)
menu_font = pygame.font.SysFont('comicsans', 24)

clock = pygame.time.Clock()


def draw_main_menu():
    screen.fill(sky)

    title = title_font.render("Slope Game", True, black)
    start = menu_font.render("Press ENTER to Play", True, black)
    quit_game = menu_font.render("Press ESC to Quit", True, black)

    screen.blit(title, (width // 2 - title.get_width() // 2, 150))
    screen.blit(start, (width // 2 - start.get_width() // 2, 330))
    screen.blit(quit_game, (width // 2 - quit_game.get_width() // 2, 380))

    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                if event.key == pygame.K_ESCAPE:
                    running = False


    if game_state == MENU:
        draw_main_menu()
        clock.tick(60)
        continue


    screen.fill((50, 50, 50))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
