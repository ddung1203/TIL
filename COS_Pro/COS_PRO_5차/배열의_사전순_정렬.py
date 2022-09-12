# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(numbers):
	answer = []
	numbers.sort()
	mid = (len(numbers) - 1) // 2
	numbers[mid], numbers[len(numbers)-1] = numbers[len(numbers)-1], numbers[mid]
	left = mid + 1
	right = len(numbers) - 2
	while left <= right:
		numbers[left], numbers[right] = numbers[right], numbers[left]
		left = left + 1
		right = right - 1
	answer = numbers
	return answer

numbers = [7, 3, 4, 1, 2, 5, 6]
ret = solution(numbers)

print("solution 함수의 반환 값은", ret, "입니다.")