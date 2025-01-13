import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_speed = 7

# Enemy settings
enemy_size = 50
enemy_speed = 5
enemy_list = []

# Clock
clock = pygame.time.Clock()

# Score
score = 0

def drop_enemies(enemy_list):
    if len(enemy_list) < 5:
        x_pos = random.randint(0, WIDTH - enemy_size)
        enemy_list.append([x_pos, 0])

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list):
    global score
    for enemy in enemy_list[:]:  # Iterate over a copy to avoid modification errors
        if enemy[1] < HEIGHT:
            enemy[1] += enemy_speed
        else:
            enemy_list.remove(enemy)
            score += 1

def detect_collision(player_pos, enemy_pos):
    px, py = player_pos
    ex, ey = enemy_pos
    if (ex < px < ex + enemy_size or ex < px + player_size < ex + enemy_size) and \
       (ey < py < ey + enemy_size or ey < py + player_size < ey + enemy_size):
        return True
    return False

def game_over():
    font = pygame.font.SysFont("comicsans", 50)
    text = font.render("Game Over!", True, RED)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# Game Loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Drop enemies
    drop_enemies(enemy_list)
    update_enemy_positions(enemy_list)

    # Draw player and enemies
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    draw_enemies(enemy_list)

    # Collision detection
    for enemy in enemy_list:
        if detect_collision((player_x, player_y), enemy):
            game_over()

    # Display score
    font = pygame.font.SysFont("comicsans", 30)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
