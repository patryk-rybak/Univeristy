#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Losowy agent do Reversi z MCTS.
'''

import random
import sys
import math


class Node:
    def __init__(self, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0


class Reversi:
    M = 8
    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = self.initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(self.M):
            for j in range(self.M):
                if self.board[i][j] is None:
                    self.fields.add((j, i))

    def initial_board(self):
        B = [[None] * self.M for _ in range(self.M)]
        B[3][3] = 1
        B[4][4] = 1
        B[3][4] = 0
        B[4][3] = 0
        return B

    def draw(self):
        for i in range(self.M):
            res = []
            for j in range(self.M):
                b = self.board[i][j]
                if b is None:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print(''.join(res))
        print('')

    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction, player)
                   for direction in self.DIRS):
                res.append((x, y))
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < self.M and 0 <= y < self.M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        assert player == len(self.move_list) % 2
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move is None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx, dy in self.DIRS:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for (nx, ny) in to_beat:
                    self.board[ny][nx] = player

    def result(self):
        res = 0
        for y in range(self.M):
            for x in range(self.M):
                b = self.board[y][x]
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] is None and self.move_list[-2] is None


class MCTSAgent:
    def __init__(self, exploration_constant=1.4, num_simulations=1000):
        self.exploration_constant = exploration_constant
        self.num_simulations = num_simulations
        self.reset()

    def reset(self):
        self.game = Reversi()
        self.my_player = 1
        self.tree = {}

    def uct_score(self, node):
        if node.visits == 0:
            return float('inf')
        exploitation = node.wins / node.visits
        exploration = math.sqrt(math.log(node.parent.visits) / node.visits)
        return exploitation + self.exploration_constant * exploration

    def select_best_child(self, node):
        best_child = None
        best_score = float('-inf')
        for child in node.children:
            score = self.uct_score(child)
            if score > best_score:
                best_child = child
                best_score = score
        return best_child

    def expand_node(self, node):
        moves = self.game.moves(node.move)
        for move in moves:
            new_node = Node(move, parent=node)
            node.children.append(new_node)

    def simulate(self, node):
        game_copy = Reversi()
        game_copy.board = [x[:] for x in self.game.board]
        game_copy.fields = set(self.game.fields)
        game_copy.move_list = list(self.game.move_list)
        game_copy.history = [x[:] for x in self.game.history]
        game_copy.do_move(node.move, node.move % 2)
        current_player = 1 - node.move % 2

        while not game_copy.terminal():
            moves = game_copy.moves(current_player)
            if moves:
                move = random.choice(moves)
                game_copy.do_move(move, current_player)
                current_player = 1 - current_player
            else:
                game_copy.do_move(None, current_player)
                current_player = 1 - current_player

        result = game_copy.result()
        return result

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            if node.move % 2 == result % 2:
                node.wins += 1
            node = node.parent

    def get_best_move(self):
        best_child = self.select_best_child(self.tree)
        return best_child.move

    def make_move(self, move):
        self.game.do_move(move, self.my_player)

    def loop(self):
        CORNERS = {(0, 0), (0, 7), (7, 0), (7, 7)}
        while True:
            cmd, args = self.hear()
            if cmd == 'HEDID':
                unused_move_timeout, unused_game_timeout = args[:2]
                move = tuple((int(m) for m in args[2:]))
                if move == (-1, -1):
                    move = None
                self.game.do_move(move, 1 - self.my_player)
            elif cmd == 'ONEMORE':
                self.reset()
                continue
            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                assert not self.game.move_list
                self.my_player = 0

            root = Node()
            self.tree = {root: self.game}
            for _ in range(self.num_simulations):
                selected_node = self.select_best_child(root)
                if selected_node not in self.tree:
                    self.tree[selected_node] = self.game
                    self.expand_node(selected_node)
                    result = self.simulate(selected_node)
                else:
                    self.game = self.tree[selected_node]
                    result = self.simulate(selected_node)
                self.backpropagate(selected_node, result)

            best_move = self.get_best_move()
            self.make_move(best_move)

            self.say('IDO %d %d' % best_move)


class Player(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = Reversi()
        self.my_player = 1
        self.say('RDY')

    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]

    def loop(self):
        agent = MCTSAgent()
        CORNERS = {(0, 0), (0, 7), (7, 0), (7, 7)}
        while True:
            cmd, args = self.hear()
            if cmd == 'HEDID':
                unused_move_timeout, unused_game_timeout = args[:2]
                move = tuple((int(m) for m in args[2:]))
                if move == (-1, -1):
                    move = None
                self.game.do_move(move, 1 - self.my_player)
            elif cmd == 'ONEMORE':
                self.reset()
                continue
            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                assert not self.game.move_list
                self.my_player = 0

            moves = self.game.moves(self.my_player)

            if moves:
                move = agent.make_move()
                agent.make_move(move)
            else:
                agent.make_move(None)
                move = (-1, -1)
            self.say('IDO %d %d' % move)


if __name__ == '__main__':
    player = Player()
    player.loop()