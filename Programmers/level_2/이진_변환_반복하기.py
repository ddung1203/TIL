def solution(s):
    zero=0
    count=0
    tmp1=0
    tmp2=0

    while True:
        zero = s.count('0')
        tmp2 = tmp2 + zero
        count = len(s) - zero
        s = bin(count)[2:]
        tmp1 = tmp1 + 1
        
        if s == '1':
            break
    
    return tmp1, tmp2

# https://school.programmers.co.kr/learn/courses/30/lessons/70129