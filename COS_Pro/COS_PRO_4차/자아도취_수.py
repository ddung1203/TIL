# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
def power(base, exponent):
	val = 1
	for i in range(exponent):
		val *= base
	return val

def solution(k):
	answer = []
	bound = power(10, k) #1000
	for i in range(bound // 10, bound): #100, 1000
		current = i
		calculated = 0
		while current != 0:
			if i == (i//100)*(i//100)*(i//100) + (i%100//10)*(i%100//10)*(i%100//10) + (i%10)//1*(i%10)//1*(i%10)//1:
				calculated = i
				break
			else:
				break
			# 정답
			#calculated = calculated + power(current % 10, k)
			#current = current // 10
		if calculated == i:
			answer.append(i)
	return answer


k = 3
ret = solution(k)

print("solution 함수의 반환 값은", ret, "입니다.")