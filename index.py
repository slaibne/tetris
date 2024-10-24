import pygame
import random

held_tetrimino = None
swap_allowed = True

pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 30
HOLD_AREA_X = 20
HOLD_AREA_Y = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Shape of Tetriminos
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1],
     [1, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[1, 0, 0],
     [1, 1, 1],],
    [[0, 0, 1],
     [1, 1, 1]]
]

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock for controlling game speed
clock = pygame.time.Clock()


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

    def move_up(self):
        self.y -= 1


# Create grid and draw grid lines
def create_grid():
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
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

    def __call__(self, action="down", *args, **kwargs):
        if action == "down":
            self.move_down()
        elif action == "left":
            self.move_left()
        elif action == "right":
            self.move_right()
        elif action == "rotate":
            self.rotate()


def draw_tetrimino(surface, tetrimino):
    for i, row in enumerate(tetrimino.shape):
        for j, val in enumerate(row):
            if val:
                pygame.draw.rect(
                    surface,
                    tetrimino.color,
                    (
                        tetrimino.x * BLOCK_SIZE + j * BLOCK_SIZE,
                        tetrimino.y * BLOCK_SIZE + i * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                )


def draw_text(surface, text, font_size, color, position):
    font = pygame.font.SysFont("Ariel", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = position
    surface.blit(text_surface, text_rect)


def new_tetrimino():
    shape = random.choice(SHAPES)
    color = random.choice([(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)])
    return Tetrimino(shape, color)


def move_tetrimino(tetrimino, direction, grid):
    if direction == "left":
        tetrimino.x -= 1
        if check_collision(tetrimino, grid):
            tetrimino.x += 1  # Undo move if it collides with the wall or other blocks
    elif direction == "right":
        tetrimino.x += 1
        if check_collision(tetrimino, grid):
            tetrimino.x -= 1  # Undo move if it collides with the wall or other blocks
    elif direction == "down":
        tetrimino.y += 1
        if check_collision(tetrimino, grid):
            tetrimino.y -= 1  # Undo move if it collides with the bottom or other blocks
            return True  # Return True if the Tetrimino has collided with the bottom
    elif direction == "rotate":
        old_shape = tetrimino.shape
        tetrimino.rotate()
        if check_collision(tetrimino, grid):
            tetrimino.shape = old_shape  # Undo rotation if it collides
    return False


def check_collision(tetrimino, grid):
    for i, row in enumerate(tetrimino.shape):
        for j, val in enumerate(row):
            if val:
                if (
                    i + tetrimino.y >= GRID_HEIGHT  # Hits bottom
                    or j + tetrimino.x < 0  # Hits left wall
                    or j + tetrimino.x >= GRID_WIDTH  # Hits right wall

                    or grid[i + tetrimino.y][j + tetrimino.x] == BLACK

                    or grid[i + tetrimino.y][j + tetrimino.x] != 0

                ):  # Hits another block
                    return True
    return False


def lock_tetrimino(tetrimino, grid, locked_positions):
    # Add Tetrimino blocks to locked positions
    for i, row in enumerate(tetrimino.shape):
        for j, val in enumerate(row):
            if val != 0:
                locked_positions[(tetrimino.x + j, tetrimino.y + i)] = tetrimino.color
    # Upgrade grid to reflect locked pieces
    for pos in locked_positions:
        p = pos
        grid[p[1]][p[0]] = locked_positions[pos]


def hard_drop(tetrimino, grid):
    while not check_collision(tetrimino, grid):
        tetrimino.y += 1
    tetrimino.y -= 1


def hold_tetrimino(current_tetrimino, held_tetrimino, swap_allowed):

    # Do nothing if swapping is not allowed
    if not swap_allowed:
        return current_tetrimino, held_tetrimino, swap_allowed

    if held_tetrimino is None:  # If no Tetrimino is held yet
        held_tetrimino = current_tetrimino  # Hold the current Tetrimino
        new_tetrimino()  # Spawn new tetrimino
    else:
        # Swap the held Tetrimino with the current one
        current_tetrimino, held_tetrimino, swap_tetrimino = held_tetrimino, current_tetrimino, swap_tetrimino

    swap_allowed = False
    return current_tetrimino, held_tetrimino, swap_allowed

    ## def draw_held(screen, held_tetrimino):
    if held_tetrimino:
        for i, row in enumerate(held_tetrimino.shape):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        screen,
                        held_tetrimino.color,
                        (
                            j * BLOCK_SIZE + HOLD_AREA_X,
                            i * BLOCK_SIZE + HOLD_AREA_Y,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )


def clear_lines(grid, locked_positions):
    lines_cleared = 0
    # Check from the bottom row up
    for i in reversed(range(len(grid))) # Iterate through rows bottom to top
        row = grid[i]
        if 0 not in row:  # If the row is full
            lines_cleared += 1
            # Remove row from grid
            del grid[i]
            # Add a new empty row at the top of grid
            grid.insert(0, [0 for _ in range(len(row))])
            # Remove locked positions in this row and shift down locked pieces above
            for pos in list(locked_positions):
                x, y = pos
                if y == i:  # remove block from locked positions
                    del locked_positions[pos]
                elif y < i:  # Move blocks down one row
                    locked_positions[(x, y + 1)] = locked_positions.pop((x, y))
    return lines_cleared


def calc_score(lines_cleared, score):
    if lines_cleared == 1:
        score += 40
    elif lines_cleared == 2:
        score += 100
    elif lines_cleared == 3:
        score += 300
    elif lines_cleared == 4:
        score += 1200
    return score


def game_over(locked_positions, current_tetrimino):
    for pos in current_tetrimino.shape:
        if (
            current_tetrimino.x + pos[0],
            current_tetrimino.y + pos[1],
        ) in locked_positions:
            return True
    return False


def main():
    grid = create_grid()
    locked_positions = {}  # Dictionary to store locked blocks in the grid
    current_tetrimino = new_tetrimino()
    score = 0
    fall_time = 0  # Track when the block should fall
    fall_speed = 0.1  # Control how fast the block falls (adjust as needed)
    drop_speed = 0.05
    keys = pygame.key.get_pressed()

    global swap_allowed
    global held_tetrimino

    running = True

    while running:
        screen.fill(WHITE)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        # Handeling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tetrimino(current_tetrimino, "left", grid)
                elif event.key == pygame.K_RIGHT:
                    move_tetrimino(current_tetrimino, "right", grid)
                elif event.key == pygame.K_DOWN:
                    if move_tetrimino(current_tetrimino, "down", grid):
                        lock_tetrimino(current_tetrimino, grid, locked_positions)
                        current_tetrimino = new_tetrimino()
                elif event.key == pygame.K_UP:
                    move_tetrimino(current_tetrimino, "rotate", grid)
                if event.key == pygame.K_SPACE:
                    hard_drop(current_tetrimino, grid)
                    lock_tetrimino(current_tetrimino, grid, locked_positions)
                    current_tetrimino = new_tetrimino()
                if event.key == pygame.K_z and swap_allowed:
                    current_tetrimino, held_tetrimino, swap_allowed = hold_tetrimino(
                        current_tetrimino, held_tetrimino, swap_allowed
                    )
                    # Re-enable swapping
            #          if move_tetrimino(current_tetrimino, "down", grid):
            #             lock_tetrimino(current_tetrimino, grid)
            #            current_tetrimino = new_tetrimino()
            #           swap_allowed = True  #
            if keys[pygame.K_DOWN]:  # Check if down arrow is being held
                fall_speed = drop_speed  # Speed up the fall
            else:
                fall_speed  # Default fall speed

        if fall_time / 1000 > fall_speed:
            if move_tetrimino(current_tetrimino, "down", grid):
                lock_tetrimino(current_tetrimino, grid, locked_positions)
                cleared = clear_lines(grid, locked_positions)  # Check for line clears
                score = calc_score(
                    cleared, score
                )  # Updates score based on lines cleared
                current_tetrimino = new_tetrimino()  # Spawns new tetrimino
                can_swap = True  # Resets swapping
                # Check for game over condition
                if game_over(locked_positions, current_tetrimino):
                    print(f"Game Over! Your final score is: {score}")
                    running = False
            fall_time = 0

        draw_grid(screen, grid)
        draw_tetrimino(screen, current_tetrimino)
        # draw_held(screen, held_tetrimino)

        draw_text(
            screen, f"Score: {score}", 30, (255, 255, 255), (SCREEN_WIDTH - 100, 20)
        )
        # Update the screen
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
