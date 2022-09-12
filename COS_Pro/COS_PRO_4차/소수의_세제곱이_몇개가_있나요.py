# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
def sosu(a):
	for i in range(2, a):
		if a % i != 0:
			return 1
		else:
			return -1

def solution(a, b):
	answer = 0
	tmp = int(b**(1/2))+1
	lis = [2]
	
	for i in range(2, tmp):
		if sosu(i) == 1:
			lis.append(i)
	
	lis2 = []
	for i in lis:
		if a <= i*i <= b:
			lis2.append(i*i)
	
	lis3 = []
	for i in lis:
		if a <= i*i*i <= b:
			lis3.append(i*i*i)
		
	answer = len(lis2) + len(lis3)
	return answer

a =  6
b =  30
ret = solution(a, b)

print("solution 함수의 반환 값은", ret, "입니다.")