# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(k, student):
	answer = 0
	for s in student:
		s -= 4*k
		if s <= 0:
			continue
		answer += (s + k - 1) // k
	return answer


k1 = 1
student1 = [4, 4, 4, 4]
ret1 = solution(k1, student1)

print("solution 함수의 반환 값은", ret1, "입니다.")

k2 = 3
student2 = [15, 17, 19, 10, 23]
ret2 = solution(k2, student2)

print("solution 함수의 반환 값은", ret2, "입니다.")