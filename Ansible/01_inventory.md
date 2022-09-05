# 정적 인벤토리
| https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#intro-inventory
기본 인벤토리 파일: `/etc/ansible/hosts`
- 잘 사용하지 않는다.

기본 위치에 있는 인벤토리 파일 아니면 -i 옵션 사용
포멧: ini, yaml
ini 예시
``` ini
key=value

[Section]
key=value
key
```

```
mail.example.com

[webservers]
foo.example.com
bar.example.com
three.example.com

[dbservers]
one.example.com
two.example.com
three.example.com
```

`[ ]`: 인벤토리 그룹

하나의 노드는 하나의 그룹에만 속해야 한다: False
``` ini
all:
  hosts:
    mail.example.com:
  children:
    webservers:
      hosts:
        foo.example.com:
        bar.example.com:
    dbservers:
      hosts:
        one.example.com:
        two.example.com:
        three.example.com:
```

기본 그룹
- 주의: 인벤토리 생성은 간결하게 할 것
- all
- ungrouped

그룹에 호스트를 분류
- what
- where
- when

호스트의 범위
``` ini
[webservers]
www[01:50].example.com
192.168.100.[10:19]
```

인벤토리 변수
``` ini
[webservers]
www[01:50].example.com A=100 B=200
192.168.100.[10:19]
```

인벤토리 그룹 변수
``` ini
[atlanta]
host1
host2

[atlanta:vars]
ntp_server=ntp.atlanta.example.com
proxy=proxy.atlanta.example.com
```

중첩 그룹
``` ini
[atlanta]
host1
host2

[raleigh]
host2
host3

[southeast:children]
atlanta
raleigh

[usa:children]
southeast
```

## 인벤토리 파일 확인
생성한 인벤토리 파일 계층 구조 확인
```
ansible-inventory -i <INVENTORY_FILE> --graph
```

JSON 형식 및 호스트/그룹 변수
```
ansible-inventory -i <INVENTORY_FILE> --list
```

호스트에 설정된 변수 확인
```
ansible-inventory -i <INVENTORY_FILE> --host <HOST>
```

호스트 매칭 확인
```
ansible <HOST_PATTERN> -i <INVENTORY_FILE> --list-hosts
```