# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean


def solution(K, words):
	answer = 1
	
	Len = 0
	
	for i in range(len(words)):
		Len = Len + len(words[i])+1
		if (Len > K+1):
			answer = answer + 1
			Len = len(words[i]) + 1
				
	return answer

K = 10
words = ["nice", "happy", "hello", "world", "hi"]
ret = solution(10, words)

print("solution 함수의 반환 값은", ret, "입니다.")