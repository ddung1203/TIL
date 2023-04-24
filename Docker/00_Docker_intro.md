# Docker

## Container란?

- 호스트 OS 상에 논리적인 구획을 만들고 어플리케이션을 작동시키기 위해 필요한 라이브러리나 어플리케이션 등을 하나로 모아 마치 별도의 서버인 것처럼 사용할 수 있게 만든 것이다.
- 개별 SW의 실행 환경을 독립적으로 운용할 수 있도록 다른 실행 환경과의 간섭을 막고 실행의 독립성을 확보해주는 운영체제 수준의 격리 기술을 말한다.
- 호스트 OS의 리소스를 논리적으로 분리시키고, 여러 개의 컨테이너가 공유하며 사용한다.
- 오버헤드가 적기 때문에 가볍고 고속으로 작동하는 것이 특징이다.
- VM가 가장 큰 차이점은 Container는 운영체제를 포함하지 않는다.
- Container 기술을 사용하면 OS나 디렉토리, IP 주소와 같은 시스템 자원을 마치 각 어플리케이션이 점유하고 있는 것처럼 보이게 할 수 있다. 컨테이너는 어플리케이션 실행에 필요한 모듈을 컨테이너를 모을 수 있기 때문에 여러개의 컨테이너를 조합하여 하나의 어플리케이션을 구축하는 MSA와 친화성이 높다.


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

## containerd & CRI-O

초기 Docker를 개발하면서 하나의 완성된 컨테이너 사용자경험을 만드느 것에 집중하다보니 Docker Engine이라는 하나의 패키지에 API, CLI, 네트워크, 스토리지 등 여러 기능들을 모두 담게 되었고, Docker에 의존하고 있던 Kubernetes에서는 Docker 버전이 새로 나올때마다 Kubernetes가 크게 영향을 받는 일들이 생겼다.

그래서 Docker를 중심으로 구글 등 컨테이너 기술에 관심있는 여러 집단들이 한데모여 Open Container Initiative(OCI) 프로젝트를 시작하여 컨테이너에 관한 표준을 정하는 일들을 시작한다. 그래서 Docker에서는 OCI 표준을 준수하는 containerd라는 Container Runtime을 만들고, Kubernetes에서는 OCI 표준을 준수하는 이미지들을 실행할 수 있는 Container Runtime Interface(CRI) 스펙을 v1.5 부터 제공함으로써 Docker 버전과 무관하게 OCI 표준을 준수하기만 하면 어떤 컨테이너 이미지도 Kubernetes에서 실행가능한 환경이 만들어지게 되었다.

한편 Red Hat, Intel, SUSE, Hyper, IBM에서도 OCI 표준에 따라 Kubernetes 전용 Container Runtime을 만들었는데 이것이 CRI-O이다.

containerd와 CRI-O 모두 현재 가장 널리 사용되고 있으며 containerd는 Docker Engine에 기본으로 탑재되어 있어서 지금도 Docker를 사용한다면 내부적으로 사용되는 Container Runtime은 containerd 를 사용하게 된다. 참고로 `docker build` 커맨드로 생성되는 이미지들 역시 OCI Image Spec을 준수하기 때문에 별도의 작업없이 containerd로 실행시킬 수 있다.

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

> `containerd.io` : Cgroup, Namespace를 사용하기 위한 라이브러리

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


## Docker의 특징 - Layer 저장 방식

Docker는 Layer의 개념을 사용하고 유니온 파일 시스템을 이용해 여러 개의 라이브러리를 하나의 파일 시스템으로 사용할 수 있게 해준다. 이미지는 여러개의 읽기 전용 레이어로 구성되고 파일이 추가되거나 수정되면 새로운 레이어가 생성된다.


## Docker의 특징 - namespace, cgroup

Docker는 Container라는 가상의 격리 환경을 만들기 위해 리눅스의 `namespace`와 `cgroup` 이라는 기능을 사용한다.

### namespace

- 프로세스 별로 리소스 사용을 분리한다.
- VM에서는 각 게스트 별로 독립적인 공간을 제공하고 충돌하지 않도록 HW Resource 자체를 가상화한다.
- 하지만 namespace의 경우, HW Resource 자체를 가상화하는 것이 아니라, Linux 내의 자원을 가상화한다.
  - pid name spaces: 프로세스 격리 처리
  - net name spaces: 네트워크 인터페이스
  - ipc name spaces: IPC 자원에 대한 엑세스 관리
  - mnt name spaces: 파일 시스템 포인트 관리
  - uts name spaces: host name 할당


### cgroup

- Control Groups의 약자로 프로세스들이 사용할 수 있는 컴퓨팅 자원들을 제한하고 격리시킬 수 있는 리눅스 커널의 기능이다. namespace와 더불어 Docker Container에서 완벽한 격리 환경을 만드는 데에 쓰이는 중요한 기능이다.
- cgroup를 이용하면 다음 자원들을 제한할 수 있다.
  - memory
  - CPU
  - Network
  - Device
  - I/O

