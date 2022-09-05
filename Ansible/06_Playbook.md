# Playbook
- playbook: YAML 파일
	- `.yaml`, `.yml`
- play
- task

`test.yaml`
``` yaml
# Play
- hosts: host1
  tasks:
  # Task
  - apt:
      name: apache2
      state: installed
  # Task
  - service:
      name: apache2
      state: started
      enabled: yes
```

| 참고

`ansible node1 -m apt -a 'name=apache2 state=installed'`

`ansible node1 -m service -a 'name=apache2 state=started enabled=yes'`

플레이북 실행
``` bash
ansible-playbook test.yaml
```

YAML 문법 확인
``` bash
ansible-playbook wordpress.yaml --syntax-check
```

플레이북 시뮬레이션
``` bash
ansible-playbook wordpress.yaml --check
```

텍스트의 변경 사항 확인
``` bash
ansible-playbook wordpress.yaml --diff
```
--check 옵션과 함께 사용하는 경우가 많다.

실행할 시스템 제한
``` bash
ansible-playbook wordpress.yaml --limit 192.168.100.11
```

적용할 호스트 목록
``` bash
ansible-playbook wordpress.yaml --list-hosts
```

플레이북의 작업 목록
``` bash
ansible-playbook wordpress.yaml --list-tasts
```

플레이북의 태그 목록
``` bash
ansible-playbook wordpress.yaml --list-tags
```