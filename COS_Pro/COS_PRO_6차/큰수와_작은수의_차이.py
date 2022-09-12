# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(arr, K):
	answer = 10001
	lis = []
	
	for i in range(len(arr)):
		for j in range(i+1, len(arr)):
			for l in range(j + 1, len(arr)):
				for k in range(l + 1, len(arr)):
					lis.append([arr[i],arr[j],arr[l],arr[k]])
	
	for i in range(len(lis)):
		mi = min(lis[i])
		ma = max(lis[i])
		if answer > ma - mi:
			answer = ma - mi
	
	return answer

arr = [9, 11, 9, 6, 4, 19]
K = 4
ret = solution(arr, K)

print("solution 함수의 반환 값은", ret, "입니다.")