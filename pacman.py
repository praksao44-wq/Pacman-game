import pygame
import random
import sys
import os

# Initialize
pygame.init()

# Screen settings
WIDTH, HEIGHT = 560, 620
TILE_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Py Pacman")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GHOST_BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Maze layout (1 = wall, 0 = pellet, 2 = power pellet, 3 = empty space)
maze = [
    "1111111111111111111111",
    "1220000001110000000221",
    "1011111110110111111101",
    "1011111110110111111101",
    "1000000000000000000001",
    "1011111011111110111101",
    "1000001000000001000001",
    "1111011011111101011011",
    "1000010000300001000010",
    "1011111110110111111101",
    "1220000000000000000221",
    "1111111111111111111111"
]

ROWS = len(maze)
COLS = len(maze[0])

# Game objects
pellets = []
power_pellets = []
walls = []

for y, row in enumerate(maze):
    for x, col in enumerate(row):
        if col == "0":
            pellets.append((x, y))
        elif col == "1":
            walls.append((x, y))
        elif col == "2":
            power_pellets.append((x, y))

# Load high score
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
else:
    highscore = 0

# Player
player_x, player_y = 10, 9
score = 0
lives = 3

# Ghosts
ghosts = [
    {"pos": [10, 7], "color": RED, "dir": (1, 0)},
    {"pos": [9, 7], "color": PINK, "dir": (-1, 0)},
    {"pos": [11, 7], "color": CYAN, "dir": (0, 1)},
    {"pos": [10, 8], "color": ORANGE, "dir": (0, -1)},
]

vulnerable_timer = 0

def draw_maze():
    for (x, y) in walls:
        pygame.draw.rect(screen, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    for (x, y) in pellets:
        pygame.draw.circle(screen, WHITE, (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), 3)
    for (x, y) in power_pellets:
        pygame.draw.circle(screen, WHITE, (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), 6)

def draw_player(x, y):
    pygame.draw.circle(screen, YELLOW, (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//2 - 2)

def draw_ghost(ghost):
    color = ghost["color"]
    if vulnerable_timer > 0:
        color = GHOST_BLUE
    pygame.draw.circle(screen, color, (ghost["pos"][0]*TILE_SIZE + TILE_SIZE//2, ghost["pos"][1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//2 - 2)

def move_ghost(ghost):
    if random.randint(0, 10) < 3:  # Random direction change
        ghost["dir"] = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
    new_x = ghost["pos"][0] + ghost["dir"][0]
    new_y = ghost["pos"][1] + ghost["dir"][1]
    if (new_x, new_y) not in walls:
        ghost["pos"] = [new_x, new_y]

def save_highscore():
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_highscore()
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    if keys[pygame.K_LEFT]:
        new_x -= 1
    if keys[pygame.K_RIGHT]:
        new_x += 1
    if keys[pygame.K_UP]:
        new_y -= 1
    if keys[pygame.K_DOWN]:
        new_y += 1

    if (new_x, new_y) not in walls:
        player_x, player_y = new_x, new_y

    # Eat pellets
    if (player_x, player_y) in pellets:
        pellets.remove((player_x, player_y))
        score += 10
    if (player_x, player_y) in power_pellets:
        power_pellets.remove((player_x, player_y))
        score += 50
        vulnerable_timer = FPS * 7  # 7 seconds

    # Move ghosts
    for ghost in ghosts:
        move_ghost(ghost)
        if (ghost["pos"][0], ghost["pos"][1]) == (player_x, player_y):
            if vulnerable_timer > 0:
                ghost["pos"] = [10, 7]  # Send back to cage
                score += 200
            else:
                lives -= 1
                player_x, player_y = 10, 9
                if lives <= 0:
                    save_highscore()
                    pygame.quit()
                    sys.exit()

    # Timer for power pellet effect
    if vulnerable_timer > 0:
        vulnerable_timer -= 1

    # Draw maze & objects
    draw_maze()
    draw_player(player_x, player_y)
    for ghost in ghosts:
        draw_ghost(ghost)

    # Draw score
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_text = font.render(f"Highscore: {highscore}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 60))
    screen.blit(high_text, (10, HEIGHT - 40))
    screen.blit(lives_text, (WIDTH - 100, HEIGHT - 40))

    # Update highscore
    if score > highscore:
        highscore = score

    pygame.display.flip()
    clock.tick(FPS)
