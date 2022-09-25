def solution(n, words):
    
    for i in range(1, len(words)):
        if words[i][0] != words[i-1][-1] or words[i] in words[:i]:
            return [(i%n)+1, (i//n)+1]
    else:
        return [0,0]

# https://school.programmers.co.kr/learn/courses/30/lessons/12981