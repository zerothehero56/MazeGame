# maze.py
# Module for generating and drawing mazes using recursive backtracking
import random
import pygame
from config import WALL_COLOR, BG_COLOR, WINDOW_W, VIEW_H

# Directions for maze generation with offsets and wall indices
DIRS = {
    'N': (0, -1, 0),
    'S': (0,  1, 2),
    'W': (-1, 0, 3),
    'E': ( 1, 0, 1),
}
# Opposite wall indices for connecting cells
OPPOSITE = {0: 2, 1: 3, 2: 0, 3: 1}

# Cell class representing a maze cell
class Cell:
    def __init__(self, col, row):
        self.col     = col
        self.row     = row
        # Walls: [top, right, bottom, left]
        self.walls   = [True, True, True, True]
        # Visited flag for generation
        self.visited = False

# Function to get grid index from column and row
def grid_index(col, row, cols, rows):
    # Check bounds
    if 0 <= col < cols and 0 <= row < rows:
        return row * cols + col
    return None

# Function to generate a maze using recursive backtracking
def generate_maze(cols, rows):
    # Create grid of cells
    grid  = [Cell(c, r) for r in range(rows) for c in range(cols)]
    # Start from top-left cell
    start = grid[0]
    start.visited = True
    # Stack for backtracking
    stack = [start]
    # While stack is not empty
    while stack:
        # Get current cell
        cur     = stack[-1]
        # Find unvisited neighbors
        nb_list = []
        for _d, (dx, dy, widx) in DIRS.items():
            nc, nr = cur.col + dx, cur.row + dy
            idx    = grid_index(nc, nr, cols, rows)
            if idx is not None and not grid[idx].visited:
                nb_list.append((grid[idx], widx))
        # If neighbors exist
        if nb_list:
            # Choose random neighbor
            nb, widx                  = random.choice(nb_list)
            # Remove walls between cells
            cur.walls[widx]           = False
            nb.walls[OPPOSITE[widx]]  = False
            # Mark neighbor as visited
            nb.visited = True
            # Push to stack
            stack.append(nb)
        else:
            # Backtrack
            stack.pop()
    # Reset visited flags
    for cell in grid:
        cell.visited = False
    # Return the grid
    return grid

# Function to draw the maze on the surface
def draw_maze(surface, grid, cell_size, cam_ix, cam_iy):
    # Loop through each cell in the grid
    for cell in grid:
        # Calculate screen position with camera offset
        sx = cell.col * cell_size - cam_ix
        sy = cell.row * cell_size - cam_iy
        # Skip cells outside the view
        if sx + cell_size < 0 or sx > WINDOW_W or sy + cell_size < 0 or sy > VIEW_H:
            continue
        # Draw cell background
        pygame.draw.rect(surface, BG_COLOR, (sx, sy, cell_size, cell_size))
        # Draw walls if present
        if cell.walls[0]:  # Top wall
            pygame.draw.line(surface, WALL_COLOR, (sx, sy), (sx + cell_size, sy), 2)
        if cell.walls[1]:  # Right wall
            pygame.draw.line(surface, WALL_COLOR, (sx + cell_size, sy), (sx + cell_size, sy + cell_size), 2)
        if cell.walls[2]:  # Bottom wall
            pygame.draw.line(surface, WALL_COLOR, (sx + cell_size, sy + cell_size), (sx, sy + cell_size), 2)
        if cell.walls[3]:  # Left wall
            pygame.draw.line(surface, WALL_COLOR, (sx, sy + cell_size), (sx, sy), 2)

def draw_maze(surface, grid, cell_size, cam_ix, cam_iy):
    for cell in grid:
        sx = cell.col * cell_size - cam_ix
        sy = cell.row * cell_size - cam_iy
        if sx + cell_size < 0 or sx > WINDOW_W or sy + cell_size < 0 or sy > VIEW_H:
            continue
        pygame.draw.rect(surface, BG_COLOR, (sx, sy, cell_size, cell_size))
        if cell.walls[0]:
            pygame.draw.line(surface, WALL_COLOR, (sx, sy), (sx + cell_size, sy), 2)
        if cell.walls[1]:
            pygame.draw.line(surface, WALL_COLOR, (sx + cell_size, sy), (sx + cell_size, sy + cell_size), 2)
        if cell.walls[2]:
            pygame.draw.line(surface, WALL_COLOR, (sx + cell_size, sy + cell_size), (sx, sy + cell_size), 2)
        if cell.walls[3]:
            pygame.draw.line(surface, WALL_COLOR, (sx, sy + cell_size), (sx, sy), 2)
