def solution(bishops):
	answer = 64
	lis = [[0 for i in range(8)] for i in range(8)]
	
	for i in range(len(bishops)):
		a = int(bishops[i][1])-1
		b = ord(bishops[i][0])-65
	
		while 0 <= a < 8 and 0 <= b < 8:
			lis[a][b] = 1
			a = a - 1
			b = b - 1
		
		a = int(bishops[i][1])-1
		b = ord(bishops[i][0])-65
		
		while 0 <= a < 8 and 0 <= b < 8:
			lis[a][b] = 1
			a = a - 1
			b = b + 1
		
		a = int(bishops[i][1])-1
		b = ord(bishops[i][0])-65
		
		while 0 <= a < 8 and 0 <= b < 8:
			lis[a][b] = 1
			a = a + 1
			b = b - 1
		
		a = int(bishops[i][1])-1
		b = ord(bishops[i][0])-65
		
		while 0 <= a < 8 and 0 <= b < 8:
			lis[a][b] = 1
			a = a + 1
			b = b + 1

	for i in lis:
		answer = answer - i.count(1)
	
	return answer


bishops1 = ["D5"]
ret1 = solution(bishops1)

print("solution 함수의 반환 값은", ret1, "입니다.")

bishops2 = ["D5", "E8", "G2"]
ret2 = solution(bishops2)

print("solution 함수의 반환 값은", ret2, "입니다.")