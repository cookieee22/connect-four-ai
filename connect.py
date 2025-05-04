import numpy as np
import random

# Constants
ROWS = 6
COLS = 7
PLAYER = 1
AI = 2
EMPTY = 0
WIN_LENGTH = 4  # Four in a row to win

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_move(board, col):
    return board[0][col] == EMPTY

def get_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row

def print_board(board):
    print(np.flip(board, 0))

def is_winning_move(board, piece):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(WIN_LENGTH)):
                return True

    return False

def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]

def evaluate_board(board, piece):
    score = 0
    center_col = [int(board[r][COLS // 2]) for r in range(ROWS)]
    score += center_col.count(piece) * 3

    for r in range(ROWS):
        for c in range(COLS - 3):
            window = [board[r][c + i] for i in range(WIN_LENGTH)]
            score += score_window(window, piece)

    for c in range(COLS):
        for r in range(ROWS - 3):
            window = [board[r + i][c] for i in range(WIN_LENGTH)]
            score += score_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + i][c + i] for i in range(WIN_LENGTH)]
            score += score_window(window, piece)

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(WIN_LENGTH)]
            score += score_window(window, piece)

    return score

def score_window(window, piece):
    score = 0
    opp_piece = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def minimax(board, depth, alpha, beta, maximizing):
    valid_moves = get_valid_moves(board)
    terminal = (
        is_winning_move(board, PLAYER)
        or is_winning_move(board, AI)
        or len(valid_moves) == 0
    )

    if depth == 0 or terminal:
        if is_winning_move(board, AI):
            return (None, 1000000)
        elif is_winning_move(board, PLAYER):
            return (None, -1000000)
        else:
            return (None, evaluate_board(board, AI))

    if maximizing:
        best_score = -float("inf")
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            row = get_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]

            if new_score > best_score:
                best_score = new_score
                best_col = col

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_col, best_score
    else:
        best_score = float("inf")
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            row = get_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]

            if new_score < best_score:
                best_score = new_score
                best_col = col

            beta = min(beta, best_score)
            if alpha >= beta:
                break

        return best_col, best_score

def get_ai_move(board):
    print("AI is thinking...")
    col, _ = minimax(board, 5, -float("inf"), float("inf"), True)
    return col

def play_game():
    board = create_board()
    print_board(board)
    game_over = False
    turn = random.randint(0, 1)

    while not game_over:
        if turn == 0:  # Player's turn
            # --- Enhanced input validation ---
            try:
                col = int(input("Enter your column (0-6): "))
                if col < 0 or col >= COLS:
                    print("Invalid column. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 0-6.")
                continue
            # ---------------------------------

            if is_valid_move(board, col):
                row = get_open_row(board, col)
                drop_piece(board, row, col, PLAYER)

                if is_winning_move(board, PLAYER):
                    print_board(board)
                    print("Congratulations! You win!")
                    game_over = True
        else:  # AI's turn
            col = get_ai_move(board)
            if is_valid_move(board, col):
                row = get_open_row(board, col)
                drop_piece(board, row, col, AI)

                if is_winning_move(board, AI):
                    print_board(board)
                    print("AI wins! Better luck next time.")
                    game_over = True

        print_board(board)
        turn = (turn + 1) % 2  # Switch turns

        if len(get_valid_moves(board)) == 0 and not game_over:
            print("It's a tie!")
            game_over = True

play_game()



