# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(s):
	s = s.lower()
	answer = ""
	previous = s[0]
	counter = 1
	for alphabet in s[1:]:
		if alphabet == previous:
			counter += 1
		else:
			answer += previous + str(counter)
			counter = 1
			previous = alphabet
	answer += previous + str(counter)
	return answer


s = "YYYYYbbbBbbBBBMmmM"
ret = solution(s)

print("solution 함수의 반환 값은", ret, "입니다.")