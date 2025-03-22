import pygame

# constants
WIDTH = 800
HEIGHT = 700
CHECKER_SPEED = 1
FPS = 60
# colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (30, 180, 20)
DARK_GREEN = (30, 120, 20)
HEADER_OFFSET = 100

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 Robot - Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
font_text = pygame.font.SysFont(None, 80)
computer = False
bot_depth = 1
player = 0  # 0 is the human and 1 is the computer

map = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

def draw_button():
    pass

def draw_hud():
    if game_over:
        winner_text = "Blue Player Wins!" if winner == 1 else "Red Player Wins!"
        text = font_text.render(winner_text, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))

def draw_lines():
    for i in range(8):  # vertical lines 100 apart
        nx = 100 * i
        pygame.draw.line(screen, BLACK, (nx, HEADER_OFFSET), (nx, HEIGHT), 5)
    for j in range(6):
        ny = 100 * j
        pygame.draw.line(screen, BLACK, (0, ny + HEADER_OFFSET), (WIDTH, ny + HEADER_OFFSET), 5)

def draw_board():
    for row in range(8):
        for col in range(6):
            if map[col][row] == 1:
                draw_circle(BLUE, row, col)
            elif map[col][row] == 2:
                draw_circle(RED, row, col)
            else:
                draw_circle(DARK_GREEN, row, col)

def draw_circle(color, row, col):
    pygame.draw.circle(screen, color, (row * 100 + 50, (col * 100) + 50 + HEADER_OFFSET), 47)

def find_last(sx): 
    for row in range(5, -1, -1):  
        if map[row][sx] == 0:
            return row
    return -1  

def get_player():
    return 1 if player == 0 else 2

def check_winner():
    # Check horizontal, vertical, and diagonal connections
    for row in range(6):
        for col in range(8):
            if map[row][col] != 0 and (
                check_direction(row, col, 1, 0) or  # Horizontal
                check_direction(row, col, 0, 1) or  # Vertical
                check_direction(row, col, 1, 1) or  # Diagonal /
                check_direction(row, col, 1, -1)    # Diagonal \
            ):
                return map[row][col]
    return 0

def check_direction(row, col, delta_row, delta_col):
    current = map[row][col]
    for i in range(1, 4):
        new_row = row + delta_row * i
        new_col = col + delta_col * i
        if new_row < 0 or new_row >= 6 or new_col < 0 or new_col >= 8 or map[new_row][new_col] != current:
            return False
    return True

isRunning = True
game_over = False
winner = 0

while isRunning:
    screen.fill(GREEN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if computer and player == 1:
                continue
            mx, my = pygame.mouse.get_pos()
            sx = mx // 100  # Calculate column index based on mouse x-position
            lastRow = find_last(sx)
            if lastRow != -1:
                map[lastRow][sx] = get_player()
                winner = check_winner()  # Check for a winner after each move
                if winner != 0:
                    game_over = True
                player = not player

    # Draw the board and grid
    draw_lines()
    draw_board()
    draw_hud()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
