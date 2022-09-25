def solution(s):
    answer = 0
    lis = []
    
    for i in range(len(s)):
        if not lis:
            lis.append(s[i])
        else:
            if s[i] == lis[-1]:
                lis.pop()
            else:
                lis.append(s[i])
                
    if not lis:
        return 1
    else:
        return 0

# https://school.programmers.co.kr/learn/courses/30/lessons/12973