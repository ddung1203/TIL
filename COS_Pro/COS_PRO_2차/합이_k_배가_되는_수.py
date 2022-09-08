# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(arr, K):
	answer = 0
	n = len(arr)
			
	for p in range(0, n):
		for q in range(p+1, n):
			for r in range(q+1, n):
				if (arr[p] + arr[q] + arr[r]) % K == 0:
					answer = answer + 1
	return answer


arr = [1, 2, 3, 4, 5]
K = 3
ret = solution(arr, K)

print("solution 함수의 반환 값은", ret, "입니다.")