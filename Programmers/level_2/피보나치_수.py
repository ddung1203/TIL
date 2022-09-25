def solution(n):
    answer = 0
    
    a = 0
    b = 1
    
    for i in range(n):
        tmp = a
        a = b
        b = b + tmp
    
    return a % 1234567

# https://school.programmers.co.kr/learn/courses/30/lessons/12945