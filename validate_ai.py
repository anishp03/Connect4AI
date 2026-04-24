from connect4.ai import boardToFeatures, predictColumn
from connect4.logic.logic import COLUMNS, PLAYER1, PLAYER2, ROWS, empty_board


def main():
    testBoardToFeatures()
    testAiWinningMove()
    testAiBlockingMove()
    testFullColumnIsSkipped()
    testFullBoardReturnsNone()
    print("AI validation checks passed.")


def testBoardToFeatures():
    board = empty_board()
    features = boardToFeatures(board)
    assert len(features) == ROWS * COLUMNS


def testAiWinningMove():
    board = empty_board()
    board[5][0] = PLAYER2
    board[5][1] = PLAYER2
    board[5][2] = PLAYER2
    assert predictColumn(board) == 3


def testAiBlockingMove():
    board = empty_board()
    board[5][0] = PLAYER1
    board[5][1] = PLAYER1
    board[5][2] = PLAYER1
    assert predictColumn(board) == 3


def testFullColumnIsSkipped():
    board = empty_board()
    for row in range(ROWS):
        board[row][3] = PLAYER1 if row % 2 == 0 else PLAYER2

    assert predictColumn(board) != 3


def testFullBoardReturnsNone():
    board = [
        [PLAYER1 if (row + column) % 2 == 0 else PLAYER2 for column in range(COLUMNS)]
        for row in range(ROWS)
    ]
    assert predictColumn(board) is None


if __name__ == "__main__":
    main()
