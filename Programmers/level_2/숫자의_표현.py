def solution(n):
    answer = 0
    
    for i in range(1, n+1):
        sum = 0
        for j in range(i, n+1):
            sum = sum + j
            if sum == n:
                answer = answer + 1
            elif sum > n:
                break
    
    return answer

# https://school.programmers.co.kr/learn/courses/30/lessons/12924