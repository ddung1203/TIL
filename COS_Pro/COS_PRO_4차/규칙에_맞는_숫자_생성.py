# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
def solution(n):
	answer = ''
	for i in range(n):
		answer += str(i+1)
		answer = answer[::-1]
	return answer


n = 5
ret = solution(n)

print("solution 함수의 반환 값은", ret, "입니다.")