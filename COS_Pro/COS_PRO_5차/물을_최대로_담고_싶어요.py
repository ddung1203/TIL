# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(walls):
	answer = 0
	for i in range(len(walls)):
		for j in range(i+1, len(walls)):
			area = 0
			if walls[i][1] < walls[j][1]:
				area = walls[i][1] * (walls[j][0] - walls[i][0])
			else:
				area = walls[j][1] * (walls[j][0] - walls[i][0])
			if answer < area:
				answer = area
	return answer

walls = [[1, 4], [2, 6], [3, 5], [5, 3], [6, 2]]
ret = solution(walls)

print("solution 함수의 반환 값은", ret, "입니다.")