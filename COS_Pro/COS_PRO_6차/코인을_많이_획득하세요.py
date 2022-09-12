# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(board):
	coins = [[0 for c in range(4)] for r in range(4)]
	for i in range(4):
		for j in range(4):
			if i == 0 and j == 0:
				coins[i][j] = board[i][j]
			elif i == 0 and j != 0:
				coins[i][j] = board[i][j] + coins[i][j-1]
			elif i != 0 and j == 0:
				coins[i][j] = board[i][j] + coins[i-1][j]
			else:
				coins[i][j] = board[i][j] + max(coins[i-1][j], coins[i][j-1])
			print(coins)
	answer = coins[3][3]
	return answer

board = [[6, 7, 1, 2], [3, 5, 3, 9], [6, 4, 5, 2], [7, 3, 2, 6]]
ret = solution(board)

print("solution 함수의 반환 값은", ret, "입니다.")