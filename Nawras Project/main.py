import pygame 

pygame.init()

Screen1 = pygame.display.set_mode((800, 400))
sand_surface = pygame.image.load("images/sky.png").convert()
grounf_surface = pygame.image.load("images/ground.png").convert()
sand_surface = pygame.transform.scale(sand_surface, (800, 400))
ball_sur = pygame.image.load("images/ball.png").convert_alpha()
target_sur = pygame.image.load("images/target.png").convert_alpha()
game_active = True
x_velocity = 0
y_velocity = 0

pygame.mixer.music.load("music/sponge.mp3")
pygame.mixer.music.play(loops=-1)
hitSound = pygame.mixer.Sound("music/se.mp3")

ball_rect = ball_sur.get_rect(center = (400, 200))
target_rect = target_sur.get_rect(center = (600, 300))
while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_velocity = x_velocity - 1
            if event.key == pygame.K_d:
                x_velocity = x_velocity + 1
            if event.key == pygame.K_w:
                y_velocity = y_velocity - 1
            if event.key == pygame.K_s:
                y_velocity = y_velocity + 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_velocity = x_velocity + 1
            if event.key == pygame.K_d:
                x_velocity = x_velocity - 1
            if event.key == pygame.K_w:
                y_velocity = y_velocity + 1
            if event.key == pygame.K_s:
                y_velocity = y_velocity - 1
            
    ball_rect.move_ip(x_velocity, y_velocity)
    Screen1.blit(sand_surface, (0,0))
    Screen1.blit(ball_sur, ball_rect)
    Screen1.blit(target_sur, target_rect)
    if ball_rect.colliderect(target_rect):
        hitSound.play()
        pygame.time.delay(5000)
        game_active = False
    pygame.display.update()
    pygame.time.Clock().tick(60)