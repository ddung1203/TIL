# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
def solution(K, numbers, up_down):
	left = 1
	right = K
	for num, word in zip(numbers, up_down):
		if word == "UP":
			left = max(num, left)
		elif word == "DOWN":
			right = min(num, right)
		elif word == "RIGHT":
			return 1
	return right - left - 1

K1 = 10
numbers1 = [4, 9, 6]
up_down1 = ["UP", "DOWN", "UP"]
ret1 = solution(K1, numbers1, up_down1)

print("solution 함수의 반환 값은", ret1, "입니다.")

K2 = 10
numbers2 = [2, 1, 6]
up_down2 = ["UP", "UP", "DOWN"]
ret2 = solution(K2, numbers2, up_down2)

print("solution 함수의 반환 값은", ret2, "입니다.")

K3 = 100
numbers3 = [97, 98]
up_down3 = ["UP", "RIGHT"]
ret3 = solution(K3, numbers3, up_down3)

print("solution 함수의 반환 값은", ret3, "입니다.")