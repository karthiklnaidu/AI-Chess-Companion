import chess

def evaluate_board(board):
    piece_value = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    
    piece_square_tables = {
        chess.PAWN: [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 5, 10, 10, 10, 10, 5, 5],
            [1, 1, 2, 5, 5, 2, 1, 1],
            [0, 0, 0, 3, 3, 0, 0, 0],
            [0, 0, 0, 3, 3, 0, 0, 0],
            [0, 0, 0, 2, 2, 0, 0, 0],
            [1, 1, 2, 0, 0, 2, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        chess.KNIGHT: [
            [-5, -4, -3, -3, -3, -3, -4, -5],
            [-4, -2, 0, 1, 1, 0, -2, -4],
            [-3, 1, 2, 3, 3, 2, 1, -3],
            [-3, 1, 3, 4, 4, 3, 1, -3],
            [-3, 1, 3, 4, 4, 3, 1, -3],
            [-3, 1, 2, 3, 3, 2, 1, -3],
            [-4, -2, 0, 1, 1, 0, -2, -4],
            [-5, -4, -3, -3, -3, -3, -4, -5]
        ],
        chess.BISHOP: [
            [-2, -1, -1, -1, -1, -1, -1, -2],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-2, -1, -1, -1, -1, -1, -1, -2]
        ],
        chess.ROOK: [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 2, 2, 2, 1, 0],
            [0, 1, 2, 3, 3, 2, 1, 0],
            [0, 1, 2, 3, 3, 2, 1, 0],
            [0, 1, 2, 2, 2, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        chess.QUEEN: [
            [-2, -1, -1, 0, 0, -1, -1, -2],
            [-1, 0, 0, 1, 1, 0, 0, -1],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-2, -1, -1, 0, 0, -1, -1, -2]
        ],
        chess.KING: [
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-2, -3, -3, -4, -4, -3, -3, -2],
            [-1, -2, -2, -3, -3, -2, -2, -1],
            [2, 2, 0, 0, 0, 0, 2, 2],
            [2, 2, 1, 0, 0, 1, 2, 2]
        ]
    }
    if board.is_checkmate():
        return float('inf') if board.turn == chess.WHITE else -float('inf')
    elif board.is_stalemate():
        return 0  


    material_count = 0
    material_count = sum(
        piece_value[piece.piece_type] * (1 if piece.color == chess.BLACK else -1)
        for piece in board.piece_map().values()
    )
        

    piece_square_score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_val = piece_value[piece.piece_type]
            piece_square_value = piece_square_tables[piece.piece_type][7 - chess.square_rank(square)][chess.square_file(square)]
            piece_square_score += (piece_val + piece_square_value) if piece.color == chess.BLACK else -(piece_val + piece_square_value)
    
    return material_count + piece_square_score

def minmax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
        
    if maximizing_player:
        max_value = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = minmax(board, depth-1, alpha, beta, False)
            board.pop()
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return max_value
    else:
        min_value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = minmax(board, depth-1, alpha, beta, True)
            board.pop()
            min_value = min(min_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_value
        
        