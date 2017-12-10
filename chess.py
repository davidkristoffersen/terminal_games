#!/usr/bin/env python3
import os

TR = lambda x: '\x1b[38;2;255;0;0m' + str(x) + '\x1b[m' if not x else '\x1b[38;2;0;255;0m' + str(x) + '\x1b[m'
t_col = {False: '\x1b[1;38;2;0;0;0m', True: '\x1b[1;38;2;255;255;255m', None: '\x1b[2m'}

# All pieces attributes and mooving algorithms
pieces = {  # n: name, p:, print, t: team, vp: valid pos, vt: valid type ♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟
        'k': {'n': 'king', 'p': 'k', 't': None,
            'vp': lambda a, b,t: True if b[0] - a[0] in [-1, 0, 1] and b[1] - a[1] in [-1, 0, 1] else False, 
            'vt': lambda a, b: False},
        'q': {'n': 'queen', 'p': 'q', 't': None,
            'vp': lambda a, b, t: True if (b[0] - a[0] == b[1] - a[1] or not (b[0] - a[0]) + (b[1] - a[1])) or
            (not b[0] - a[0] and b[1] - a[1]) or (b[0] - a[0] and not b[1] - a[1]) else False, 
            'vt': lambda a, b: False},
        'r': {'n': 'rook', 'p': 'r', 't': None,
            'vp': lambda a, b, t: True if (not b[0] - a[0] and b[1] - a[1]) or (b[0] - a[0] and not b[1] - a[1]) else False, 
            'vt': lambda a, b: False},
        'c': {'n': 'knight', 'p': 'c', 't': None,
            'vp': lambda a, b, t: True if (b[0] - a[0] in [-2, 2] and b[1] - a[1] in [-1, 1]) or (b[0] - a[0] in [-1, 1] and b[1] - a[1] in [-2, 2]) else False, 
            'vt': lambda a, b: False},
        'b': {'n': 'bishop', 'p': 'b', 't': None,
            'vp': lambda a, b, t: True if b[0] - a[0] and b[1] - a[1] and (b[0] - a[0] == b[1] - a[1] or not (b[0] - a[0]) + (b[1] - a[1])) else False, 
            'vt': lambda a, b: False},
        'p': {'n': 'pawn', 'p': 'p', 't': None,
            'vp': lambda a, b, t: True if not b[1] - a[1] and 
            ((b[0] - a[0] == -1 or (b[0] - a[0] == -2 and a[0] == 6)) and t) or
            ((b[0] - a[0] == 1 or (b[0] - a[0] == 2 and a[0] == 1)) and not t)
            else False, 
            'vt': lambda a, b: False},
        'n': {'n': 'nonce', 'p': 'n',  't': None,
            'vp': lambda a, b, t: False, 
            'vt': lambda a, b: False}
        }

board_list =    [   # Lower is black, upper is white. n is empty
                'rcbqkbcr',
                'pppppppp',
                'nnnnnnnn',
                'nnnnnnnn',
                'nnnnnnnn',
                'nnnnnnnn',
                'PPPPPPPP',
                'RCBQKBCR'
                ]

# Constant of board size
size = 8

# Simple dictionary deep copy
memcpy = lambda x: {key: val for key, val in x.items()}

# For printing the board
pi = lambda i: print('\x1b[1;38;2;175;105;44m' + str([' ', 8, 7, 6, 5, 4, 3, 2, 1, ' '][i + 1]) + ' \x1b[m', end = ' ')
pj = lambda j: print('\x1b[1;38;2;175;105;44m' + ' abcdefgh '[j+1] + ' \x1b[m', end = ' ')
cij = lambda i, j:  pi(i) if j in [-1, 8] else pj(j)

prb = lambda x: [[print(t_col[board[i][j]['t']] + board[i][j]['p'] + ' \x1b[m', end = ' ') 
    if j in range(8) and i in range(8) else cij(i, j) for j in range(-1, size + 1)] for i in range(-1, size + 1) if not print()]

# For converting input to correct index
chtonum = lambda x: {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}[x]
invnum = lambda x: [8, 7, 6, 5, 4, 3, 2, 1, 0][x]
convmove = lambda x: [[invnum(int(x[1])), int(chtonum(x[0]))], [invnum(int(x[4])), int(chtonum(x[3]))]]


# Creatin of the board
def create_board():
    board = [[(memcpy(pieces[j]), False) if not j.istitle() else (memcpy(pieces[j.lower()]), True) for j in i] for i in board_list]
    for i, v in enumerate(board):
        for j, w in enumerate(v):
            if board[i][j][0]['n'] == 'nonce': board[i][j][0]['t'] = None
            elif w[1]: board[i][j][0]['t'] = True
            else: board[i][j][0]['t'] = False
            board[i][j] = board[i][j][0]
    return board

# Input checker
def action():
    os.system('clear')
    prb(board)
    print('\n\nAction: ', end = '')
    def inp_val(x): 
        try:
            return True if len(x) == 5 and x[0] in 'abcdefgh' and int(x[1]) in range(1, 9) and x[2] == ' ' and x[3] in 'abcdefgh' and int(x[4]) in range(1, 9) and not x[:2] == x[3:5] else False
        except: return False
    while True:
        ch = input()
        if inp_val(ch): return ch
        os.system('clear')
        prb(board)
        print('\n\x1b[38;2;255;0;0mInvalid input!\x1b[m', end='')
        print('\nAction: ', end = '')

def move_valid(ch):
    print(ch)
    p1, p2 = board[ch[0][0]][ch[0][1]], board[ch[1][0]][ch[1][1]]
    pos1, pos2 = [ch[0][0], ch[0][1]], [ch[1][0], ch[1][1]]
    if p1['n'] == 'nonce': 
        print('\n\x1b[38;2;255;0;0mNonce cannot be moved!\x1b[0;2m\t(press enter)\x1b[m', end = '')
        return False
    if not p1['vp'](pos1, pos2, p1['t']):
        print('\n\x1b[38;2;255;0;0mInvalid position!\x1b[0;2m\t(press enter)\x1b[m', end = '')
        return False

    return True

# Moving
def move(ch):
    board[ch[1][0]][ch[1][1]] = board[ch[0][0]][ch[0][1]]
    board[ch[0][0]][ch[0][1]] = memcpy(pieces['n'])
    prb(board)

# 16 pieces: one king, one queen, two rooks, two knights, two bishops, and eight pawns
if __name__ == '__main__':
    board = create_board()

    # Main loop
    while True:     
        while True:
            ch = action()
            ch = convmove(ch)
            if move_valid(ch): break
            input()
        move(ch)
        print('\n\n\x1b[0;2mPress enter\x1b[m', end = '')
        input()
