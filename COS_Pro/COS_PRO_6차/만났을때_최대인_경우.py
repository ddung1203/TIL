# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(grid):
	answer = 0
	for i in range(4):
		for j in range(4):
			for k in range(j + 1, 4, 2):
				answer = max(answer, max(grid[i][j] + grid[i][k], grid[i][j] + grid[k][j]))
	return answer

grid = [[1, 4, 16, 1], [20, 5, 15, 8], [6, 13, 36, 14], [20, 7, 19, 15]]
ret = solution(grid)

print("solution 함수의 반환 값은", ret, "입니다.")