# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
def func_a(n):
	ret = 1
	while n > 0:
		ret *= 10
		n -= 1
	return ret

def func_b(n):
	ret = 0
	while n > 0:
		ret += 1
		n //= 10
	return ret

def func_c(n):
	ret = 0
	while n > 0:
		ret += n%10
		n //= 10
	return ret

def solution(num):
	next_num = num
	while True:
		next_num += 1
		length = func_b(next_num)
		if length % 2:
			continue
		divisor = func_a(length//2)  
		front = next_num // divisor
		back = next_num % divisor

		front_sum = func_c(front)
		back_sum = func_c(back)
		if front_sum == back_sum:
			break
	return next_num - num


num1 = 1
ret1 = solution(num1)

print("solution 함수의 반환 값은", ret1, "입니다.")

num2 = 235386
ret2 = solution(num2)

print("solution 함수의 반환 값은", ret2, "입니다.")