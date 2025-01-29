import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Sand Simulator")

# Colors
BLACK = (0, 0, 0)

# Grid dimensions
GRID_SIZE = 5 # Each pixel represents a grid cell
cols, rows = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE

# Grid to store the sand particles and their colors
grid = [[None for _ in range(rows)] for _ in range(cols)]

# Frame rate
clock = pygame.time.Clock()

# Size of the square to spawn
SQUARE_SIZE = 5

# Function to generate a random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Main loop
running = True
dragging = False
current_color = None  # Variable to store the current color for the batch

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                current_color = random_color()  # Generate a new color for the batch

        # Mouse button up event
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False

    # If dragging, spawn sand particles in a 5x5 square with the same color
    if dragging and current_color is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        start_x = mouse_x // GRID_SIZE
        start_y = mouse_y // GRID_SIZE

        for dx in range(SQUARE_SIZE):
            for dy in range(SQUARE_SIZE):
                x_pos = start_x + dx
                y_pos = start_y + dy
                if 0 <= x_pos < cols and 0 <= y_pos < rows:
                    if grid[x_pos][y_pos] is None:  # Only place if empty
                        grid[x_pos][y_pos] = current_color  # Place sand particle with color

    # Update sand particles
    for x in range(cols):
        for y in range(rows - 1, -1, -1):
            if grid[x][y] is not None:  # Check for sand particle
                # Fall down
                if y < rows - 1 and grid[x][y + 1] is None:
                    grid[x][y + 1] = grid[x][y]  # Move down
                    grid[x][y] = None  # Clear old position
                # Fall left
                elif x > 0 and y < rows - 1 and grid[x - 1][y + 1] is None:
                    grid[x - 1][y + 1] = grid[x][y]  # Move left and down
                    grid[x][y] = None  # Clear old position
                # Fall right
                elif x < cols - 1 and y < rows - 1 and grid[x + 1][y + 1] is None:
                    grid[x + 1][y + 1] = grid[x][y]  # Move right and down
                    grid[x][y] = None  # Clear old position

    # Draw everything
    screen.fill(BLACK)
    for x in range(cols):
        for y in range(rows):
            if grid[x][y] is not None:
                pygame.draw.rect(screen, grid[x][y], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)  # Adjust this value for faster/slower simulation

pygame.quit()