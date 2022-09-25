def solution(s):
    answer = ''
    lis = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    s=s.lower()
    
    for i in range(len(s)):
        if s[i-1] == ' ' and s[i] in lis:
            answer = answer + s[i].upper()
        elif i == 0 and s[i] in lis:
            answer = answer + s[i].upper()
        else:
            answer = answer + s[i]
        
    return answer

# https://school.programmers.co.kr/learn/courses/30/lessons/12951