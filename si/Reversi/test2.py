#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import random
import sys
from copy import deepcopy
from math import inf

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

	def __eval(self):
		static_core = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20],
        ]

		# Coin Parity & Static Score
		max_player_coins = 0
		min_player_coins = 0
		max_val = 0
		min_val = 0
		for i in range(self.M):
			for j in range(self.M):
				if self.board[i][j] == 1:
					max_player_coins += 1
					max_val += static_core[i][j]
				elif self.board[i][j] == 0:
					min_player_coins += 1
					min_val += static_core[i][j]
		if (max_val + min_val) != 0:
			static_score_heuristic_value = 100 * (max_val - min_val) / (max_val + min_val)
		else: static_score_heuristic_value = 0
		if max_player_coins > min_player_coins:
			coin_parity_heuristic_value = 100 * max_player_coins / (max_player_coins + min_player_coins)
		elif max_player_coins < min_player_coins:
			coin_parity_heuristic_value = 100 * min_player_coins / (max_player_coins + min_player_coins)
		else: coin_parity_heuristic_value = 0


		# Mobility
		max_player_actual_mobility_value = len(self.moves(1))
		min_player_actual_mobility_value = len(self.moves(0))
		if (max_player_actual_mobility_value + min_player_actual_mobility_value) != 0:
			actual_mobility_heuristic_value = 100 * (max_player_actual_mobility_value - min_player_actual_mobility_value) / (max_player_actual_mobility_value + min_player_actual_mobility_value)
		else:
			actual_mobility_heuristic_value = 0

		# Corners Captured & Stability
		max_min_player_corner_value = [0, 0]
		max_min_palyer_stability_value = [0, 0]
		corner = self.board[0][0]
		if corner != None:
			max_min_player_corner_value[corner] += 1
			max_min_palyer_stability_value[corner] += 1
			index_col, index_row = 1, 1
			while self.board[0][index_row] == corner and index_row < self.M - 1:
				max_min_palyer_stability_value[corner] += 1
				index_row += 1
			while self.board[index_col][0] == corner and index_col < self.M - 1:
				max_min_palyer_stability_value[corner] += 1
				index_col += 1
		corner = self.board[self.M - 1][0]
		if corner != None: 
			max_min_player_corner_value[corner] += 1
			max_min_palyer_stability_value[corner] += 1
			index_col, index_row = self.M - 2, 1
			while self.board[self.M - 1][index_row] == corner and index_row < self.M - 1:
				max_min_palyer_stability_value[corner] += 1
				index_row += 1
			while self.board[index_col][0] == corner and index_col > 0:
				max_min_palyer_stability_value[corner] += 1
				index_col -= 1
		corner = self.board[0][self.M - 1]
		if corner != None:
			max_min_player_corner_value[corner] += 1
			max_min_palyer_stability_value[corner] += 1
			index_col, index_row = 1, self.M - 2
			while self.board[0][index_row] == corner and index_row > 0:
				max_min_palyer_stability_value[corner] += 1
				index_row -= 1
			while self.board[index_col][self.M - 1] == corner and index_col < self.M - 1:
				max_min_palyer_stability_value[corner] += 1
				index_col += 1
		corner = self.board[self.M - 1][self.M - 1]
		if corner != None:
			max_min_player_corner_value[corner] += 1
			max_min_palyer_stability_value[corner] += 1
			index_col, index_row = self.M - 2, self.M - 2
			while self.board[self.M - 1][index_row] == corner and index_row > 0:
				max_min_palyer_stability_value[corner] += 1
				index_row -= 1
			while self.board[index_col][self.M - 1] == corner and index_col > 0:
				max_min_palyer_stability_value[corner] += 1
				index_col -= 1
		if sum(max_min_player_corner_value) != 0:
			corners_captured_heuristic_value = 100 * (max_min_player_corner_value[0] - max_min_player_corner_value[1]) / sum(max_min_player_corner_value)
		else: corners_captured_heuristic_value = 0
		if sum(max_min_palyer_stability_value) != 0:
			stable_coins_heuristic_value = 100 * (max_min_palyer_stability_value[0] - max_min_palyer_stability_value[1]) / sum(max_min_palyer_stability_value)
		else: stable_coins_heuristic_value = 0

		# print('corners_captured_heuristic_value', corners_captured_heuristic_value)
		# print('actual_mobility_heuristic_value', actual_mobility_heuristic_value)
		# print('stable_coins_heuristic_value', stable_coins_heuristic_value)
		# print('static_score_heuristic_value', static_score_heuristic_value)
		# print('coin_parity_heuristic_value', coin_parity_heuristic_value) G

		return (2 * max_player_coins * coin_parity_heuristic_value) + (9000 * corners_captured_heuristic_value) + (10 * static_score_heuristic_value) + (784 * actual_mobility_heuristic_value) + (382 * stable_coins_heuristic_value)

	def heuristic(self, move, player):
		temp = deepcopy(self)
		temp.do_move(move, player)
		sub_states_after_move = set()
		for m in temp.moves(1 - player):
			temp2 = deepcopy(temp)
			temp2.do_move(m, 1 - player)
			sub_states_after_move.add(temp2.__eval())
		if len(sub_states_after_move) != 0:
			return sum(sub_states_after_move) / len(sub_states_after_move)
		return +inf



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
		CORNERS = { (0,0), (0,7), (7,0), (7,7)}
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
			better_moves = list(set(moves) & CORNERS)
			
			if better_moves:
				move = random.choice(better_moves)
				self.game.do_move(move, self.my_player)
			elif moves:
				# move = random.choice(moves)
				heuristic_vals = {(self.game.heuristic(m, self.my_player), m) for m in moves}
				move = max(heuristic_vals, key=lambda x: x[0])[1]
				self.game.do_move(move, self.my_player)
			else:
				self.game.do_move(None, self.my_player)
				move = (-1, -1)
			self.say('IDO %d %d' % move)
			# self.game.draw()


if __name__ == '__main__':
	player = Player()
	# player.game.draw()
	player.loop()
