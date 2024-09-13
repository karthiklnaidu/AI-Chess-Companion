import chess
import minmax

def print_board(board):
    print(board)
    print("")
    
def AI(board):
    best_move = None
    best_value = -float('inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minmax.minmax(board, depth, False)
        board.pop()
        
        if best_value < board_value:
            best_value = board_value
            best_move = move
    return best_move

def engine(board, move):
    # Initialize the board

    print("Welcome to Chess!")
    print("Enter moves in UCI format (e.g., e2e4, e7e5, etc.)")
    print_board(board)

    try:
        board.push_uci(move)
    except ValueError:
        print("Invalid move! Please enter a valid move.")
        

    if board.is_game_over():
        result = board.result()
        if result == "1-0":
            print("You win!")
        elif result == "0-1":
            print("You lose!")
        else:
            print("It's a draw!")
        

        # Engine's move
        # result = engine.play(board, chess.engine.Limit(time=2.0))
        
    move = AI(board)
    board.push(move)

    print(" ")
    print_board(board)

    result = board.result()
    if result == "1-0":
        print("You win!")
    if result == "0-1":
        print("You lose!")

    return board

if __name__ == "__main__":
    depth = 2
    engine()