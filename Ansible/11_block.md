# 블록

블록이란? 여러 작업을 묶어 놓은 그룹

블록의 기능
1. 여러 작업에 공통의 키워드를 부여할 수 있음(예. 조건문)
2. `block`, `rescue`, `always` 블록을 이용해 오류 처리를 할 수 있음

`block`: 블록은 항상 실행
`rescue`: `block`의 오류가 있을 때만 실행
`always`: 항상 실행

``` yaml
- hosts: 192.168.100.11

  tasks:
    - block:
        - debug:
            msg: hello world
        - command: /usr/bin/false
        - debug:
            msg: hello world2
      ignore_errors: yes

      rescue:
        - debug:
            msg: It's rescue

      always:
        - debug:
            msg: It's Always
```