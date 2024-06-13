from enum import Enum
from typing import Dict, List, Tuple, Optional

import cv2
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'


class XoxState(Enum):
    """
    Enum that represents the state of the tic-tac-toe game.
    """
    RUNNING = 0
    X_WINS = 1
    O_WINS = 2
    DRAW = 3


class TicTackToeBoard:
    def __init__(self):
        """
        Initializes the empty tic-tac-toe board.
        """
        self.__board = [[' ' for _ in range(3)] for _ in range(3)]
        self.__next_move = 'X'

    @property
    def next_move(self) -> str:
        return self.__next_move

    def __getitem__(self, key: int) -> List[str]:
        """
        Returns the row of the board.
        """
        return list(self.__board[key])

    def copy(self) -> 'TicTackToeBoard':
        """
        Returns a copy of the current board.
        """
        copy = TicTackToeBoard()
        copy.__board = [row.copy() for row in self.__board]
        copy.__next_move = self.__next_move
        return copy

    def get_possible_moves(self) -> List[Point]:
        """
        Returns the list of possible moves at the current state of the game.
        """
        return [Point(i, j) for i in range(3) for j in range(3) if self.__board[i][j] == ' ']

    def is_move_valid(self, point: Point) -> bool:
        """
        Returns True if the move is valid, False otherwise.
        """
        return self.__board[point.x][point.y] == ' '

    def make_move(self, point: Point):
        """
        Makes the move on the board.
        """
        assert self.is_move_valid(point), 'Invalid move'
        self.__board[point.x][point.y] = self.__next_move
        self.__next_move = 'O' if self.__next_move == 'X' else 'X'

    def get_state(self) -> Tuple[XoxState, Optional[Tuple[Point, Point]]]:
        """
        Returns the current state of the game.
        If the game is finished, returns the points that should be highlighted.
        """
        for i in range(3):
            if self.__board[i][0] == self.__board[i][1] == self.__board[i][2] != ' ':
                return XoxState.X_WINS if self.__board[i][0] == 'X' else XoxState.O_WINS, (Point(i, 0), Point(i, 2))
            if self.__board[0][i] == self.__board[1][i] == self.__board[2][i] != ' ':
                return XoxState.X_WINS if self.__board[0][i] == 'X' else XoxState.O_WINS, (Point(0, i), Point(2, i))
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2] != ' ':
            return XoxState.X_WINS if self.__board[0][0] == 'X' else XoxState.O_WINS, (Point(0, 0), Point(2, 2))
        if self.__board[0][2] == self.__board[1][1] == self.__board[2][0] != ' ':
            return XoxState.X_WINS if self.__board[0][2] == 'X' else XoxState.O_WINS, (Point(0, 2), Point(2, 0))
        if all(cell != ' ' for row in self.__board for cell in row):
            return XoxState.DRAW, None
        return XoxState.RUNNING, None

    def __hash__(self) -> int:
        return hash(str(self.__board))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TicTackToeBoard) and \
            all(self.__board[i][j] == other.__board[i][j] for i in range(3) for j in range(3))

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


def draw_board(board: TicTackToeBoard, moves: List[Tuple[Point, int]]) -> np.ndarray:
    """
    Draws the current board and the scores of all possible moves.

    Params:
    -------
        board: The current tic-tac-toe board.
        moves: List of tuples containing the move and its score.

    Returns:
    --------
        Image of the board.
    """
    image = np.ones((300, 300, 3), dtype=np.uint8) * 255

    # Color the cells based on the score
    for move, score in moves:
        if score == -1:
            color = (0, 0, 255)
        elif score == 1:
            color = (0, 255, 0)
        else:
            color = (255, 255, 0)
        cv2.rectangle(image, (100 * move.y, 100 * move.x), (100 * (move.y + 1), 100 * (move.x + 1)), color, -1)

    # Draw lines
    for i in range(0, 3):
        cv2.line(image, (100 * i, 0), (100 * i, 300), (0, 0, 0), 3)
        cv2.line(image, (0, 100 * i), (300, 100 * i), (0, 0, 0), 3)
    cv2.line(image, (300, 0), (300, 300), (0, 0, 0), 3)
    cv2.line(image, (0, 300), (300, 300), (0, 0, 0), 3)

    # Draw Xs and Os
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                cv2.line(image, (100 * j + 20, 100 * i + 20), (100 * (j + 1) - 20, 100 * (i + 1) - 20), (0, 0, 0), 5)
                cv2.line(image, (100 * j + 20, 100 * (i + 1) - 20), (100 * (j + 1) - 20, 100 * i + 20), (0, 0, 0), 5)
            elif board[i][j] == 'O':
                cv2.circle(image, (100 * j + 50, 100 * i + 50), 30, (0, 0, 0), 5)

    # Draw finish line
    state, winning_points = board.get_state()
    if state in [XoxState.X_WINS, XoxState.O_WINS]:
        cv2.line(image, (100 * winning_points[0].y + 50, 100 * winning_points[0].x + 50),
                 (100 * winning_points[1].y + 50, 100 * winning_points[1].x + 50), (0, 0, 255), 10)

    return image


def minimax_recursive(board: TicTackToeBoard, maximize_player: str, cache: Dict[TicTackToeBoard, int]) -> int:
    """
    Recursive function that calculates the minimax score for the given board.
    """
    if board in cache:
        return cache[board]

    # If the game is done, report how it went for the maximizing player
    state, _ = board.get_state()
    if state == XoxState.X_WINS:
        return 1 if maximize_player == 'X' else -1
    if state == XoxState.O_WINS:
        return 1 if maximize_player == 'O' else -1
    if state == XoxState.DRAW:
        return 0

    if board.next_move == maximize_player:
        # If the maximizing player is on the move,
        # assume the the move will be taken that maximizes the score
        best_score = -2
        for move in board.get_possible_moves():
            board_copy = board.copy()
            board_copy.make_move(move)
            score = minimax_recursive(board_copy, maximize_player, cache)
            best_score = max(best_score, score)
    else:
        # If the minimizing player is on the move,
        # assume the the move will be taken that minimizes the score
        best_score = 2
        for move in board.get_possible_moves():
            board_copy = board.copy()
            board_copy.make_move(move)
            score = minimax_recursive(board_copy, maximize_player, cache)
            best_score = min(best_score, score)

    cache[board] = best_score
    return best_score


def minimax(board: TicTackToeBoard) -> List[Tuple[Point, int]]:
    """
    Takes the current tic-tac-toe board and returns the scores of all possible moves.

    Params:
    -------
        board: The current tic-tac-toe board.

    Returns:
    --------
        List of tuples containing the move and its score.
    """
    state, _ = board.get_state()
    if state != XoxState.RUNNING:
        return []

    moves = []
    cache = {}
    for move in board.get_possible_moves():
        # Find score for each possible move of the starting board
        board_copy = board.copy()
        board_copy.make_move(move)
        score = minimax_recursive(board_copy, board.next_move, cache)
        moves.append((move, score))

    return moves


if __name__ == '__main__':
    # Play tic-tac-toe using the keyboard (q, w, e, a, s, d, z, x, c) with cheats
    # Press 'r' to restart the game and 'Esc' to exit
    while True:
        board = TicTackToeBoard()
        state, _ = board.get_state()
        while state == XoxState.RUNNING:
            cv2.imshow('Tic-Tac-Toe', draw_board(board, minimax(board)))
            key = cv2.waitKey(0)
            if key == 27:
                cv2.destroyAllWindows()
                exit(0)
            if key == ord('r'):
                board = TicTackToeBoard()
            elif key in [ord('q'), ord('w'), ord('e'), ord('a'), ord('s'), ord('d'), ord('z'), ord('x'), ord('c')]:
                x = 0 if key in [ord('q'), ord('w'), ord('e')] else 1 if key in [ord('a'), ord('s'), ord('d')] else 2
                y = 0 if key in [ord('q'), ord('a'), ord('z')] else 1 if key in [ord('w'), ord('s'), ord('x')] else 2
                if board.is_move_valid(Point(x, y)):
                    board.make_move(Point(x, y))
        cv2.imshow('Tic-Tac-Toe', draw_board(board, []))
        cv2.waitKey(0)
