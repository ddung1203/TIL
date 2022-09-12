# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def solution(hour, minute):
	answer = ''
	hour_pos = (float(hour) * 30.0) + (float(minute) * 0.5)
	minute_pos = float(minute) * 6.0
	answer = abs(hour_pos - minute_pos)
	
	if answer > float(360) - answer:
		answer = float(360) - answer
	
	return "{:.1f}".format(answer)


hour = 3
minute = 0
ret = solution(hour, minute)

print("solution 함수의 반환 값은", ret, "입니다.")