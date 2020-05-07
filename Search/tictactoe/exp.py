import tictactoe as ttt
from sys import maxsize as MAXSIZE

X = 'X'
O = 'O'
EMPTY = None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    def straight_lines():
        ## checks if any player has completed the horizontal or verticle line
        ## takes len(board) iterations

        for row in range(0, len(board)**2, len(board)):
            first_in_row, row = divmod(row, len(board)), row + 1
            second_in_row, row = divmod(row, len(board)), row + 1
            third_in_row, row = divmod(row, len(board)), row + 1

            ## Reversing the position finds the transposed element
            first_in_col = first_in_row[::-1]
            second_in_col = second_in_row[::-1]
            third_in_col = third_in_row[::-1]

            if board[first_in_row[0]][first_in_row[1]] == board[second_in_row[0]][second_in_row[1]]\
            and board[second_in_row[0]][second_in_row[1]] == board[third_in_row[0]][third_in_row[1]]:
                winner = board[first_in_row[0]][first_in_row[1]]
                if winner:
                    return winner

            if board[first_in_col[0]][first_in_col[1]] == board[second_in_col[0]][second_in_col[1]]\
            and board[second_in_col[0]][second_in_col[1]] == board[third_in_col[0]][third_in_col[1]]:
                winner = board[first_in_col[0]][first_in_col[1]]
                if winner:
                    return winner

    def diagonals():
        ## checks if any diagonals are completed

        ## left to right diagonal
        lrdiags = [i for i in range(0, len(board)**2, len(board)+1)]
        ## right to left diagonal
        rldiags = [i for i in range(len(board)-1, len(board)**2-1, len(board)-1)]

        s = set()
        for i in lrdiags:
            i = divmod(i, len(board))
            s.add(board[i[0]][i[1]])

        if len(s) <= 1:
            i = divmod(lrdiags[0], len(board))
            return board[i[0]][i[1]]

        s = set()
        for i in rldiags:
            i = divmod(i , len(board))
            s.add(board[i[0]][i[1]])

        if len(s) <= 1:
            i = divmod(rldiags[0], len(board))
            return board[i[0]][i[1]]

    winning_combos = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
    ]
    for line in winning_combos:
        a, b, c = line
        a, b, c = divmod(a, 3), divmod(b, 3), divmod(c, 3)

        if board[a[0]][a[1]] and board[a[0]][a[1]] == board[b[0]][b[1]] and\
        board[b[0]][b[1]] == board[c[0]][c[1]]:
            return board[a[0]][a[1]]

    # return straight_lines() or diagonals() or None

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(state, depth=0):

        if ttt.terminal(state):
            return (None, ttt.utility(state))

        v = (None, -2)

        for action in ttt.actions(state):
            v = max(v, (action, min_value(ttt.result(state, action), depth+1)[1] - (depth/10)), key=lambda x: x[1])
        return v

    def min_value(state, depth=0):

        if ttt.terminal(state):
            return (None, ttt.utility(state))

        v = (None, 2)

        for action in ttt.actions(state):
            v = min(v, (action, max_value(ttt.result(state, action), depth+1)[1] + (depth/10)), key=lambda x: x[1])
        return v


    if ttt.player(board) == X:
        return max_value(board)[0]
    elif ttt.player(board) == O:
        return min_value(board)[0]

if __name__ == '__main__':
    board = ttt.initial_state()
    # for i in board:
    #     i[1] = 'X'
    # for i in range(len(board)):
    #     board[i][i] = 'O'
    board[0][0] = 'X'
    board[0][1] = 'O'
    board[0][2] = 'X'
    board[2][2] = 'O'
    board[1][1] = 'X'
    board[1][0] = 'O'
    board[2][0] = 'X'

    # print(board)
    # print(tictactoe.player(board))
    # print(tictactoe.actions(board))
    # print(tictactoe.result(board, (0,1)))
    # print(check(board))
    # print(tictactoe.winner(board))
    print(winner(board))
