# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean


def solution(s1, s2, p, q):
	answer = ''
	s1_=0
	s2_=0
	
	for i in range(1, len(s1)+1):
		s1_ = s1_ + (p**(i-1) * int(s1[-i]))
	for i in range(1, len(s2)+1):
		s2_ = s2_ + (p**(i-1) * int(s2[-i]))
	
	tmp = s1_ + s2_
	
	while tmp != 0:
		answer = str(tmp%q) + answer
		tmp = tmp // q
	
	return answer

s1 = "112001"
s2 = "12010"
p = 3
q = 8
ret = solution(s1, s2, p, q)

print("solution 함수의 반환 값은", ret, "입니다.")