#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Losowy agent do Reversi.
'''


import random
import sys
from math import inf
import numpy as np
import math
from copy import deepcopy
from numpy import log as ln

# def deepcopy(obj):
# 	res = Reversi()
# 	res.board = np.array(obj.board.copy())
# 	res.fields = obj.fields.copy()
# 	return res

def expand(node, who_am_i):
	new_leafs = []
	for m in node.state.moves(node.whose_turn):
		new_state = deepcopy(node.state)
		new_state.do_move(m, node.whose_turn)
		child = Node()
		child.parent = node
		child.state = new_state
		child.move_done = m
		child.whose_turn = 1 - node.whose_turn
		node.children.add(child)
	return new_leafs

class Node:
	def __init__(self):
		self.t = 0
		self.n = 0
		self.parent = None
		self.state = None
		self.children = set()
		self.move_done = None
		self.whose_turn = None

	def expand(self, who_am_i):
		new_leafs = []
		for m in self.state.moves(self.whose_turn):
			new_state = deepcopy(self.state)
			new_state.do_move(m, self.whose_turn)
			child = Node()
			child.parent = self
			child.state = new_state
			child.move_done = m
			child.whose_turn = 1 - self.whose_turn
			self.children.add(child)
			new_leafs.append(child)

			if new_state.terminal():
				if am_i_winning(who_am_i): child.t = inf
				else: child.t = -inf
		return new_leafs

	def find_leafs(node):
		if len(node.children) == 0:
			res = set()
			res.add(node)
			return res
		else:
			res = set()
			for ch in node.children:
				res = res | Node.find_leafs(ch)
			return res


def propagate_score(node, score):

	while node != None:
		node.n += 1
		node.t += score
		node = node.parent

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

	# na oko
	def am_i_winning(self, me):
		counter = 0
		for y in range(self.M):
			for x in range(self.M):
				if self.board[y][x] == me: counter += 1
		return counter >= 32


class Player(object):
	def __init__(self):
		self.reset()

	def reset(self):
		self.my_player = 1
		self.root = Node()
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

	def simulate(state, whose_turn, me):
		while not state.terminal():
			moves = state.moves(whose_turn)
			if moves:
				move = random.choice(moves)
				state.do_move(move, whose_turn)
			else:
				state.do_move(None, whose_turn)
			whose_turn = 1 - whose_turn

		if state.am_i_winning(me):
			return 4
		return 0

	def USB1(leaf, iteration):
		C = 2
		if leaf.n == 0: return inf
		return (leaf.t / leaf.n) + C * pow(ln(iteration) / leaf.n, 1/2)

	def find_best_move(self, moves, iterations):
		for i in range(1, iterations + 1):
			node_to_simulate = max(self.leafs, key=lambda x: Player.USB1(x, i))
			if node_to_simulate.n == 0:
				score = Player.simulate(deepcopy(node_to_simulate.state), node_to_simulate.whose_turn, self.my_player)
				propagate_score(node_to_simulate, score)
			else:
				if not node_to_simulate.state.terminal():
					self.leafs.remove(node_to_simulate)
					new_leafs = expand(node_to_simulate, self.my_player)
					for l in new_leafs: self.leafs.add(l)
					node_to_simulate = max(self.leafs, key=lambda x: Player.USB1(x, i))
					score = Player.simulate(deepcopy(node_to_simulate.state), node_to_simulate.whose_turn, self.my_player)
					propagate_score(node_to_simulate, score)
				elif node_to_simulate.t == inf: break
		best = max(self.root.children, key=lambda x: x.t / x.n if x.n != 0 else 0)
		return best

	def loop(self):
		CORNERS = { (0,0), (0,7), (7,0), (7,7)}
		FIRST_MOVE = True
		while True:
			cmd, args = self.hear()
			if cmd == 'HEDID':
				unused_move_timeout, unused_game_timeout = args[:2]
				move = tuple((int(m) for m in args[2:]))
				if move == (-1, -1):
					move = None
				if FIRST_MOVE:
					self.root.state.do_move(move, 1 - self.my_player)
					self.root.whose_turn = self.my_player
				else:
					for ch in self.root.children:
						if ch.move_done == move and ch.whose_turn == 1 - self.my_player:
							self.root = ch
							self.leafs = Node.find_leafs(self.root)
				print('YOUDID', move)
				self.root.state.draw()
				print()
			elif cmd == 'ONEMORE':
				self.reset()
				continue
			elif cmd == 'BYE':
				break
			else:
				assert cmd == 'UGO'
				assert not self.root.state.move_list
				self.my_player = 0
				self.root.whose_turn = 0

			moves = self.root.state.moves(self.my_player)
			  
			if moves:
				# move = random.choice(moves)
				# print('MY TURN')
				# print('STATE BEFORE MOVE')
				# self.root.state.draw()
				# print('whose turn', self.root.whose_turn)
				# print('me', self.my_player)

				# print('CHLDREN BELOW')
				# for ch in self.root.children:
				# 	print(ch.whose_turn)
				# 	ch.state.draw()
				# if len(self.root.children) != 0:
				# 	temp = list(self.root.children)
				# 	print('PRINTING FATHER')
				# 	temp[0].parent.state.draw()
				# print('CHILDREN END')
				best_node = self.find_best_move(moves, 40)
				# assert best_node.whose_turn == 1 - self.my_player

				# making move
				self.root = best_node
				self.leafs = set(Node.find_leafs(best_node))
				move = self.root.move_done
			else:
				self.root.state.do_move(None, self.my_player)
				self.root.children = set()
				self.leafs = set()
				self.root.whose_turn = 1 - self.my_player
				move = (-1, -1)
			self.say('IDO %d %d' % move)
			self.root.state.draw()
			print()


if __name__ == '__main__':
	player = Player()
	# player.root.state.draw()
	player.loop()
