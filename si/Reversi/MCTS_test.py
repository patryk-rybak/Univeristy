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

	def expand(self):
		new_leafs = set()
		for m in self.state.moves(self.whose_turn):
			new_state = deepcopy(self.state)
			new_state.do_move(m, self.whose_turn)
			new_node = Node(1 - self.whose_turn, new_state, self, m)
			new_node.parent = self
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


# correcting leafs
def find_leafs(node):
	if len(node.children) == 0:
		res = set()
		res.add(node)
		return res
	else:
		res = set()
		for ch in node.children:
			res = res | find_leafs(ch)
		return res

class Player(object):
	def __init__(self):
		self.reset()

	def reset(self):
		self.my_player = 1
		self.root = Node(self.my_player)
		self.root.state = Reversi()
		self.root.whose_turn = self.my_player
		self.leafs = set()
		self.leafs.add(self.root)
		self.say('RDY')

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

		# ogarnac od nowa
		def simulate(state, whose_turn):
			while not state.terminal():
				moves = state.moves(whose_turn)
				if len(moves) != 0: move = random.choice(moves)
				else: move = None
				state.do_move(move, whose_turn)
				whose_turn = 1 - whose_turn
			points = 0
			for y in range(self.root.state.M):
				for x in range(self.root.state.M):
					if state.board[y][x] == self.my_player: points += 1
			if points > 32: return 4
			elif points == 32: return 2
			return 0

		for i in range(1, iterations + 1):
			node_to_simulate = max(self.leafs, key=lambda x: Player.USB1(x, i))
			if node_to_simulate.n != 0:
				if not node_to_simulate.state.terminal():
					self.leafs.remove(node_to_simulate)
				temp = node_to_simulate.expand()
				# for kkk in temp: print(kkk.whose_turn)
				for j in temp: self.leafs.add(j)
				node_to_simulate = max(self.leafs, key=lambda x: Player.USB1(x, i))
			score = simulate(deepcopy(node_to_simulate.state), node_to_simulate.whose_turn)
			node_to_simulate.t += score
			node_to_simulate.n += 1

		# propagation
		while node_to_simulate.parent != None:
			node_to_simulate = node_to_simulate.parent
			node_to_simulate.n += 1
			node_to_simulate.t += score

		best = max(self.root.children, key=lambda x: x.t / x.n if x.n != 0 else 0)

		ok = find_leafs(best)
		# print('LEN LEAFS', len(self.leafs))
		self.leafs = ok
		# print('LEN LEAFS', len(self.leafs))
		self.root = best
		return best.move

	def loop(self):
		FIRST_MOVE = True
		TIME = 1
		CORNERS = {(0,0), (0,7), (7,0), (7,7)}
		while True:
			cmd, args = self.hear()
			if cmd == 'HEDID':
				unused_move_timeout, unused_game_timeout = args[:2]
				move = tuple((int(m) for m in args[2:]))
				# print('aktualny', move)
				if move == (-1, -1):
					move = None
				if FIRST_MOVE:
					FIRST_MOVE = False
					self.root.state.do_move(move, 1 - self.my_player)
					assert self.root.whose_turn == self.my_player
				else:
					# print('len(self.root.children)', len(self.root.children))
					# assert self.root.whose_turn == 1 - self.my_player
					for ch in self.root.children:
						# print('ch.move', ch.move)
						if ch.move == move and ch.whose_turn == 1 - self.root.whose_turn:
							self.root = ch
							# print('kogo bedzie tura', self.root.whose_turn)
							# print('kim jestem', self.my_player)
							break

					self.leafs = find_leafs(self.root)

				print('YOUDID')
				self.root.state.draw()
				print()
			elif cmd == 'ONEMORE':
				self.reset()
				continue
			elif cmd == 'BYE':
				break
			else:
				assert cmd == 'UGO'
				FIRST_MOVE = False
				assert not self.root.state.move_list
				self.my_player = 0
				self.root.whose_turn = 0
			# print('whose turn', self.root.whose_turn)
			# print('me', self.my_player)
			moves = self.root.state.moves(self.my_player)

			if moves:
				move = self.find_best(40)
			else:
				# self.game.do_move(None, self.my_player)
				move = (-1, -1)
			self.say('IDO %d %d' % move)
			TIME += 1
			self.root.state.draw()
			print()


if __name__ == '__main__':
	player = Player()
	player.root.state.draw()
	player.loop()