import sys
import random


def print_board(board):
    print()
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---+---+---")
    print()


def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [2, 4, 6]               # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None


def get_player_move(board, player):
    while True:
        print(f"Player {player}'s turn. Enter position (1-9): ", end='', flush=True)
        try:
            pos = int(input()) - 1
        except ValueError:
            print("Invalid input. Please enter a number 1-9.")
            continue
        except EOFError:
            sys.exit(0)
        if pos < 0 or pos > 8:
            print("Out of range! Enter a number 1-9.")
        elif board[pos] != ' ':
            print("That spot is taken! Choose another.")
        else:
            return pos


def get_ai_move(board, ai_mark, human_mark):
    # 1. Win if possible
    for i in range(9):
        if board[i] == ' ':
            board[i] = ai_mark
            if check_winner(board):
                board[i] = ' '
                return i
            board[i] = ' '
    # 2. Block human win
    for i in range(9):
        if board[i] == ' ':
            board[i] = human_mark
            if check_winner(board):
                board[i] = ' '
                return i
            board[i] = ' '
    # 3. Take center
    if board[4] == ' ':
        return 4
    # 4. Take a corner
    for i in [0, 2, 6, 8]:
        if board[i] == ' ':
            return i
    # 5. Take any open spot
    for i in range(9):
        if board[i] == ' ':
            return i


def play_game(vs_ai):
    board = [' '] * 9
    players = ['X', 'O']
    turn = 0

    print_board(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

    for _ in range(9):
        player = players[turn % 2]
        print_board(board)

        if vs_ai and player == 'O':
            print("AI is thinking...")
            pos = get_ai_move(board, 'O', 'X')
            print(f"AI chose position {pos + 1}")
        else:
            pos = get_player_move(board, player)

        board[pos] = player
        winner = check_winner(board)

        if winner:
            print_board(board)
            if vs_ai and winner == 'O':
                print("AI wins!")
            else:
                print(f"Player {winner} wins!")
            return

        turn += 1

    print_board(board)
    print("It's a draw!")


def main():
    print("=== Tic Tac Toe ===")

    while True:
        print("\nMode: [1] Two players  [2] vs AI  [q] Quit")
        try:
            choice = input("Choose: ").strip().lower()
        except EOFError:
            break

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == '1':
            play_game(vs_ai=False)
        elif choice == '2':
            play_game(vs_ai=True)
        else:
            print("Invalid choice.")
            continue

        try:
            again = input("Play again? (y/n): ").strip().lower()
        except EOFError:
            break
        if again != 'y':
            print("Goodbye!")
            break


if __name__ == '__main__':
    main()
