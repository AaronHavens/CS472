"""Games, or Adversarial Search (Chapter 5)"""

from collections import namedtuple
import random

infinity = float('inf')
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

# ______________________________________________________________________________
# Minimax Search



def alphabeta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

# ______________________________________________________________________________
# Players for Games


def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move_string = input('Your move? ')
    try:
        move = eval(move_string)
    except NameError:
        move = move_string
    return move


def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state))


def alphabeta_player(game, state):
    return alphabeta_search(state, game)


# ______________________________________________________________________________
# Some Sample Games

#
def actions(board, player):
        """Return a list of the allowable moves at this point."""
        validMoves = []
        board = copy_board(board)
        for x in range(8):
            for y in range(8):
                if isValidMove(board,player,x,y):
                    validMoves.append([x,y])
        return validMoves

def isOnBoard(x,y):
    return (x <= 7 and x >= 0 and y <= 7 and y >= 0)

def opponent(player):
    if(player == 'W'):
        return 'B'
    else:
        return 'W'

def copy_board(board):
    board_copy = []
    for x in range(8):
        board_copy.append([' ']*8)
    for x in range(8):
        for y in range(8):
            board_copy[x][y] = board[x][y]
    return board_copy
def new_board():
    new_board = []
    for x in range(8):
        new_board.append([' ']*8)
    return new_board
def make_move(board,player,m):
    to_flip = isValidMove(board,player,m[0],m[1])
    if to_flip:
        board[m[0]][m[1]] = player
        for x,y in to_flip:
            board[x][y] = player
    return board

def score(player, board):
    player_score, opponent_score = 0, 0
    opponent = opponent(player)
    for x in range(8):
        for y in range(8):
            if(board[x][y] != ' '):
                if board[x][y] == player:
                    player_score += 1
                elif board[x][y] == opponent:
                    opponent_score += 1

    return player_score - opponent_score

def alpha_beta(board,player,beta,depth,eval):
    if depth == 0:
        return evaluate(board,player), None
    def value(board,alpha,beta):
        return - alpha_beta(opponent(player),board,-beta,-alpha,depth-1,eval)[0]
    moves = actions(board,player)
    if not moves:
        if not actions(board ,opponent(player)):
            return final_val(board,player), None
        return value(board), None
    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            break
        val = value(make_move(board, opponent(player),move), alpha,beta)
        if val > alpha:
            alpha = val
            best_move = move
    return alpha, best_move
def start_config(board):
    board[3][3], board[4][3] = 'B','W'
    board[3][4], board[4][4] = 'W','B'
#check if move is valid and which tiles would be flipped as a result
def isValidMove(board,player,x_s,y_s):
    if board[x_s][y_s] != ' ' or not isOnBoard(x_s,y_s):
        return False
    board[x_s][y_s] = player
    other_player = opponent(player)
    flip_tiles = []
    for xd,yd in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x,y = x_s,y_s
        x += xd
        y += yd
        if isOnBoard(x,y) and board[x][y] == other_player:
            x += xd
            y += yd
            if not isOnBoard(x,y):
                continue
            while board[x][y] == other_player:
                x += xd
                y += yd
                if not isOnBoard(x,y):
                    break
            if not isOnBoard(x,y):
                continue
            if board[x][y] == player:
                while True:
                    x -= xd
                    y -= yd
                    if x == x_s and y == y_s:
                        break
                    flip_tiles.append([x,y])
    board[x_s][y_s] = ' '
    if len(flip_tiles) == 0:
        return False
    return flip_tiles

def disp_board(board):
    print('-----------------')
    for i in range(8):
        line_str = '|'
        for j in range(8):
            line_str += board[j][i] +'|'
        print(line_str )
        print('-----------------')

def final_val(board, player):
    diff = score(board,player)
    if diff < 0:
        return MIN_VAL
    elif diff > 0:
        return MAX_VAl
    return diff
#
class Game():
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))
board = new_board()
start_config(board)
#disp_board(board)
print(actions(board,'B'))
board = make_move(board,'B',[2,4])
board = make_move(board,'W',[4,5])
board = make_move(board,'W',[1,4])
#board = make_move(board,'B',[3,5])
disp_board(board)