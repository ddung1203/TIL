# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
def where(commands, i):
	if commands[i] == 'U':
		return [0, 1]
	elif commands[i] == 'D':
		return [0, -1]
	elif commands[i] == 'L':
		return [-1, 0]
	else:
		return [1, 0]

def solution(commands):
	answer = [0, 0]
	for i in range(len(commands)):
		tmp = where(commands, i)
		
		answer[0] = answer[0] + tmp[0]
		answer[1] = answer[1] + tmp[1]
	return answer


commands = "URDDL"
ret = solution(commands)

print("solution 함수의 반환 값은", ret, "입니다.")