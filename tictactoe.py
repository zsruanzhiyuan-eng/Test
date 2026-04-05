import os

# Colors
R = "\033[91m"   # Red
B = "\033[94m"   # Blue
Y = "\033[93m"   # Yellow
G = "\033[92m"   # Green
W = "\033[97m"   # White
DIM = "\033[2m"  # Dim
RESET = "\033[0m"
BOLD = "\033[1m"
BG = "\033[100m" # Dark background

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def color_cell(cell):
    if cell == "X":
        return f"{R}{BOLD} X {RESET}"
    elif cell == "O":
        return f"{B}{BOLD} O {RESET}"
    else:
        return f"{DIM} {cell} {RESET}"

def print_board(board):
    nums = ["1","2","3","4","5","6","7","8","9"]
    idx = 0
    print(f"\n{W}  ╔═══╦═══╦═══╗{RESET}")
    for i, row in enumerate(board):
        line = f"{W}  ║{RESET}"
        for cell in row:
            display = color_cell(cell) if cell != " " else f"{DIM} {nums[idx]} {RESET}"
            if cell == " ":
                idx += 1
            else:
                idx += 1
            line += display + f"{W}║{RESET}"
        print(line)
        if i < 2:
            print(f"{W}  ╠═══╬═══╬═══╣{RESET}")
    print(f"{W}  ╚═══╩═══╩═══╝{RESET}")

def print_header():
    print(f"\n{Y}{BOLD}  ╔══════════════════╗")
    print(f"  ║   TIC  TAC  TOE  ║")
    print(f"  ╚══════════════════╝{RESET}")

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def get_move(board, player):
    color = R if player == "X" else B
    while True:
        try:
            move = int(input(f"\n  {color}{BOLD}Player {player}{RESET} — pick a spot {W}(1-9):{RESET} ")) - 1
            row, col = divmod(move, 3)
            if 0 <= move <= 8 and board[row][col] == " ":
                return row, col
            else:
                print(f"  {Y}That spot is taken or invalid. Try again.{RESET}")
        except (ValueError, IndexError):
            print(f"  {Y}Enter a number between 1 and 9.{RESET}")

def play():
    board = [[" "] * 3 for _ in range(3)]
    players = ["X", "O"]

    clear()
    print_header()
    print(f"\n  {DIM}Each number = that position on the board{RESET}")
    print_board(board)

    for turn in range(9):
        player = players[turn % 2]
        row, col = get_move(board, player)
        board[row][col] = player

        clear()
        print_header()
        print_board(board)

        if check_winner(board, player):
            color = R if player == "X" else B
            print(f"\n  {color}{BOLD}🎉 Player {player} wins! Congratulations!{RESET}\n")
            return

    print(f"\n  {Y}{BOLD}It's a draw! Well played both!{RESET}\n")

if __name__ == "__main__":
    while True:
        play()
        again = input(f"  {W}Play again? (y/n):{RESET} ").strip().lower()
        if again != "y":
            print(f"\n  {G}Thanks for playing! Bye! 👋{RESET}\n")
            break
