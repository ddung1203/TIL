# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def func(record):
	if record == 0:
		return 1
	elif record == 1:
		return 2
	return 0

def solution(recordA, recordB):
	cnt = 0
	for i in range(len(recordA)):
		if recordA[i] == recordB[i]:
			continue
		elif recordA[i] == func(recordB[i]):
			cnt = cnt + 3
		else:
			cnt = cnt - 1
		if cnt < 0:
			cnt = 0
	return cnt

recordA = [2,0,0,0,0,0,1,1,0,0]
recordB = [0,0,0,0,2,2,0,2,2,2]
ret = solution(recordA, recordB)


print("solution 함수의 반환 값은", ret, "입니다.")