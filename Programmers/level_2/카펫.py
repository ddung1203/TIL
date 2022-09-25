def solution(brown, yellow):
    answer = []
    tmp = []
    
    for i in range(1, brown+yellow+1):
        if (brown+yellow) % i == 0:
            tmp.append(i)
            
    if len(tmp)%2 == 1:
        answer.append(tmp[(len(tmp)//2)])
        answer.append(tmp[(len(tmp)//2)])
        
    elif len(tmp)%2 != 1 and (tmp[len(tmp)//2] - 2) * (tmp[(len(tmp)//2)-1] - 2) == yellow:
        answer.append(tmp[len(tmp)//2])
        answer.append(tmp[(len(tmp)//2)-1])
        
    else:
        while (tmp[len(tmp)//2] - 2) * (tmp[(len(tmp)//2)-1] - 2) != yellow:
            tmp.remove(tmp[len(tmp)//2])
            tmp.remove(tmp[len(tmp)//2])
        answer.append(tmp[len(tmp)//2])
        answer.append(tmp[(len(tmp)//2)-1])
        
    return answer

# https://school.programmers.co.kr/learn/courses/30/lessons/42842#