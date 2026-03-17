import pygame
import sys
import random

TILE_SIZE = 24
GRID_WIDTH = 28
GRID_HEIGHT = 20

SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

FPS = 8

BLACK = (0, 0, 0)
NAVY = (10, 10, 80)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
RED = (255, 0, 0)


# Harta labirintului
# 0 = gol, 1 = perete, 2 = punct


LEVEL_MAP = [
    "1111111111111111111111111111",
    "1000000000000000000000000001",
    "1011110111110111110111110101",
    "1020000100000100000100000101",
    "1011110111110111110111110101",
    "1000000000000000000000000001",
    "1011110111110111110111110101",
    "1000000100000000000100000001",
    "1110110110111111011010110111",
    "1000100000100000100000100001",
    "1011101110101110101110111101",
    "1000000100000000000100000001",
    "1011110111110111110111110101",
    "1000000000000100000000000001",
    "1011110111110111110111110101",
    "1020000100000000000100000201",
    "1011110111110111110111110101",
    "1000000000000000000000000001",
    "1000000000000000000000000001",
    "1111111111111111111111111111",
]

maze = [[int(c) for c in row] for row in LEVEL_MAP]

def is_wall(x, y):
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        return maze[y][x] == 1
    return True

def count_dots():
    total = 0
    for row in maze:
        total += row.count(2)
    return total

class Player:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.dir_x = 0
        self.dir_y = 0
        self.next_dir = (0, 0)

    def update(self):
        ndx, ndy = self.next_dir
        nx = self.grid_x + ndx
        ny = self.grid_y + ndy
        if not is_wall(nx, ny):
            self.dir_x, self.dir_y = self.next_dir

        nx = self.grid_x + self.dir_x
        ny = self.grid_y + self.dir_y
        if not is_wall(nx, ny):
            self.grid_x = nx
            self.grid_y = ny

        if maze[self.grid_y][self.grid_x] == 2:
            maze[self.grid_y][self.grid_x] = 0

    def draw(self, surface):
        px = self.grid_x * TILE_SIZE + TILE_SIZE // 2
        py = self.grid_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(surface, YELLOW, (px, py), TILE_SIZE // 2 - 2)


class Ghost:
    def __init__(self, x, y, color):
        self.grid_x = x
        self.grid_y = y
        self.color = color
        self.dir_x = 0
        self.dir_y = 0
        self.change_direction_random()

    def change_direction_random(self):
        possible_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(possible_dirs)
        for dx, dy in possible_dirs:
            nx = self.grid_x + dx
            ny = self.grid_y + dy
            if not is_wall(nx, ny):
                self.dir_x, self.dir_y = dx, dy
                return

    def update(self):
        if random.random() < 0.3:
            self.change_direction_random()

        nx = self.grid_x + self.dir_x
        ny = self.grid_y + self.dir_y
        if is_wall(nx, ny):
            self.change_direction_random()
        else:
            self.grid_x = nx
            self.grid_y = ny

    def draw(self, surface):
        px = self.grid_x * TILE_SIZE
        py = self.grid_y * TILE_SIZE

        w = TILE_SIZE
        h = TILE_SIZE


        pygame.draw.rect(surface, self.color, (px, py + h//3, w, h*2//3))

        pygame.draw.circle(surface, self.color, (px + w//2, py + h//3), w//2)

        eye_radius = 3
        eye_offset_x = 5
        eye_offset_y = 5
        pygame.draw.circle(surface, WHITE, (px + w//2 - eye_offset_x, py + h//3), eye_radius)
        pygame.draw.circle(surface, WHITE, (px + w//2 + eye_offset_x, py + h//3), eye_radius)

        pygame.draw.circle(surface, BLACK, (px + w//2 - eye_offset_x, py + h//3), 1)
        pygame.draw.circle(surface, BLACK, (px + w//2 + eye_offset_x, py + h//3), 1)


def draw_maze(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = maze[y][x]
            if tile == 1:
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, NAVY, rect)
            elif tile == 2:
                px = x * TILE_SIZE + TILE_SIZE // 2
                py = y * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(surface, WHITE, (px, py), 3)


def check_collision(player, ghosts):
    for g in ghosts:
        if g.grid_x == player.grid_x and g.grid_y == player.grid_y:
            return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)


    player_start = (1, 1)
    ghosts_start = [(26, 1), (26, 18), (1, 18)]

    player = Player(*player_start)

    ghosts = [
        Ghost(ghosts_start[0][0], ghosts_start[0][1], RED),
        Ghost(ghosts_start[1][0], ghosts_start[1][1], PINK),
        Ghost(ghosts_start[2][0], ghosts_start[2][1], CYAN),
    ]

    running = True
    game_over = False
    win = False


    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 0:
                maze[y][x] = 2
            if maze[y][x] == 1:
                continue


    maze[player_start[1]][player_start[0]] = 0
    for gx, gy in ghosts_start:
        maze[gy][gx] = 0

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.next_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.next_dir = (1, 0)
                elif event.key == pygame.K_UP:
                    player.next_dir = (0, -1)
                elif event.key == pygame.K_DOWN:
                    player.next_dir = (0, 1)
                elif event.key == pygame.K_r and (game_over or win):
                    return main()

        if not game_over and not win:
            
            player.update()
            for g in ghosts:
                g.update()

            if check_collision(player, ghosts):
                game_over = True

            if count_dots() == 0:
                win = True

        screen.fill(BLACK)
        draw_maze(screen)
        player.draw(screen)
        for g in ghosts:
            g.draw(screen)

        if game_over:
            text = font.render("Ai pierdut! :( Apasa R pentru restart.", True, WHITE)
            screen.blit(text, (40, SCREEN_HEIGHT // 2 - 10))
        elif win:
            text = font.render("Ai castigat!:) Apasa R pentru restart.", True, WHITE)
            screen.blit(text, (40, SCREEN_HEIGHT // 2 - 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
