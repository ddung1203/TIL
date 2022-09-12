# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(number):
	answer = ''
	number_count = [0 for _ in range(10)]
	while number > 0:
		number_count[number % 10] += 1
		number //= 10
	for i in range(9, -1, -1):
		if number_count[i] != 0:
			answer += (str(i) + str(number_count[i]))
	return answer

number1 = 2433
ret1 = solution(number1)

print("solution 함수의 반환 값은", ret1, "입니다.")

number2 = 662244
ret2 = solution(number2)

print("solution 함수의 반환 값은", ret2, "입니다.")