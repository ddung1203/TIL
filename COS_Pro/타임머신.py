# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(num):
	answer = ''
	tmp = num + 1
	tmp=list(str(tmp))
	for i in range(len(tmp)):
		if tmp[i] == '0':
			tmp[i] = '1'
		answer=answer+tmp[i]	
	return answer

	
num = 9949999;
ret = solution(num)
 
print("solution 함수의 반환 값은", ret, "입니다.")