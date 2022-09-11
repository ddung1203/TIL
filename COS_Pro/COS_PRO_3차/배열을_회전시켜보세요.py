# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
def func_a(arr):
	ret = arr + arr
	return ret

def func_b(first, second):
	MAX_NUMBER = 1001
	counter = [0 for _ in range(MAX_NUMBER)]
	for f, s in zip(first, second):
		counter[f] += 1
		counter[s] -= 1
	for c in counter:
		if c != 0:
			return False
	return True

def func_c(first, second):
	length = len(second)
	for i in range(length):
		if first[i : i + length] == second:
			return True
	return False

def solution(arrA, arrB):
	if len(arrA) != len(arrB):
		return False
	if func_b(arrA, arrB):
		arrA_temp = func_a(arrA)
		if func_c(arrA_temp, arrB):
			return True
	return False

arrA1 = [1, 2, 3, 4]
arrB1 = [3, 4, 1, 2]
ret1 = solution(arrA1, arrB1)

print("solution 함수의 반환 값은", ret1, "입니다.")

arrA2 = [1, 2, 3, 4]
arrB2 = [1, 4, 2, 3]
ret2 = solution(arrA2, arrB2)

print("solution 함수의 반환 값은", ret2, "입니다.")