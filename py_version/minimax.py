#!/usr/bin/env python3
from math import inf as infinity
import platform
import time
from os import system

"""
An implementation of Minimax AI Algorithm in Tic Tac Toe,
using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)
"""

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
last_move = [-1, -1, -1]

calculate_time = 0
search_count = 0

options = {
    1: ' Minimax',
    2: ' Alpha-Beta search'
}
level = 0

def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    n = len(state)
    full = [player] * n
    if full in state:
        return True
    if full in [list(col) for col in zip(*state)]:
        return True
    if [state[i][i] for i in range(n)] == full:
        return True
    if [state[i][n - 1 - i] for i in range(n)] == full:
        return True
    return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    # cells = []
    #
    # for x, row in enumerate(state):
    #     for y, cell in enumerate(row):
    #         if cell == 0:
    #             cells.append([x, y])
    cells = [[x, y] for x, row in enumerate(state)
             for y, cell in enumerate(row) if cell == 0]
    return cells


def neighbor_cells(state):
    cells = [[x, y] for x, row in enumerate(state)
             for y, cell in enumerate(row) if
             cell == 0 and x != 0 and y != 0 and
             x != len(state) - 1 and y != len(state) - 1
             and (row[y-1] or row[y+1] or state[x-1][y] or state[x+1][y])]
    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    global search_count
    search_count += 1
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def alpha_beta_search(state, player):
    if player is COMP:
        move = max_value(state, -infinity, +infinity, player)
    else:
        move = min_value(state, -infinity, +infinity, player)
    return move


def min_value(state, alpha, beta, player, depth=1):
    global search_count
    search_count += 1
    empties = empty_cells(state)
    if len(empties) == 0 or game_over(state):
        val = evaluate(state)
        return val, -1, -1
    # shuffle(empties)
    score, ax, ay = +infinity, -1, -1
    for cell in empties:
        x, y = cell[0], cell[1]
        state[x][y] = player
        m, _, _ = max_value(state, alpha, beta, -player, depth + 1)
        if m < score:
            score = m
            ax, ay = x, y
        state[x][y] = 0
        if score <= alpha:
            return score, ax, ay
        beta = min(beta, score)

    return score, ax, ay


def max_value(state, alpha, beta, player, depth=1):
    """
    @return [score, x, y]
    """
    global search_count
    search_count += 1
    empties = empty_cells(state)
    if len(empties) == 0 or game_over(state):
        val = evaluate(state)
        return val, -1, -1
    # shuffle(empties)
    score, ax, ay = -infinity, -1, -1
    for cell in empties:
        x, y = cell[0], cell[1]
        state[x][y] = player
        m, _, _ = min_value(state, alpha, beta, -player, depth + 1)
        if m > score:
            score = m
            ax, ay = x, y
        state[x][y] = 0
        if score >= beta:
            return score, ax, ay
        alpha = max(alpha, score)
    return score, ax, ay


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    print(options[level])
    str_line = '----' * (len(state) + 1)
    print('   ', end='')
    for i in range(len(state)):
        print(f'{i+1:-3} ', end='')
    print('\n' + str_line + '-')
    for i, row in enumerate(state):
        print(f'{i+1:-3} ', end='')
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} ', end='')
        print('|')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    global last_move
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)
    print('Calculating...')

    if level == 1:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]
    else:
        move = alpha_beta_search(board, COMP)
        x, y = move[1], move[2]
    last_move = move

    set_move(x, y, COMP)


def human_turn(c_choice, h_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)
    print(f"search count: {search_count}")

    while True:
        try:
            move = input('x y: ')
            coord = [int(c) for c in move.split()]
            can_move = set_move(coord[0]-1, coord[1]-1, HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
            else:
                break
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (IndexError, KeyError, ValueError):
            print('Bad choice')


def main():
    """
    Main function that calls all functions
    """
    global board, calculate_time, search_count, level
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first
    n = 3
    while True:
        nstr = input('Choose board size between 3 and 10 [default 3]: ')
        if nstr:
            try:
                n = int(nstr)
            except ValueError:
                print('Invalid number')
                continue
        if n > 2 and n <= 10:
            n = int(n)
            board = [
                    [0 for _ in range(n)] for __ in range(n)
            ]
            break
    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose [X] or O\nChosen: ').upper()
            if not h_choice:
                h_choice = 'X'
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human chooses X or O to play
    print(
        'Choose computer level:',
    )
    for k, v in options.items():
        print(f"{k}. {v}")
    while True:
        try:
            print('')
            level = int(input('Chosen: ').upper())
            if level not in options:
                raise ValueError()
            break
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y]/n: ').upper()
            if not first:
                first = 'Y'
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    start = None
    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            search_count = 0
            ai_turn(c_choice, h_choice)
            first = ''
        time.sleep(1. - calculate_time)
        human_turn(c_choice, h_choice)
        start = time.time()
        search_count = 0
        ai_turn(c_choice, h_choice)
        end = time.time()
        calculate_time = end-start

    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
