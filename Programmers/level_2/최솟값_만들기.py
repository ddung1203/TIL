def solution(A,B):
    answer = 0

    A.sort()
    B.sort()
    B.reverse()
    
    for i in range(len(A)):
        answer = answer + A[i]*B[i]

    return answer

# https://school.programmers.co.kr/learn/courses/30/lessons/12941