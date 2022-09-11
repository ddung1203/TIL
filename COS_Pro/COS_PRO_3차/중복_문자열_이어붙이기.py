def solution(s1, s2):
	answer = 0
	
	for i in range(len(s1)):
		if s1[0:i] == s2[-i:]:
			tmp1 = i
			
	for j in range(len(s2)):
		if s2[0:j] == s1[-j:]:
			tmp2 = j
	
	answer = len(s1) + len(s2) - max(tmp1, tmp2)
	
	return answer


s1 = "ababc"
s2 = "abcdab"
ret = solution(s1, s2)

print("solution 함수의 반환 값은", ret, "입니다.")