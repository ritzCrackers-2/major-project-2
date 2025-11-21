import pygame

pygame.init()

Screen1 = pygame.display.set_mode((800, 400))
sky_surface = pygame.image.load("images/sky.png").convert()
ground_surface = pygame.image.load("images/ground.png").convert()
ball_sur = pygame.image.load("images/ball.png").convert_alpha()
block_sur = pygame.image.load("images/block.png").convert_alpha()

sky_surface = pygame.transform.scale(sky_surface, (800, 400))

pygame.mixer.music.load("music/spoonge.mp3")
pygame.mixer.music.play(loops=-1)
hitSound = pygame.mixer.Sound("music/se.mp3")

game_active = True
x_velocity = 0
y_velocity = 0

camera_x = 0      # moves world left/right
camera_y = 0      # moves world up/down

ball_rect = ball_sur.get_rect(center = (400, 200))

# Borders on left and right
left_wall = pygame.Rect(0, 0, 200, 400)
right_wall = pygame.Rect(600, 0, 200, 400)

# Blocks in the world (world coords)
blocks = [
    pygame.Rect(300, 250, 80, 80),
    pygame.Rect(700, 260, 80, 80),
    pygame.Rect(1100, 230, 80, 80)
]

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_velocity -= 1.5
            if event.key == pygame.K_d:
                x_velocity += 1.5
            if event.key == pygame.K_w:
                y_velocity -= 1.5
            if event.key == pygame.K_s:
                y_velocity += 1.5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_velocity += 1.5
            if event.key == pygame.K_d:
                x_velocity -= 1.5
            if event.key == pygame.K_w:
                y_velocity += 1.5
            if event.key == pygame.K_s:
                y_velocity -= 1.5

    
    ball_rect.move_ip(x_velocity, y_velocity)

    
    camera_x -= x_velocity
    camera_y -= y_velocity

  
    Screen1.blit(sky_surface, (0, 0))

  
    block_rects_on_screen = []
    for b in blocks:
        shifted = pygame.Rect(b.x + camera_x, b.y + camera_y, b.width, b.height)
        block_rects_on_screen.append(shifted)
        Screen1.blit(block_sur, shifted)

 
    Screen1.blit(ball_sur, ball_rect)

 
    pygame.draw.rect(Screen1, (255, 0, 0), left_wall)
    pygame.draw.rect(Screen1, (255, 0, 0), right_wall)

  
    if ball_rect.colliderect(left_wall) or ball_rect.colliderect(right_wall):
        hitSound.play()
        pygame.time.delay(1500)
        game_active = False


    for b in block_rects_on_screen:
        if ball_rect.colliderect(b):
            hitSound.play()
            pygame.time.delay(1500)
            game_active = False

    pygame.display.update()
    pygame.time.Clock().tick(60)
