# 태그

작업에 태그를 부여하고, 특정 태그의 작업만 실행할 수 있음

``` yaml
- hosts: 192.168.100.11
  gather_facts: no

  tasks:
    - debug:
        msg: "web server stage"
      tags:
        - stage
    - debug:
        msg: "web server product"
      tags:
        - prod
    - debug:
        msg: "web server all"
```

all 태그: 모든 작업이 속함
untagged 태그: 태그가 설정되어 있지 않는 작업 속함

``` bash
ansible-playbook test.yaml --tags=stage, prod
```

태그 확인
``` bash
ansible-playbook test.yaml --start-at-task="tasks3"
```

``` bash
ansible-playbook test.yaml --start-at-task="task3" --limit 192.168.100.12
```