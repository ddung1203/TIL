# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(one_day_price, multi_day, multi_day_price, n):
	if one_day_price * multi_day <= multi_day_price:
		return n * one_day_price
	else:
		return (n // multi_day) * multi_day_price + (n % multi_day) * one_day_price


one_day_price1 = 3
multi_day1 = 5
multi_day_price1 = 14
n1 = 6
ret1 = solution(one_day_price1, multi_day1, multi_day_price1, n1)

print("solution 함수의 반환 값은", ret1, "입니다.")

one_day_price2 = 2
multi_day2 = 3
multi_day_price2 = 5
n2 = 11
ret2 = solution(one_day_price2, multi_day2, multi_day_price2, n2)

print("solution 함수의 반환 값은", ret2, "입니다.")