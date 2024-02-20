#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Losowy agent do Reversi.
'''


import random
import sys
from copy import deepcopy
from math import inf

# def static_eval(state, maximizingPlayer): # maximizingPlayer niepotrzebny
# 		score = [[8, -2, 3, 3, 3, 3, -2, 8], [-2, 1, 2, 2, 2, 2, 1, -2], [3, 2, 1, 1, 1, 1, 2, 3], [3, 2, 1, 1, 1, 1, 2, 3], [3, 2, 1, 1, 1, 1, 2, 3], [3, 2, 1, 1, 1, 1, 2, 3], [-2, 1, 2, 2, 2, 2, 1, -2], [8, -2, 3, 3, 3, 3, -2, 8]]
# 		val = 0
# 		for y in range(state.M):
# 				for x in range(state.M):
# 						if state.board[y][x] == 1: val += score[y][x]
# 		return val

def static_eval(state):
	static_core = [[4, -3, 2, 2, 2, 2, -3, 4], [-3, -4, -1, -1, -1 ,-1, -4, -3], [2, -1, 1, 0, 0, 1, -1, 2], [2, -1, 0, 1, 1, 0, -1, 2], [2, -1, 0, 1, 1, 0, -1, 2], [2, -1, 1, 0, 0, 1, -1, 2], [-3, -4, -1, -1, -1, -1, -4, -3], [4, -3, 2, 2, 2, 2, -3, 4]]

	# # Coin Parity
	# max_player_coins = 0
	# min_player_coins = 0
	# for i in range(state.M):
	# 	for j in range(state.M):
	# 		if state.board[i][j] == 1: max_player_coins += 1
	# 	elif state.board[i][j] == 0: min_player_coins += 1
	# coin_parity_heuristic_value =  100 * (max_player_coins - min_player_coins) / (max_player_coins + min_player_coins)

	# Mobility
	max_player_actual_mobility_value = len(state.moves(1))
	min_player_actual_mobility_value = len(state.moves(0))
	if (max_player_actual_mobility_value + min_player_actual_mobility_value) != 0:
		actual_mobility_heuristic_value = 100 * (max_player_actual_mobility_value - min_player_actual_mobility_value) / (max_player_actual_mobility_value + min_player_actual_mobility_value)
	else:
		actual_mobility_heuristic_value = 0



	max_val = 0
	min_val = 0
	for y in range(state.M):
		for x in range(state.M):
			if state.board[y][x] == 1: max_val += static_core[y][x]
			elif state.board[y][x] == 0: min_val += static_core[y][x]
	if (max_val + min_val) != 0:
		actual_val_heuristic_value = 100 * (max_val - min_val) / (max_val + min_val)
	else:
		actual_val_heuristic_value = 0

	return 1/3 * actual_mobility_heuristic_value + 2/3 * actual_val_heuristic_value

	# # Corners Captured
	# max_player_corner_value = sum(folter(lambda x: x == 1), [state.board[0][0], state.board[0][state.M - 1], state.game.board[state.M - 1][state.M - 1], state.game.board[state.M - 1][0]])
	# min_player_corner_value = sum(folter(lambda x: x == 0), [state.board[0][0], state.board[0][state.M - 1], state.game.board[state.M - 1][state.M - 1], state.game.board[state.M - 1][0]])
	# if (max_player_corner_value + min_player_corner_value) != 0:
	# 	corner_heuristic_value =  100 * (max_player_corner_value - min_player_corner_value) / (max_player_corner_value + min_player_corner_value)
	# else:
	# 	corner_heuristic_value = 0

	# # Stability
	# #
	# #
	# #
	#




def children(state, maximizingPlayer):
		moves = state.moves(maximizingPlayer)
		for move in moves:
				new_state = deepcopy(state)
				new_state.do_move(move, maximizingPlayer)
				yield new_state

def alpha_beta(state, depth, alpha, beta, maximizingPlayer):
		if depth == 0 or state.terminal():
				return static_eval(state)
		
		if maximizingPlayer:
				maxEval = -inf
				for child in children(state, maximizingPlayer):
						eval = alpha_beta(deepcopy(child), depth - 1, alpha, beta, 0)
						maxEval = max(maxEval, eval)
						alpha = max(alpha, eval)
						if beta <= alpha:
								break
				return maxEval
		else:
				minEval = +inf
				for child in children(state, maximizingPlayer):
						eval = alpha_beta(deepcopy(child), depth - 1, alpha, beta, 1)
						minEval = min(minEval, eval)
						beta = min(beta, eval)
						if beta <= alpha:
								break
				return minEval
				

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
				# print('do_move move', move)
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

							childrenList = []
							for m in moves:
							    temp = deepcopy(self.game)
							    temp.do_move(m, self.my_player)
							    childrenList.append((m, alpha_beta(temp, 1, -inf, +inf, 1 - self.my_player)))

							# move = random.choice(moves)
							move = max(childrenList, key=lambda x: x[1])[0]
							self.game.do_move(move, self.my_player)
						else:
								self.game.do_move(None, self.my_player)
								move = (-1, -1)
						self.say('IDO %d %d' % move)



if __name__ == '__main__':
		player = Player()
		player.loop()
