import random
import sys
import time
import pygame

# maze game cause sigma


# Configuration
CELL_SIZE = 24      # pixels per cell
MAZE_COLS = 25      # number of columns
MAZE_ROWS = 19      # number of rows
WALL_COLOR = (40, 40, 40)
BG_COLOR = (220, 220, 220)
PLAYER_COLOR = (200, 30, 30)
GOAL_COLOR = (30, 160, 30)
FPS = 60

# Directions: (dx, dy), wall indices ordering: top, right, bottom, left
DIRS = {
    'N': (0, -1, 0),
    'S': (0, 1, 2),
    'W': (-1, 0, 3),
    'E': (1, 0, 1),
}
OPPOSITE = {0:2, 1:3, 2:0, 3:1}  # opposite wall index mapping


class Cell:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        # walls: top, right, bottom, left (True = wall exists)
        self.walls = [True, True, True, True]
        self.visited = False

    def coords(self):
        return (self.col, self.row)


def index(col, row, cols, rows):
    if 0 <= col < cols and 0 <= row < rows:
        return row * cols + col
    return None


def generate_maze(cols, rows):
    # Create grid of cells
    grid = [Cell(c, r) for r in range(rows) for c in range(cols)]

    # Recursive backtracker iterative
    start = grid[0]
    start.visited = True
    stack = [start]

    while stack:
        current = stack[-1]
        c, r = current.col, current.row
        neighbors = []

        # check neighbors that are unvisited
        for dir_key, (dx, dy, wall_idx) in DIRS.items():
            nc, nr = c + dx, r + dy
            idx = index(nc, nr, cols, rows)
            if idx is not None:
                neighbor = grid[idx]
                if not neighbor.visited:
                    neighbors.append((neighbor, wall_idx))

        if neighbors:
            neighbor, wall_idx = random.choice(neighbors)
            # knock down wall between current and neighbor
            current.walls[wall_idx] = False
            neighbor.walls[OPPOSITE[wall_idx]] = False
            neighbor.visited = True
            stack.append(neighbor)
        else:
            stack.pop()

    # After generation clear visited flags for potential use later
    for cell in grid:
        cell.visited = False
    return grid


def draw_maze(surface, grid, cols, rows, cell_size):
    for cell in grid:
        x = cell.col * cell_size
        y = cell.row * cell_size

        # draw background for cell (optional)
        pygame.draw.rect(surface, BG_COLOR, (x, y, cell_size, cell_size))

        # walls: top, right, bottom, left
        if cell.walls[0]:
            pygame.draw.line(surface, WALL_COLOR, (x, y), (x + cell_size, y), 2)
        if cell.walls[1]:
            pygame.draw.line(surface, WALL_COLOR, (x + cell_size, y), (x + cell_size, y + cell_size), 2)
        if cell.walls[2]:
            pygame.draw.line(surface, WALL_COLOR, (x + cell_size, y + cell_size), (x, y + cell_size), 2)
        if cell.walls[3]:
            pygame.draw.line(surface, WALL_COLOR, (x, y + cell_size), (x, y), 2)


def main():
    pygame.init()
    cols, rows = MAZE_COLS, MAZE_ROWS
    width = cols * CELL_SIZE
    height = rows * CELL_SIZE

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    def new_game():
        grid = generate_maze(cols, rows)
        player = [0, 0]  # col, row
        goal = [cols - 1, rows - 1]
        start_time = time.time()
        won = False
        steps = 0
        return grid, player, goal, start_time, won, steps

    grid, player, goal, start_time, won, steps = new_game()

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid, player, goal, start_time, won, steps = new_game()

                if not won:
                    moved = False
                    col, row = player
                    cur = grid[index(col, row, cols, rows)]

                    if event.key in (pygame.K_UP, pygame.K_w):
                        # move north if no top wall
                        if not cur.walls[0] and row > 0:
                            player[1] -= 1
                            moved = True
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        if not cur.walls[2] and row < rows - 1:
                            player[1] += 1
                            moved = True
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if not cur.walls[3] and col > 0:
                            player[0] -= 1
                            moved = True
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if not cur.walls[1] and col < cols - 1:
                            player[0] += 1
                            moved = True

                    if moved:
                        steps += 1
                        if player == goal:
                            won = True
                            win_time = time.time() - start_time

        # draw
        screen.fill(WALL_COLOR)
        draw_maze(screen, grid, cols, rows, CELL_SIZE)

        # draw goal
        gx = goal[0] * CELL_SIZE
        gy = goal[1] * CELL_SIZE
        pygame.draw.rect(screen, GOAL_COLOR, (gx + 4, gy + 4, CELL_SIZE - 8, CELL_SIZE - 8))

        # draw player
        px = player[0] * CELL_SIZE + CELL_SIZE // 2
        py = player[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, PLAYER_COLOR, (px, py), CELL_SIZE // 3)

        # HUD
        elapsed = time.time() - start_time
        hud_surf = font.render(f"Steps: {steps}  Time: {int(elapsed)}s  (R = regenerate)", True, (10, 10, 10))
        screen.blit(hud_surf, (8, 8))

        if won:
            msg = f"You reached the goal in {steps} steps, {int(win_time)}s! Press R to play again."
            win_surf = font.render(msg, True, (0, 0, 0))
            # center overlay
            rect = win_surf.get_rect(center=(width // 2, height // 2))
            overlay = pygame.Surface((rect.width + 20, rect.height + 20))
            overlay.fill((240, 240, 180))
            screen.blit(overlay, (rect.x - 10, rect.y - 10))
            screen.blit(win_surf, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
