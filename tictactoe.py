import sys

def print_board(board):
    print()
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---+---+---")
    print()

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # cols
        [0,4,8],[2,4,6]           # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None

def play():
    board = [' '] * 9
    players = ['X', 'O']
    turn = 0

    print("Tic Tac Toe!")
    print("Positions: 1-9 (left-to-right, top-to-bottom)")
    print_board(['1','2','3','4','5','6','7','8','9'])

    for move_num in range(9):
        player = players[turn % 2]
        print_board(board)
        print(f"Player {player}'s turn. Enter position (1-9): ", end='', flush=True)

        try:
            pos = int(input()) - 1
        except (ValueError, EOFError):
            print("\nInvalid input. Exiting.")
            sys.exit(1)

        if pos < 0 or pos > 8 or board[pos] != ' ':
            print("Invalid move! Try again.")
            continue

        board[pos] = player
        winner = check_winner(board)

        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            return

        turn += 1

    print_board(board)
    print("It's a draw!")

if __name__ == '__main__':
    play()
