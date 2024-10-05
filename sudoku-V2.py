import pygame
import random
import time

pygame.init()

# Window dimensions and colors
WIDTH, HEIGHT = 600, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
FONT = pygame.font.SysFont("comicsans", 40)
FONT_SMALL = pygame.font.SysFont("comicsans", 20)

# Initialize the board
board = [[0 for _ in range(9)] for _ in range(9)]
original_board = [[0 for _ in range(9)] for _ in range(9)]
solved_cells = [[False for _ in range(9)] for _ in range(9)]

# Difficulty levels
difficulties = {
    "Easy": 20,
    "Medium": 30,
    "Hard": 40
}

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, BLUE, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 3)
        text = FONT_SMALL.render(self.text, 1, WHITE)
        win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

# Buttons
solve_button = Button(425, 620, 100, 50, "Solve")
easy_button = Button(50, 620, 100, 50, "Easy")
medium_button = Button(175, 620, 100, 50, "Medium")
hard_button = Button(300, 620, 100, 50, "Hard")

def draw_grid(win):
    gap = WIDTH // 9
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(win, BLACK, (0, i * gap), (WIDTH, i * gap), thickness)
        pygame.draw.line(win, BLACK, (i * gap, 0), (i * gap, WIDTH), thickness)

def draw_board(win, board, highlight=None):
    gap = WIDTH // 9
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                color = RED if solved_cells[i][j] else BLACK
                text = FONT.render(str(board[i][j]), 1, color)
                win.blit(text, (j * gap + 20, i * gap + 15))
            if highlight and highlight == (i, j):
                pygame.draw.rect(win, YELLOW, (j * gap, i * gap, gap, gap), 3)

def clear_board(board):
    for i in range(9):
        for j in range(9):
            board[i][j] = 0
            solved_cells[i][j] = False

def generate_puzzle(board, difficulty):
    clear_board(board)
    fill_diagonal_boxes(board)
    fill_remaining(board, 0, 0)
    remove_digits(board, difficulty)
    for i in range(9):
        for j in range(9):
            original_board[i][j] = board[i][j]
            solved_cells[i][j] = False

def fill_diagonal_boxes(board):
    for i in range(0, 9, 3):
        fill_box(board, i, i)

def fill_box(board, row, col):
    num = random.sample(range(1, 10), 9)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = num.pop()

def fill_remaining(board, i, j):
    if j >= 9 and i < 8:
        i += 1
        j = 0
    if i >= 9 and j >= 9:
        return True
    if i < 3:
        if j < 3:
            j = 3
    elif i < 6:
        if j == (i // 3) * 3:
            j += 3
    else:
        if j == 6:
            i += 1
            j = 0
            if i >= 9:
                return True
    for num in range(1, 10):
        if is_safe(board, i, j, num):
            board[i][j] = num
            if fill_remaining(board, i, j + 1):
                return True
            board[i][j] = 0
    return False

def remove_digits(board, difficulty):
    count = difficulties[difficulty]
    while count != 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        board[row][col] = 0
        count -= 1

def is_safe(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_with_animation(board, win):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            solved_cells[row][col] = True
            animate_number_selection(win, board, row, col, num)
            pygame.event.pump()  # Process events to keep the window responsive
            if solve_with_animation(board, win):
                return True
            board[row][col] = 0
            solved_cells[row][col] = False
            animate_number_selection(win, board, row, col, 0)
            pygame.event.pump()  # Process events to keep the window responsive
    return False

def animate_number_selection(win, board, row, col, final_num):
    gap = WIDTH // 9
    for num in range(1, 10):
        pygame.draw.rect(win, WHITE, (col * gap + 1, row * gap + 1, gap - 1, gap - 1))
        text = FONT.render(str(num), 1, RED)
        win.blit(text, (col * gap + 20, row * gap + 15))
        pygame.display.update()
        pygame.time.delay(50)
    pygame.draw.rect(win, WHITE, (col * gap + 1, row * gap + 1, gap - 1, gap - 1))
    if final_num != 0:
        text = FONT.render(str(final_num), 1, RED)
        win.blit(text, (col * gap + 20, row * gap + 15))
    pygame.display.update()
    pygame.time.delay(100)

def get_mouse_pos(pos):
    x, y = pos
    gap = WIDTH // 9
    row = y // gap
    col = x // gap
    return row, col

def draw_window(win, board):
    win.fill(WHITE)
    draw_grid(win)
    draw_board(win, board)
    solve_button.draw(win)
    easy_button.draw(win)
    medium_button.draw(win)
    hard_button.draw(win)
    pygame.display.update()

def reset_board():
    for i in range(9):
        for j in range(9):
            board[i][j] = original_board[i][j]
            solved_cells[i][j] = False

def main():
    run = True
    key = None
    difficulty = "Easy"
    generate_puzzle(board, difficulty)
    row, col = None, None
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if solve_button.is_over(pos):
                    reset_board()
                    start_time = time.time()
                    if solve_with_animation(board, WIN):
                        end_time = time.time()
                        solve_time = end_time - start_time
                        print(f"Solved successfully in {solve_time:.2f} seconds!")
                    else:
                        print("Failed to solve.")
                elif easy_button.is_over(pos):
                    difficulty = "Easy"
                    generate_puzzle(board, difficulty)
                elif medium_button.is_over(pos):
                    difficulty = "Medium"
                    generate_puzzle(board, difficulty)
                elif hard_button.is_over(pos):
                    difficulty = "Hard"
                    generate_puzzle(board, difficulty)
                else:
                    row, col = get_mouse_pos(pos)
                    if row is not None and col is not None:
                        if original_board[row][col] == 0:
                            key = None
            if event.type == pygame.KEYDOWN:
                if row is not None and col is not None:
                    if original_board[row][col] == 0:
                        if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                            key = 1
                        elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                            key = 2
                        elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                            key = 3
                        elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                            key = 4
                        elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                            key = 5
                        elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                            key = 6
                        elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                            key = 7
                        elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                            key = 8
                        elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                            key = 9
                        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                            key = 0
                        if key is not None:
                            if key == 0 or is_safe(board, row, col, key):
                                board[row][col] = key
                                solved_cells[row][col] = False
                                key = None
                            else:
                                print("Invalid move!")
        draw_window(WIN, board)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
