#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# test2.py

import random
import sys
from math import inf
import numpy as np

def deepcopy(obj):
    res = Reversi()
    res.board = np.array(obj.board.copy())
    res.fields = obj.fields.copy()
    return res

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

	def heuristics(self, move_num, my_player):
		static_core = [
			[20, -3, 11, 8, 8, 11, -3, 20],
			[-3, -7, -4, 1, 1, -4, -7, -3],
			[11, -4, 8, 2, 2, 8, -4, 11],
			[8, 1, 2, -3, -3, 2, 1, 8],
			[8, 1, 2, -3, -3, 2, 1, 8],
			[11, -4, 8, 2, 2, 8, -4, 11],
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
				if self.board[i][j] == my_player:
					max_player_coins += 1
					max_val += static_core[i][j]
				elif self.board[i][j] == 1 - my_player:
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
		max_player_actual_mobility_value = len(self.moves(my_player))
		min_player_actual_mobility_value = len(self.moves(1 - my_player))
		if max_player_actual_mobility_value > min_player_actual_mobility_value:
			actual_mobility_heuristic_value = 100 * max_player_actual_mobility_value / (max_player_actual_mobility_value + min_player_actual_mobility_value)
		elif max_player_actual_mobility_value < min_player_actual_mobility_value:
			actual_mobility_heuristic_value = -100 * min_player_actual_mobility_value / (max_player_actual_mobility_value + min_player_actual_mobility_value)
		else: actual_mobility_heuristic_value = 0

		# Corners Captured
		max_min_player_corner_value = [0, 0]
		corner = self.board[0][0]
		if corner != None:
			max_min_player_corner_value[corner] += 1
		corner = self.board[self.M - 1][0]
		if corner != None: 
			max_min_player_corner_value[corner] += 1
		corner = self.board[0][self.M - 1]
		if corner != None:
			max_min_player_corner_value[corner] += 1
		corner = self.board[self.M - 1][self.M - 1]
		if corner != None:
			max_min_player_corner_value[corner] += 1
		if sum(max_min_player_corner_value) != 0:
			corners_captured_heuristic_value = 25 * (max_min_player_corner_value[my_player] - max_min_player_corner_value[1 - my_player])
		else: corners_captured_heuristic_value = 0

		# Stability
		max_color = my_player
		stable_coins_heuristic_value = 0
		self.board = np.array(self.board) 
		diags = [self.board[::-1,:].diagonal(i) for i in range(-3, 4)]
		diags.extend(self.board.diagonal(i) for i in range(3, -4, -1))
		diags = [n.tolist() for n in diags]
		for i in range(4):
			z = 0
			flag = False
			if flag == False:
				for o in diags[i*4:(i+1)*4+1]:
					#print(o)
					z += 1
					for a in o:
						#print(i)
						if a == max_color:
							stable_coins_heuristic_value += 3 * z	
						else:    
							flag = True
							break
		for i in range(4):
			z = 0
			flag = False
			if flag == False:
				for o in diags[i*4:(i+1)*4+1]:
					#print(o)
					z += 1
					for a in o:
						#print(i)
						if a == 1 - max_color:
							stable_coins_heuristic_value -= 3 * z
						else:    
							flag = True
							break

		return (2 * move_num * coin_parity_heuristic_value) + (9000 * corners_captured_heuristic_value) + (783.922 * actual_mobility_heuristic_value) + (10 * static_score_heuristic_value) + (10 * stable_coins_heuristic_value)

	



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

	def find_best(self, depth, moves, TIME):

		def children(state, maximizingPlayer):
			moves = state.moves(maximizingPlayer)
			for move in moves:
				new_state = deepcopy(state)
				new_state.do_move(move, maximizingPlayer)
				yield new_state

		def alphabeta(state, depth, alpha, beta, maximizingPlayer, TIME):
			if depth == 0 or state.terminal():
				return state.heuristics(TIME, self.my_player)
		
			if maximizingPlayer == self.my_player:
				maxEval = -inf
				for child in children(state, maximizingPlayer):
					eval = alphabeta(deepcopy(child), depth - 1, alpha, beta, 1 - maximizingPlayer, TIME)
					maxEval = max(maxEval, eval)
					alpha = max(alpha, eval)
					if beta <= alpha:
							break
				return maxEval
			else:
				minEval = +inf
				for child in children(state, maximizingPlayer):
					eval = alphabeta(deepcopy(child), depth - 1, alpha, beta, maximizingPlayer, TIME)
					minEval = min(minEval, eval)
					beta = min(beta, eval)
					if beta <= alpha:
							break
				return minEval

		sorted_states = []
		for m in moves:
			temp = deepcopy(self.game)
			temp.do_move(m, self.my_player)
			score = temp.heuristics(TIME, self.my_player)
			pair = (score, temp, m)
			sorted_states.append(pair)
		sorted_states.sort(reverse=True, key=lambda x: x[0])

		best_move = None
		best_score = -inf

		for board in sorted_states:
			val = alphabeta(board[1], depth, -inf, +inf, 1 - self.my_player, TIME + 1)
			if val > best_score:
				best_move = board[2]
				best_score = val
		return best_move

	def loop(self):
		TIME = 1
		CORNERS = {(0,0), (0,7), (7,0), (7,7)}
		# print('START')
		# self.game.draw()
		while True:
			cmd, args = self.hear()
			if cmd == 'HEDID':
				unused_move_timeout, unused_game_timeout = args[:2]
				move = tuple((int(m) for m in args[2:]))
				if move == (-1, -1):
					move = None
				self.game.do_move(move, 1 - self.my_player)
				# print('YOUDID')
				# self.game.draw()
				# print()
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
				# move = random.choice(moves)
				# if len(moves) >= 10: move = self.find_best(2, moves, TIME)
				# else: move = self.find_best(3, moves, TIME)
				move = self.find_best(1, moves, TIME)
				self.game.do_move(move, self.my_player)
			else:
				self.game.do_move(None, self.my_player)
				move = (-1, -1)
			self.say('IDO %d %d' % move)
			TIME += 1
			# self.game.draw()
			# print()


if __name__ == '__main__':
	player = Player()
	# player.game.draw()
	player.loop()