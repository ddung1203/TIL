# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
def solution(n):
	answer = 0
	primes = [2]
	for i in range (3, n + 1, 2) :
		is_prime = True
		for j in range(2, i) :
			if i % j == 0 :
				is_prime = False
				break
		if is_prime == True:
			primes.append(i)
	
	prime_len = len(primes)
	for i in range(0, prime_len - 2) :
		for j in range(i + 1, prime_len - 1) :
			for k in range(j + 1, prime_len) :
				if primes[i] + primes[j] + primes[k] == n:
					answer += 1
	return answer


n1 = 33
ret1 = solution(n1)

print("solution 함수의 반환 값은", ret1, "입니다.")

n2 = 9
ret2 = solution(n2)

print("solution 함수의 반환 값은", ret2, "입니다.")