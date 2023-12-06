
import random
import sys
from copy import deepcopy
from math import inf

class Node:

    def __init__(self, player, s=None, prev=None, m=None):
        self.whose_turn = player # ten player wykonuje ruch zeby storzyc nowy stan
        self.t = 0
        self.n = 0
        self.parent = prev
        self.children = set()
        self.state = s
        self.move = m
        self.leaf = True

    def expand(self, p):
        new_leafs = set()
        for m in self.state.moves(self.whose_turn):
            new_state = deepcopy(self.state)
            new_state.do_move(m)
            new_node = Node(1 - self.whose_turn, new_state, p, m)
            new_leafs.add(new_node)
            self.children.add(new_node)
            # setattr(self, 'children', self.children.add(new_node))
        if len(new_leafs) != 0: self.leaf = False
        return new_leafs
 
class Jungle:
    MAXIMAL_PASSIVE = 30
    DENS_DIST = 0.1
    MX = 7
    MY = 9
    traps = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
    ponds = {(x, y) for x in [1, 2, 4, 5] for y in [3, 4, 5]}
    dens = [(3, 8), (3, 0)]
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    rat, cat, dog, wolf, jaguar, tiger, lion, elephant = range(8)

    def __init__(self):
        self.board = self.initial_board()
        self.pieces = {0: {}, 1: {}}

        for y in range(Jungle.MY):
            for x in range(Jungle.MX):
                C = self.board[y][x]
                if C:
                    pl, pc = C
                    self.pieces[pl][pc] = (x, y)
        self.curplayer = 0
        self.peace_counter = 0
        self.winner = None
        

    def initial_board(self):
        pieces = """
        L.....T
        .D...C.
        R.J.W.E
        .......
        .......
        .......
        e.w.j.r
        .c...d.
        t.....l
        """

        B = [x.strip() for x in pieces.split() if len(x) > 0]
        T = dict(zip('rcdwjtle', range(8)))

        res = []
        for y in range(9):
            raw = 7 * [None]
            for x in range(7):
                c = B[y][x]
                if c != '.':
                    if 'A' <= c <= 'Z':
                        player = 1
                    else:
                        player = 0
                    raw[x] = (player, T[c.lower()])
            res.append(raw)
        return res

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return None

    def can_beat(self, p1, p2, pos1, pos2):
        if pos1 in Jungle.ponds and pos2 in Jungle.ponds:
            return True  # rat vs rat
        if pos1 in Jungle.ponds:
            return False  # rat in pond cannot beat any piece on land
        if p1 == Jungle.rat and p2 == Jungle.elephant:
            return True
        if p1 == Jungle.elephant and p2 == Jungle.rat:
            return False
        if p1 >= p2:
            return True
        if pos2 in Jungle.traps:
            return True
        return False

    def pieces_comparison(self):
        for i in range(7, -1, -1):
            ps = []
            for p in [0,1]:
                if i in self.pieces[p]:
                    ps.append(p)
            if len(ps) == 1:
                return ps[0]
        return None
                
    def rat_is_blocking(self, player_unused, pos, dx, dy):        
        x, y = pos
        nx = x + dx
        for player in [0,1]:
            if Jungle.rat not in self.pieces[1-player]:
                continue
            rx, ry = self.pieces[1-player][Jungle.rat]
            if (rx, ry) not in self.ponds:
                continue
            if dy != 0:
                if x == rx:
                    return True
            if dx != 0:
                if y == ry and abs(x-rx) <= 2 and abs(nx-rx) <= 2:
                    return True
        return False

    def draw(self):
        TT = {0: 'rcdwjtle', 1: 'RCDWJTLE'}
        for y in range(Jungle.MY):
            L = []
            for x in range(Jungle.MX):
                b = self.board[y][x]
                if b:
                    pl, pc = b
                    L.append(TT[pl][pc])
                else:
                    L.append('.')
            print(''.join(L))
        print('')

    
    def victory(self, player):
        oponent = 1 - player        
        if len(self.pieces[oponent]) == 0: # opponent nie ma juz pionkow
            self.winner = player
            return True

        x, y = self.dens[oponent]
        if self.board[y][x]:
            self.winner = player
            return True
        return False

    def do_move(self, m):
        self.curplayer = 1 - self.curplayer
        if m is None:
            return
        pos1, pos2 = m
        x, y = pos1
        pl, pc = self.board[y][x]

        x2, y2 = pos2
        if self.board[y2][x2]:  # piece taken!
            pl2, pc2 = self.board[y2][x2]
            del self.pieces[pl2][pc2]
            self.peace_counter = 0
        else:
            self.peace_counter += 1    

        self.pieces[pl][pc] = (x2, y2)
        self.board[y2][x2] = (pl, pc)
        self.board[y][x] = None

    def moves(self, player):
        res = []
        for p, pos in self.pieces[player].items():
            x, y = pos
            for (dx, dy) in Jungle.dirs:
                pos2 = (nx, ny) = (x+dx, y+dy)
                if 0 <= nx < Jungle.MX and 0 <= ny < Jungle.MY:
                    if Jungle.dens[player] == pos2:
                        continue
                    if pos2 in self.ponds:
                        if p not in (Jungle.rat, Jungle.tiger, Jungle.lion):
                            continue
                        #if self.board[ny][nx] is not None:
                        #    continue  # WHY??
                        if p == Jungle.tiger or p == Jungle.lion:
                            if dx != 0:
                                dx *= 3
                            if dy != 0:
                                dy *= 4
                            if self.rat_is_blocking(player, pos, dx, dy):
                                continue
                            pos2 = (nx, ny) = (x+dx, y+dy)
                    if self.board[ny][nx] is not None:
                        pl2, piece2 = self.board[ny][nx]
                        if pl2 == player:
                            continue
                        if not self.can_beat(p, piece2, pos, pos2):
                            continue
                    res.append((pos, pos2))
        return res

    # ======================================================
    # alpha beta

    def manhattan_distance_and_animal_weight(self, me):
        my_summary_dist = 0
        my_summary_weight = 0
        oponent_summary_dist = 0
        opponent_summary_weight = 0
        
        my_dest_den = self.dens[1 - me]
        for piece in self.pieces[me]:
            my_summary_weight += piece
            pos = self.pieces[me][piece]
            my_summary_dist += abs(pos[0] - my_dest_den[0]) + abs(pos[1] - my_dest_den[1])

        opponent_dest_den = self.dens[me]
        for piece in self.pieces[1 - me]:
            opponent_summary_weight += piece
            pos = self.pieces[1 - me][piece]
            oponent_summary_dist += abs(pos[0] - opponent_dest_den[0]) + abs(pos[1] - opponent_dest_den[1])
                
        return 100 * (oponent_summary_dist / (oponent_summary_dist + my_summary_dist)), 100 * (my_summary_weight / (my_summary_weight + opponent_summary_weight))
    
    def rat_in_water(self, me):
        return 1 if 0 in pieces[me] and (pieces[me][0] in ponds) else 0

    def heuristic(self, me):
        summary_dist, summary_weight = self.manhattan_distance_and_animal_weight(me)
        rat_value = self.rat_in_water()
        return 100 * summary_dist + 100 * summary_weight + 1000 * rat_value

    def find_best(self, player, moves):

        def children(state, maximizingPlayer):
            moves = state.moves(maximizingPlayer)
            for move in moves:
                new_state = deepcopy(state)
                new_state.do_move(move)
                yield new_state

        def alphabeta(state, depth, alpha, beta, maximizingPlayer):
            if depth == 0 or state.check_finish() == player:
                return 100000
        
            if maximizingPlayer:
                maxEval = -inf
                for child in children(state, maximizingPlayer):
                    eval = alphabeta(deepcopy(child), depth - 1, alpha, beta, 0)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                            break
                return maxEval
            else:
                minEval = +inf
                for child in children(state, maximizingPlayer):
                    eval = alphabeta(deepcopy(child), depth - 1, alpha, beta, 1)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                            break
                return minEval

        best_move = None
        best_score = -inf
        for m in moves:
            temp = deepcopy(self)
            temp.do_move(m)
            score = alphabeta(temp, 1, -inf, +inf, 1 - player)
            if score > best_score:
                best_score = score
                best_move = m
        return best_move

    # MCTS

    def USB1(leaf, iteration):
        C = 2
        if leaf.n == 0: return inf
        return (leaf.t / leaf.n) + C * pow(ln(iteration) / leaf.n, 1/2)

    def find_best_MCTS(self, player, moves, iterations):
        root = Node(player)
        root.state = deepcopy(self)
        leafs = set()
        leafs.add(root)

        for i in range(1, iterations + 1):
            print(len(root.children))
            flag = False
            node_to_simulate = max(leafs, key=lambda x: Jungle.USB1(x, i))
            if node_to_simulate.n != 0:
                temp = node_to_simulate.expand(node_to_simulate)
                if len(temp) != 0:
                    leafs.remove(node_to_simulate)
                    for j in temp: leafs.add(j)
                    node_to_simulate = max(leafs, key=lambda x: Jungle.USB1(x, i))
                    flag = True

            if flag:
                won, moves_counter = finish_game(node_to_simulate.state, node_to_simulate.whose_turn)
                if won ==  player: score = 2
                elif won == 2: score = 1
                else: score = 0
                node_to_simulate.t += score
                node_to_simulate.n += 1
            else:
                score = 2

            # propagation
            while node_to_simulate.parent != None:
                node_to_simulate = node_to_simulate.parent
                node_to_simulate.n += 1
                node_to_simulate.t += score
        print(len(root.children))
        best = max(root.children, key=lambda x: x.t / x.n if x.n != 0 else 0)
        return best.move

    # ======================================================

    def check_finish(self):
        """
        -1 : kontynuuj
        0 : wygrywa 0
        1 : wygrywa 1
        2 : remis
        """
        if self.victory(1):
            if self.victory(0):
                return 2  # Remis
            else:
                return 1  # Wygrana

        elif self.victory(0):
            return 0
        return -1

    def choose_move_random(self,moves,player):
        return random.choice(moves)
    
    def choose_move_simulation(self, moves, player, N=20000):
        pieces_copy = deepcopy(self.pieces)
        board_copy = deepcopy(self.board)  
        curr_player_copy = self.curplayer
        peace_counter_copy = self.peace_counter
        
        set_cnt = {move: 0 for move in moves}
        total_moves = 0 
        for move in moves: 
            self.pieces = deepcopy(pieces_copy)
            self.board = deepcopy(board_copy)
            self.curplayer = curr_player_copy
            self.peace_counter = peace_counter_copy
            self.do_move(move)
            (won, moves_cnt) = finish_game(self,player)
            total_moves += moves_cnt
            if won == player:
                set_cnt[move] += 1
            elif won == 2: #remis
                set_cnt[move] += 0.5

        max_value = max(set_cnt.values())
        max_value_keys = [key for key, value in set_cnt.items() if value == max_value]
        self.pieces=pieces_copy
        self.board=board_copy
        self.curplayer=curr_player_copy
        self.peace_counter=peace_counter_copy
        return random.choice(max_value_keys)



def finish_game(game, player):            
    player_turn = player
    temp = game.check_finish()
    if temp != -1:
        return (temp, 0)
    moves_cnt = 0
    while game.check_finish() == -1:       
        moves = game.moves(player_turn)
        if moves:
            move = random.choice(moves)
            game.do_move(move)
            moves_cnt += 1
        else:
            if game.moves(1 - player_turn) != []:
                return (1 - player_turn,moves_cnt)
            else:
                return (2, moves_cnt)
        player_turn = 1 - player_turn
    return (game.check_finish(),moves_cnt)


def own_simulator(game, player):          
    player_turn = player
    temp = game.check_finish()
    if temp!=-1:
        return (temp,0)
    moves_cnt = 0
    while game.check_finish() == -1: 
        moves = game.moves(player_turn)
        if moves:
            if player_turn == 0:
                 # move = random.choice(moves)
                 move = game.find_best(player_turn, moves)
            else:
                # move = game.choose_move_simulation(moves, 1, 50)
                move = game.find_best_MCTS(player_turn, moves, 200)
            game.do_move(move)
            moves_cnt += 1
        else:
            if game.moves(1 - player_turn) != []: #or game.victory(1-player_turn)
                return (1 - player_turn,moves_cnt)
            else:
                return (2, moves_cnt) #remis
        player_turn = 1 - player_turn

    res = game.check_finish()
    return (res, moves_cnt)  


scores = [0, 0, 0]
for i in range (30):
    game = Jungle()
    my_player = random.choice([0,1])
    (won, moves) = own_simulator(game, my_player)
    if won == 2:
        print('draw')
    else:
        print(f"Player {won} won in {str(moves)} moves")
    scores[won] += 1

print(f"\nPlayer 0 won {scores[0]} games\nPlayer 1 won {scores[1]} games\ndraws {scores[2]}")
