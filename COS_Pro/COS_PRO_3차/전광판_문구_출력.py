# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean


def solution(phrases, second):
	answer = ''
	st = '_' * (14-second)
	
	answer = st + phrases[:second]
			
	return answer


phrases = "happy-birthday"
second = 3
ret = solution(phrases, second)

print("solution 함수의 반환 값은", ret, "입니다.")