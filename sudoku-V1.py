import pygame
import random

# Initialize Pygame
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

# Fonts
FONT = pygame.font.SysFont("comicsans", 40)
FONT_SMALL = pygame.font.SysFont("comicsans", 20)

# Initialize the board
board = [[0 for _ in range(9)] for _ in range(9)]
original_board = [[0 for _ in range(9)] for _ in range(9)]

# Difficulty levels
difficulties = {
    "Easy": 20,
    "Medium": 30,
    "Hard": 40
}

# Button class to create and draw buttons
class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        # Draw the button rectangle
        pygame.draw.rect(win, BLUE, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 3)
        # Draw the button text
        text = FONT_SMALL.render(self.text, 1, WHITE)
        win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Check if the mouse position is over the button
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

# Buttons
solve_button = Button(425, 620, 100, 50, "Solve")
easy_button = Button(50, 620, 100, 50, "Easy")
medium_button = Button(175, 620, 100, 50, "Medium")
hard_button = Button(300, 620, 100, 50, "Hard")

# Draw the grid lines on the window
def draw_grid(win):
    gap = WIDTH // 9
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(win, BLACK, (0, i * gap), (WIDTH, i * gap), thickness)
        pygame.draw.line(win, BLACK, (i * gap, 0), (i * gap, WIDTH), thickness)

# Draw the numbers on the board
def draw_board(win, board):
    gap = WIDTH // 9
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                text = FONT.render(str(board[i][j]), 1, BLACK)
                win.blit(text, (j * gap + 20, i * gap + 15))

# Clear the board by setting all values to 0
def clear_board(board):
    for i in range(9):
        for j in range(9):
            board[i][j] = 0

# Generate a new puzzle with the given difficulty level
def generate_puzzle(board, difficulty):
    clear_board(board)
    fill_diagonal_boxes(board)
    fill_remaining(board, 0, 0)
    remove_digits(board, difficulty)
    # Store the original board for resetting
    for i in range(9):
        for j in range(9):
            original_board[i][j] = board[i][j]

# Fill the diagonal 3x3 boxes with random numbers
def fill_diagonal_boxes(board):
    for i in range(0, 9, 3):
        fill_box(board, i, i)

# Fill a 3x3 box with random numbers
def fill_box(board, row, col):
    num = random.sample(range(1, 10), 9)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = num.pop()

# Fill the remaining cells using backtracking
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

# Remove digits from the board based on the difficulty level
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

# Check if a number can be placed in a specific cell
def is_safe(board, row, col, num):
    # Check the row and column
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check the 3x3 box
    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

# Find the next empty cell
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# Solve the Sudoku puzzle using backtracking
def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
    return False

# Get the row and column from the mouse position
def get_mouse_pos(pos):
    x, y = pos
    gap = WIDTH // 9
    row = y // gap
    col = x // gap
    return row, col

# Draw the window with the board, buttons, and grid
def draw_window(win, board):
    win.fill(WHITE)
    draw_grid(win)
    draw_board(win, board)
    solve_button.draw(win)
    easy_button.draw(win)
    medium_button.draw(win)
    hard_button.draw(win)
    pygame.display.update()

# Reset the board to the original state
def reset_board():
    for i in range(9):
        for j in range(9):
            board[i][j] = original_board[i][j]

# Main game loop
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
                    if solve(board):
                        print("Solved successfully!")
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
                                key = None
                            else:
                                print("Invalid move!")
        draw_window(WIN, board)
        pygame.display.flip()
    pygame.quit()

# Entry point of the program
if __name__ == "__main__":
    main()

"""
Execution flow:

1. The program initializes Pygame and sets up the window dimensions, colors, and fonts.
2. The board and original_board lists are initialized to store the Sudoku puzzle.
3. The difficulty levels are defined in a dictionary.
4. The Button class is defined to create and draw buttons on the window.
5. The buttons for solving, and selecting difficulty levels are created.
6. The draw_grid function draws the grid lines on the window.
7. The draw_board function draws the numbers on the board.
8. The clear_board function sets all values on the board to 0.
9. The generate_puzzle function generates a new Sudoku puzzle based on the selected difficulty level.
10. The fill_diagonal_boxes function fills the diagonal 3x3 boxes with random numbers.
11. The fill_box function fills a 3x3 box with random numbers.
12. The fill_remaining function fills the remaining cells using backtracking.
13. The remove_digits function removes digits from the board based on the difficulty level.
14. The is_safe function checks if a number can be placed in a specific cell.
15. The find_empty function finds the next empty cell on the board.
16. The solve function solves the Sudoku puzzle using backtracking.
17. The get_mouse_pos function gets the row and column from the mouse position.
18. The draw_window function draws the window with the board, buttons, and grid.
19. The reset_board function resets the board to the original state.
20. The main function is the game loop that handles user input and updates the game state.
21. The program starts by calling the main function.

Features:
- Generate Sudoku puzzles with different difficulty levels (Easy, Medium, Hard)
- Solve the puzzle using the "Solve" button
- User can input numbers by clicking on the cells and typing on the keyboard
- Invalid moves are prevented
- Reset the board to the original state
- Display messages for successful and failed solving attempts
"""
