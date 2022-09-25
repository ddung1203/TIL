def solution(s):
    answer = True
    tmp1 = []
    
    if s[0] == ')':
        return False
    
    for i in range(len(s)):
        if s[i] == '(':
            tmp1.append(s[i])
        elif len(tmp1) > 0 and s[i] == ')':
            tmp1.pop()
    
    if len(tmp1) > 0:
        return False
    
    return True

# https://school.programmers.co.kr/learn/courses/30/lessons/12909#