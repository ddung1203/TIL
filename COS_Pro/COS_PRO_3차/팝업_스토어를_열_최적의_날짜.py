# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(revenue, k) :
	answer = 0
	rsum = sum(revenue[0:k])
	answer = rsum
	for i in range(k, len(revenue)) :
		rsum = rsum - revenue[i - k] + revenue[i]
		if answer < rsum :
			answer = rsum
	return answer


revenue1 = [1, 1, 9, 3, 7, 6, 5, 10]
k1 = 4
ret1 = solution(revenue1, k1)

print("solution 함수의 반환 값은", ret1, "입니다.")

revenue2 = [1, 1, 5, 1, 1]
k2 = 1
ret2 = solution(revenue2, k2)

print("solution 함수의 반환 값은", ret2, "입니다.")