def solution(n):
    answer = 0
    
    tmp = bin(n)[2:].count('1')
    
    while True:
        n = n + 1
        if bin(n)[2:].count('1') == tmp:
            return n
    
# https://school.programmers.co.kr/learn/courses/30/lessons/12911