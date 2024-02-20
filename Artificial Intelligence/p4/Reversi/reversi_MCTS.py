#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# test2.py
# Generalnie plansza albo caly state moze byc od razu tylko w Node
# moze zmienic warunek kiedy plansza jest wygrana

import random
import sys
from math import inf
import numpy as np
from numpy import log as ln
from copy import deepcopy



class Node:

	def __init__(self, player, s=None, prev=None, m=None):
		self.whose_turn = player # ten player wykonuje ruch zeby storzyc nowy stan
		self.t = 0
		self.n = 0
		self.parent = prev
		self.children = set()
		self.state = s
		self.move = m

	def is_leaf(self):
		return len(self.children) == 0

	def expand(self, p):
		new_leafs = set()
		for m in self.state.moves(self.whose_turn):
			new_state = deepcopy(self.state)
			new_state.do_move(m, self.whose_turn)
			new_node = Node(1 - self.whose_turn, new_state, p, m)
			self.children.add(new_node)
			new_leafs.add(new_node)
		return new_leafs



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
		# assert player == len(self.move_list) % 2
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


class Player(object):
	def __init__(self):
		self.reset()

	def reset(self):
		self.game = Reversi()
		self.my_player = 1
		self.say('RDY')
		self.tree = Node(self.my_player, s=self.game)
		self.tree.children.add(self.tree)
		self.leafs = set()
		self.leafs.add(self.tree)

	def say(self, what):
		sys.stdout.write(what)
		sys.stdout.write('\n')
		sys.stdout.flush()

	def hear(self):
		line = sys.stdin.readline().split()
		return line[0], line[1:]

	def USB1(leaf, iteration):
		C = 2
		if leaf.n == 0: return inf
		return (leaf.t / leaf.n) + C * pow(ln(iteration) / leaf.n, 1/2)

	def find_best(self, iterations):

		def simulate(state, whose_turn):
			state = deepcopy(state)
			while not state.terminal():
				moves = state.moves(whose_turn)
				if len(moves) != 0: move = random.choice(moves)
				else: move = None
				state.do_move(move, whose_turn)
				whose_turn = 1 - whose_turn

			points = 0
			for y in range(self.game.M):
				for x in range(self.game.M):
					if state.board[y][x] == self.my_player: points += 1
			if points > 32: return 4
			elif points == 32: return 2
			return 0
		
		for i in range(1, iterations + 1):
			# print('for', i)
			# for pp in self.leafs: print(pp.n)
			node_to_simulate = max(self.leafs, key=lambda x: Player.USB1(x, i))
			if node_to_simulate.n != 0:
				self.leafs.remove(node_to_simulate)
				temp = node_to_simulate.expand(node_to_simulate)
				for j in temp: self.leafs.add(j)
				node_to_simulate = max(self.leafs, key=lambda x: Player.USB1(x, i))
			score = simulate(node_to_simulate.state, node_to_simulate.whose_turn)
			node_to_simulate.t += score
			node_to_simulate.n += 1

		# propagation
		while node_to_simulate.parent != None:
			node_to_simulate = node_to_simulate.parent
			node_to_simulate.n += 1
			node_to_simulate.t += score

		best = max(self.tree.children, key=lambda x: x.t / x.n if x.n != 0 else 0)
		print('best.t', best.t)

		# correcting leafs
		def find_leafs(node):
			# node.state.draw()
			if len(node.children) == 0:
				res = set()
				res.add(node)
				return res
			else:
				res = set()
				for ch in node.children:
					res = res | find_leafs(ch)
				return res
		ok = find_leafs(best)
		# print('ok', ok)
		# print('leafs', self.leafs)
		self.leafs = self.leafs.intersection(ok)
		# print('leafs AFTER', self.leafs)
		self.tree = best
		return best.move

	def loop(self):
		START = 1
		TIME = 1
		CORNERS = {(0,0), (0,7), (7,0), (7,7)}
		while True:
			cmd, args = self.hear()
			if cmd == 'HEDID':
				unused_move_timeout, unused_game_timeout = args[:2]
				move = tuple((int(m) for m in args[2:]))
				if move == (-1, -1):
					move = None
				self.game.do_move(move, 1 - self.my_player)
				if START:
					self.tree.state.do_move(move, 1 - self.my_player)
					START = 0
				else:
					for ch in self.tree.children:
						if ch.move == move:
							self.tree = ch
							self.tree.whose_turn = 1 -self.tree.whose_turn # ????	
							break

				print('YOUDID')
				self.game.draw()
				print()
			elif cmd == 'ONEMORE':
				self.reset()
				continue
			elif cmd == 'BYE':
				break
			else:
				assert cmd == 'UGO'
				assert not self.game.move_list
				self.my_player = 0
				self.tree.whose_turn = 0

			moves = self.game.moves(self.my_player)
			better_moves = list(set(moves) & CORNERS)
			
			if better_moves:
				move = random.choice(better_moves)
				self.game.do_move(move, self.my_player)
			elif moves:
				# move = random.choice(moves)
				move = self.find_best(40)
				self.game.do_move(move, self.my_player)
			else:
				self.game.do_move(None, self.my_player)
				move = (-1, -1)
			self.say('IDO %d %d' % move)
			TIME += 1
			self.game.draw()
			print()


if __name__ == '__main__':
	player = Player()
	# player.game.draw()
	player.loop()