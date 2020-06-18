"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flattened = [inner for outer in board for inner in outer]

    return O if flattened.count(X) > flattened.count(O) else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    rows, cols = len(board), len(board[0])

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == EMPTY:
                moves.add((i,j))
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if not 0 <= i < len(board)\
    or not 0 <= j < len(board[0]):
        raise ValueError("This is not a valid position on the board")

    result_board = deepcopy(board)
    result_board[i][j] = player(board)

    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winning_combos = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
    ]

    for line in winning_combos:
        a, b, c = line
        a, b, c = divmod(a, len(board)), divmod(b, len(board)), divmod(c, len(board))

        if board[a[0]][a[1]]\
        and board[a[0]][a[1]] == board[b[0]][b[1]] and\
        board[b[0]][b[1]] == board[c[0]][c[1]]:
            return board[a[0]][a[1]]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    flattened = [inner for outer in board for inner in outer]
    if all(flattened):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    the_winner = winner(board)
    if the_winner == X:
        return 1
    elif the_winner == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    

    def max_value(state, alpha, beta):

        if terminal(state):
            return (EMPTY, utility(state))

        v = (EMPTY, -2)

        for action in actions(state):
            v = max(v, 
                (action, min_value(result(state, action), alpha, beta)[1]), 
                key=lambda x: x[1])
            
            alpha = max(v[1], alpha)
            if alpha >= beta:
                break

        return v

    def min_value(state, alpha, beta):

        if terminal(state):
            return (EMPTY, utility(state))

        v = (EMPTY, 2)

        for action in actions(state):
            v = min(v,
                (action, max_value(result(state, action), alpha, beta)[1]),
                key=lambda x: x[1])
            
            beta = min(v[1], beta)
            if alpha >= beta:
                break

        return v

    the_player = player(board)
    alpha, beta = -2, 2

    if the_player == X:
        return max_value(board, alpha, beta)[0]
    elif the_player == O:
        return min_value(board, alpha, beta)[0]
