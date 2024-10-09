import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Shape of Tetriminos
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
]

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock for controlling game speed
clock = pygame.time.Clock()


# Create grid and draw grid lines
def create_grid():
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    return grid


def draw_grid(surface, grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                0,
            )
    for i in range(GRID_HEIGHT):
        pygame.draw.line(
            surface, GRAY, (0, i * BLOCK_SIZE), (SCREEN_WIDTH, i * BLOCK_SIZE)
        )
    for j in range(GRID_WIDTH):
        pygame.draw.line(
            surface, GRAY, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, SCREEN_HEIGHT)
        )


class Tetrimino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2  # Start at middle-top
        self.y = 0  # Start at the top of the grid

    def rotate(self):
        self.shape = [
            list(row) for row in zip(*self.shape[::-1])
        ]  # rotate 90 degrees clockwise

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1


# Loop
def new_tetrimino():
    shape = random.choice(SHAPES)
    color = random.choice([(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)])
    return Tetrimino(shape, color)


def main():
    grid = create_grid()

    running = True
    while running:
        screen.fill(WHITE)

        # Handeling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid(screen, grid)

        # Update the screen
        pygame.display.update()

        # Control game speed
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
