# Docker

## Container 핵심 기술

- Cgroup: Control Group (리소스 양)
- Namespace: isolation
	- IPD NS : IPC
	- PID NS : Process
	- Network NS : Network
	- UID NS : User/Group
	- Mount NS : Mount Point
	- UTS NS : Hostname
- Layered Filesystem
	- overlay2
	- aufs (<-ufs: Union FS)

Docker = Docker Engine
Docker CE : Community Edition
Docker EE : Enterprise Edition

0.X -> 1.X(1.13.X) -> 17.04 -> 20.10

## Docker Engine 설치

> https://docs.docker.com/engine/install/ubuntu/

``` bash
sudo apt update
```

``` bash
sudo apt install ca-certificates curl gnupg lsb-release
```

``` bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

``` bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

``` bash
sudo apt update
```

``` bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

- docker-ce: Docker Engine
- docker-ce-cli: docker command
- containerd.io: Container Runtime Interface
- docker-compose-plugin: Docker Compose


``` bash
sudo usermod -aG docker vagrant
```


## 컨테이너 이미지

(registry/)repository/name:tag

docker.io/library/hello-world:latest

## Lifestyle

- create -> start -> (pause) -> (unpause) -> (kill) -> stop -> rm run ---------->

> application이 종료
> 컨테이너도 종료(stop)

- -i: STDIN 유지
- -t: Terminal 할당
- -d: Detach

> -it 옵션은 Shell을 실행하는 이미지에서 사용: centos, ubuntu ... -d 옵션 application이 계속적으로 실행되어햐 할 때: httpd ...

리눅스 배포판 이름으로된 이미지

- ubuntu
- centos
- rocky
- debian
- alpine
- busybox
- amazonlinux
- oraclelinux
- ... -> Base Image