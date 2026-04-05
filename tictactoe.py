import sys
import os

# ── ANSI helpers ─────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

# Foreground colours
RED    = "\033[91m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"

# Background colours for cells
BG_DARK  = "\033[48;5;236m"   # dark grey cell
BG_X     = "\033[48;5;52m"    # deep red cell (X occupied)
BG_O     = "\033[48;5;17m"    # deep blue cell (O occupied)
BG_WIN   = "\033[48;5;58m"    # olive highlight for winning cells

def clr(text, *codes):
    return "".join(codes) + text + RESET

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ── Board rendering ───────────────────────────────────────────────────────────

# Box-drawing pieces
TOP    = "╔═══════╦═══════╦═══════╗"
MID    = "╠═══════╬═══════╬═══════╣"
BOT    = "╚═══════╩═══════╩═══════╝"
SEP    = "║"

def cell_lines(value, index, win_cells):
    """Return the three display lines for a single cell."""
    num = str(index + 1)
    occupied = value in ("X", "O")

    if index in win_cells:
        bg = BG_WIN
    elif value == "X":
        bg = BG_X
    elif value == "O":
        bg = BG_O
    else:
        bg = BG_DARK

    pad = bg + "       " + RESET

    if value == "X":
        symbol = clr(" ╲ ╱ ", bg + BOLD + RED)
        middle = bg + "  " + symbol + "  " + RESET
        symbol2 = clr(" ╱ ╲ ", bg + BOLD + RED)
        # squish into 3 lines: top-pad, X-glyph, bot-pad
        top_line  = bg + "  " + clr("╲   ╱", BOLD + RED) + "  " + RESET
        mid_line  = bg + "   " + clr("╳", BOLD + RED) + "   " + RESET
        bot_line  = bg + "  " + clr("╱   ╲", BOLD + RED) + "  " + RESET
    elif value == "O":
        top_line  = bg + "  " + clr("╭───╮", BOLD + BLUE) + "  " + RESET
        mid_line  = bg + "  " + clr("│   │", BOLD + BLUE) + "  " + RESET
        bot_line  = bg + "  " + clr("╰───╯", BOLD + BLUE) + "  " + RESET
    else:
        hint = clr(num, GRAY + DIM)
        top_line  = pad
        mid_line  = bg + "   " + hint + "   " + RESET
        bot_line  = pad

    return top_line, mid_line, bot_line


def print_board(board, win_cells=(), title=""):
    print()
    if title:
        print("  " + clr(title, BOLD + CYAN))
        print()

    rows = [board[0:3], board[3:6], board[6:9]]
    indices = [range(0, 3), range(3, 6), range(6, 9)]

    print("  " + clr(TOP, GRAY))
    for r, row_idx in enumerate(indices):
        tops, mids, bots = [], [], []
        for ci in row_idx:
            t, m, b = cell_lines(board[ci], ci, win_cells)
            tops.append(t); mids.append(m); bots.append(b)

        sep = clr(SEP, GRAY)
        print("  " + sep + tops[0] + sep + tops[1] + sep + tops[2] + sep)
        print("  " + sep + mids[0] + sep + mids[1] + sep + mids[2] + sep)
        print("  " + sep + bots[0] + sep + bots[1] + sep + bots[2] + sep)

        if r < 2:
            print("  " + clr(MID, GRAY))

    print("  " + clr(BOT, GRAY))
    print()


def print_title():
    clear()
    print()
    print(clr("  ╔╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╗", CYAN + BOLD))
    print(clr("  ╠╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣", CYAN + BOLD))
    print(clr("  ║  ", CYAN + BOLD) +
          clr("T I C", RED + BOLD) + "  " +
          clr("T A C", WHITE + BOLD) + "  " +
          clr("T O E", BLUE + BOLD) +
          clr("  ║", CYAN + BOLD))
    print(clr("  ╠╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣", CYAN + BOLD))
    print(clr("  ╚╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╝", CYAN + BOLD))
    print()

# ── Game logic ────────────────────────────────────────────────────────────────

WINS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6],
]

def check_winner(board):
    for a, b, c in WINS:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a], (a, b, c)
    return None, ()


def get_player_move(board, player):
    colour = RED if player == "X" else BLUE
    label = clr(f"Player {player}", BOLD + colour)
    while True:
        print(f"  {label} — enter position (1-9): ", end='', flush=True)
        try:
            raw = input()
        except EOFError:
            sys.exit(0)
        try:
            pos = int(raw) - 1
        except ValueError:
            print(clr("  ✗  Please enter a number 1–9.", YELLOW))
            continue
        if pos < 0 or pos > 8:
            print(clr("  ✗  Out of range! Enter 1–9.", YELLOW))
        elif board[pos] != ' ':
            print(clr("  ✗  That spot is taken.", YELLOW))
        else:
            return pos


def get_ai_move(board, ai_mark, human_mark):
    for i in range(9):
        if board[i] == ' ':
            board[i] = ai_mark
            if check_winner(board)[0]:
                board[i] = ' '
                return i
            board[i] = ' '
    for i in range(9):
        if board[i] == ' ':
            board[i] = human_mark
            if check_winner(board)[0]:
                board[i] = ' '
                return i
            board[i] = ' '
    if board[4] == ' ':
        return 4
    for i in [0, 2, 6, 8]:
        if board[i] == ' ':
            return i
    for i in range(9):
        if board[i] == ' ':
            return i


def play_game(vs_ai):
    board = [' '] * 9
    players = ['X', 'O']
    turn = 0

    for move_num in range(9):
        player = players[turn % 2]
        clear()

        mode_tag = "vs AI" if vs_ai else "2 Players"
        print_board(board, title=f"Tic-Tac-Toe  [{mode_tag}]  —  Move {move_num + 1}")

        if vs_ai and player == 'O':
            print(clr("  AI is thinking…", GRAY + DIM))
            pos = get_ai_move(board, 'O', 'X')
            print(clr(f"  AI chose position {pos + 1}", GRAY))
        else:
            pos = get_player_move(board, player)

        board[pos] = player
        winner, win_cells = check_winner(board)

        if winner:
            clear()
            colour = RED if winner == "X" else BLUE
            if vs_ai and winner == 'O':
                msg = clr("  ★  AI wins!  Better luck next time.", BOLD + BLUE)
            else:
                msg = clr(f"  ★  Player {winner} wins!  Congratulations!", BOLD + colour)
            print_board(board, win_cells=set(win_cells), title="Game Over")
            print(msg)
            print()
            return

        turn += 1

    clear()
    print_board(board, title="Game Over")
    print(clr("  ═  It's a draw!  Well played both sides.", BOLD + YELLOW))
    print()


def main():
    while True:
        print_title()
        print(clr("  [1]", BOLD + WHITE) + "  Two players")
        print(clr("  [2]", BOLD + WHITE) + "  Play vs AI")
        print(clr("  [q]", BOLD + WHITE) + "  Quit")
        print()
        print("  Choose: ", end='', flush=True)

        try:
            choice = input().strip().lower()
        except EOFError:
            break

        if choice == 'q':
            clear()
            print(clr("\n  Goodbye! Thanks for playing.\n", BOLD + CYAN))
            break
        elif choice == '1':
            play_game(vs_ai=False)
        elif choice == '2':
            play_game(vs_ai=True)
        else:
            continue

        print("  Play again? (y/n): ", end='', flush=True)
        try:
            again = input().strip().lower()
        except EOFError:
            break
        if again != 'y':
            clear()
            print(clr("\n  Goodbye! Thanks for playing.\n", BOLD + CYAN))
            break


if __name__ == '__main__':
    main()
