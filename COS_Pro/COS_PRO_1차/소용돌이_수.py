# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(n):
	answer = 0
	
	if n == 1:
		return 1
	if n == 2:
		return 4
	else:
		answer = n*2 + (n-1)*4*(n-2) + solution(n-2)

	return answer

n1 = 3
ret1 = solution(n1)

print("solution 함수의 반환 값은", ret1, "입니다.")
    
n2 = 2
ret2 = solution(n2)

print("solution 함수의 반환 값은", ret2, "입니다.")