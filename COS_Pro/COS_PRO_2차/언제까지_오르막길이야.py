def solution(arr):
	lis = []
	for i in range(len(arr)):
		answer = 0
		while i+1 < len(arr):
			if arr[i] < arr[i+1]:
				answer = answer + 1
			if arr[i] >= arr[i+1]:
				break
			i = i + 1

		lis.append(answer)
	return max(lis)+1


arr = [3, 1, 2, 4, 5, 1, 2, 2, 3, 4]
ret = solution(arr)

print("solution 함수의 반환 값은", ret, "입니다.")