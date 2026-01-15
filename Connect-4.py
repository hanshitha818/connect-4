import pygame
import numpy as np
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time

# Constants
ROWS = 6  # Number of rows on the board
COLS = 7  # Number of columns on the board
SQUARESIZE = 100  # Size of each square on the board
RADIUS = SQUARESIZE // 2 - 5  # Radius of the discs

# Colors
COLOR_OPTIONS = [
    ("Tan", (230, 219, 172)), 
    ("Beige", (238, 220, 154)),  
    ("Macaroon", (249, 224, 118)), 
    ("Hazel Wood", (201, 187, 142)), 
    ("Granola", (214, 184, 90)), 
    ("Oat", (223, 201, 138)), 
    ("Egg Nog", (250, 226, 156)), 
    ("Fawn", (200, 169, 81)), 
    ("Sugar Cookie", (243, 234, 175)), 
    ("Sand", (216, 184, 99)), 
    ("Sepia", (227, 183, 120)), 
    ("Latte", (231, 194, 125)), 
    ("Oyster", (220, 215, 160)), 
    ("Biscotti", (227, 197, 101)), 
    ("Parmesan", (253, 233, 146)), 
    ("Hazelnut", (189, 165, 93))
]


GREY = (192, 192, 192)  # Background color
BLACK = (0, 0, 0)  # Player's disc color
WHITE = (255, 255, 255)  # AI's disc color

PLAYER_DISC = 1  # Represents player's disc in the board array
AI_DISC = 2  # Represents AI's disc in the board array


# Function to create an empty game board
def initialize_board():
    return np.zeros((ROWS, COLS), dtype=int)


# Function to draw the game board and the discs
def render_board(board, screen, board_color):
    screen.fill(GREY)  # Fill the screen with the background color
    for col in range(COLS):
        for row in range(ROWS):
            pygame.draw.rect(screen, board_color, (col * SQUARESIZE, (row + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, GREY, 
                               (int(col * SQUARESIZE + SQUARESIZE / 2), int((row + 1) * SQUARESIZE + SQUARESIZE / 2)),
                               RADIUS)
    # Draw the discs
    for col in range(COLS):
        for row in range(ROWS):
            if board[row][col] == PLAYER_DISC:
                pygame.draw.circle(screen, BLACK,
                                   (int(col * SQUARESIZE + SQUARESIZE / 2), int((ROWS - row) * SQUARESIZE + SQUARESIZE / 2)),
                                   RADIUS)
            elif board[row][col] == AI_DISC:
                pygame.draw.circle(screen, WHITE,
                                   (int(col * SQUARESIZE + SQUARESIZE / 2), int((ROWS - row) * SQUARESIZE + SQUARESIZE / 2)),
                                   RADIUS)
    pygame.display.update()  # Refresh the display


# Function to place a disc in the specified column
def place_disc(board, row, col, disc):
    board[row][col] = disc


# Check if the selected column has space for a disc
def is_column_valid(board, col):
    return board[ROWS - 1][col] == 0


# Get the next available row in the selected column
def get_available_row(board, col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row


# Check if the current piece has formed a 2x2 square win
def check_square_win(board, disc):
    for row in range(ROWS - 1):
        for col in range(COLS - 1):
            if (board[row][col] == disc and
                    board[row][col + 1] == disc and
                    board[row + 1][col] == disc and
                    board[row + 1][col + 1] == disc):
                return True, (row, col)  # Return top-left coordinates of winning square
    return False, None


# Get all valid column indices where a move is possible
def get_valid_columns(board):
    return [col for col in range(COLS) if is_column_valid(board, col)]


# Evaluate the score of a window of 4 positions
def evaluate_window(window, disc):
    opponent_disc = PLAYER_DISC if disc == AI_DISC else AI_DISC
    if window.count(disc) == 4:
        return 100
    elif window.count(disc) == 3 and window.count(0) == 1:
        return 5
    elif window.count(disc) == 2 and window.count(0) == 2:
        return 2
    if window.count(opponent_disc) == 3 and window.count(0) == 1:
        return -4
    return 0


# Calculate the total score for the given board state
def calculate_score(board, disc):
    score = 0
    center_array = [int(i) for i in list(board[:, COLS // 2])]
    center_count = center_array.count(disc)
    score += center_count * 3  # Central column bonus

    # Score horizontal windows
    for row in range(ROWS):
        row_array = [int(i) for i in list(board[row, :])]
        for col in range(COLS - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, disc)

    # Score vertical windows
    for col in range(COLS):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(ROWS - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, disc)

    return score


# Check if the game is over due to a win or a draw
def is_game_over(board):
    return check_square_win(board, PLAYER_DISC)[0] or check_square_win(board, AI_DISC)[0] or len(get_valid_columns(board)) == 0


# Minimax algorithm for AI decision-making with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_columns = get_valid_columns(board)
    if depth == 0 or is_game_over(board):
        if is_game_over(board):
            if check_square_win(board, AI_DISC)[0]:
                return (None, 100000)
            elif check_square_win(board, PLAYER_DISC)[0]:
                return (None, -100000)
            else:
                return (None, 0)
        else:
            return (None, calculate_score(board, AI_DISC))

    if maximizing_player:
        value = -np.inf
        column = random.choice(valid_columns)
        for col in valid_columns:
            row = get_available_row(board, col)
            board_copy = board.copy()
            place_disc(board_copy, row, col, AI_DISC)
            new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = np.inf
        column = random.choice(valid_columns)
        for col in valid_columns:
            row = get_available_row(board, col)
            board_copy = board.copy()
            place_disc(board_copy, row, col, PLAYER_DISC)
            new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def main():
    root = tk.Tk()
    root.withdraw()

    # Prompt user for game setup details
    color_names = "\n".join([f"{i+1}. {name}" for i, (name, _) in enumerate(COLOR_OPTIONS)])
    while True:
        try:
            color_index = simpledialog.askinteger("Input", f"Choose Board Color:\n{color_names}", minvalue=1, maxvalue=16)
            player_name = ""
            while not player_name.strip():
                player_name = simpledialog.askstring("Input", "Enter Player Name:").strip()
                if not player_name:
                    messagebox.showerror("Error", "Player name cannot be empty.")
            
            while True:
                first_player = simpledialog.askstring(
                    "Input", f"Who plays first? ('{player_name}' or 'AI'):"
                ).strip().lower()
                
                if first_player in [player_name.lower(), "ai"]:
                    break
                else:
                    messagebox.showerror("Error", f"Invalid input! Please enter '{player_name}' or 'AI'.")
            
            minimax_depth = simpledialog.askinteger("Input", "Enter Minimax Depth (1-5):", minvalue=1, maxvalue=5)
            break
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            sys.exit()

    pygame.init()
    board_color = COLOR_OPTIONS[color_index - 1][1]
    screen = pygame.display.set_mode((COLS * SQUARESIZE, (ROWS + 1) * SQUARESIZE))
    board = initialize_board()
    render_board(board, screen, board_color)

    game_over = False
    turn = 0 if first_player == player_name.lower() else 1
    moves = 0
    start_time = time.time()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, GREY, (0, 0, COLS * SQUARESIZE, SQUARESIZE))
                x_pos = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, BLACK, (x_pos, SQUARESIZE // 2), RADIUS)
                pygame.display.update()

            if turn == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                col = x_pos // SQUARESIZE
                if is_column_valid(board, col):
                    row = get_available_row(board, col)
                    place_disc(board, row, col, PLAYER_DISC)
                    moves += 1

                    won, winning_block = check_square_win(board, PLAYER_DISC)
                    if won:
                        messagebox.showinfo("Game Over", f"{player_name} Wins!")
                        display_game_stats(player_name, moves, start_time)
                        game_over = True
                    render_board(board, screen, board_color)
                    turn = 1

            elif turn == 1:
                col, _ = minimax(board, minimax_depth, -np.inf, np.inf, True)
                if is_column_valid(board, col):
                    row = get_available_row(board, col)
                    pygame.time.wait(500)
                    place_disc(board, row, col, AI_DISC)
                    moves += 1

                    won, winning_block = check_square_win(board, AI_DISC)
                    if won:
                        render_board(board, screen, board_color)
                        messagebox.showinfo("Game Over", "AI Wins!")
                        display_game_stats("AI", moves, start_time)
                        game_over = True
                    render_board(board, screen, board_color)
                    turn = 0

            if len(get_valid_columns(board)) == 0 and not game_over:
                messagebox.showinfo("Draw", "It's a draw!")
                display_game_stats("Draw", moves, start_time)
                game_over = True

    pygame.quit()
    sys.exit()


# Function to display game statistics after a game ends
def display_game_stats(winner, moves, start_time):
    total_time = time.time() - start_time
    print(f"--- Game Summary ---\nWinner: {winner}\nTotal Moves: {moves}\nTime Elapsed: {total_time:.2f} seconds")


if __name__ == "__main__":

    main()
