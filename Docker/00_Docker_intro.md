# Docker

## Container란?

- 호스트 OS 상에 논리적인 구획을 만들고 어플리케이션을 작동시키기 위해 필요한 라이브러리나 어플리케이션 등을 하나로 모아 마치 별도의 서버인 것처럼 사용할 수 있게 만든 것이다.
- 개별 SW의 실행 환경을 독립적으로 운용할 수 있도록 다른 실행 환경과의 간섭을 막고 실행의 독립성을 확보해주는 운영체제 수준의 격리 기술을 말한다.
- 호스트 OS의 리소스를 논리적으로 분리시키고, 여러 개의 컨테이너가 공유하며 사용한다.
- 오버헤드가 적기 때문에 가볍고 고속으로 작동하는 것이 특징이다.
- VM가 가장 큰 차이점은 Container는 운영체제를 포함하지 않는다.
- Container 기술을 사용하면 OS나 디렉토리, IP 주소와 같은 시스템 자원을 마치 각 어플리케이션이 점유하고 있는 것처럼 보이게 할 수 있다. 컨테이너는 어플리케이션 실행에 필요한 모듈을 컨테이너를 모을 수 있기 때문에 여러개의 컨테이너를 조합하여 하나의 어플리케이션을 구축하는 MSA와 친화성이 높다.

Docker는 컨테이너를 주료로 만든 최초의 컨테이너 플랫폼이다. 컨테이너의 격리는 리눅스 네임스페이스(파일, 프로세스, 네트워크 인터페이스, 호스트 이름 등)와 cgroup(CPU, 메모리, 네트워크 대역폭 등)과 같은 커널 기능으로 리눅스 커널 수준에서 수행된다. Docker는 이런 기능들을 사용하기 쉽게 한다.

## Microservices

마이크로서비스는 자율성에 최적화된 아키텍처다. 서비스들 간에 자율성과 느슨한 연결은 마이크로서비스 아키텍처의 중요한 특징이다. 

마이크로서비스는 API를 통해 상호작용하고, 데이터베이스 스키마나 데이터 구조, 데이터의 내부적 표현은 공유하지 않는다. 

모놀로식 애플리케이션에서 기능을 업데이트하거나 버그를 고칠 경우, 일반적으로 전체 애플리케이션을 만들고 배포해야 한다. 라이브러리나 컴포넌트를 조금 변경한 경우에도 변경되지 않는 부분을 포함해서 전체 애플리케이션을 다시 배포해야 한다. 마이크로서비스 기반 아키텍처에서, 각 마이크로서비스는 다른 서비스와 독립적으로 만들어 배포되며, 서비스들 간에 느슨한 결합을 유지할 수 있다. 이는 카탈로그 서비스에서 필요한 다른 변경 사항과 완전히 독립적으로 마이크로서비스에 심각한 버그 수정을 적용할 수 있다. 

독립적인 배포와 데브옵스 수행을 통해 마이크로서비스 아키텍처는 조직의 비즈니스에 영향을 끼치지 않고 중요한 시기에 업데이트를 할 수 있다. 



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

## CRI-O

### Container Runtime Tool을 CRI-O로 사용

``` bash
sudo yum update
```

`/etc/modules-load-d` 경로에 `.conf` 파일명으로 모듈 정보를 등록하면 부팅 시 자동으로 로드
Kubernetes에서container runtime tool로 CRI-O를 사용하기 위한 사전 작업으로 overlay와 br_netfilter 커널 모듈을 로딩해줘야 함
``` bash
# .conf 파일 생성
cat <<EOF | sudo tee /etc/modules-load.d/crio.conf
overlay
br_netfilter
EOF

# 커널 모듈 등록
sudo modprobe overlay
sudo modprobe br_netfilter

# 재기동이 커널모듈이 유지되도록 설정
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sudo sysctl --system
```

### CRI-O 설치

``` bash
export VERSION=1.26
export OS=CentOS_7

sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/devel:kubic:libcontainers:stable.repo

sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo
```

``` bash
sudo yum install cri-o

sudo systemctl daemon-reload
sudo systemctl enable crio --now

systemctl status cri-o
```

## CRI-O와 함께 사용되는 Tool

CRI-O의 경우 오로지 container를 실행하는 역할을 담당한다. 따라서 container 실행 이외의 기능인 image build, clik image registry 생승 등과 같은 부가적인 기능은 수행하지 못한다.

### Podman

Podman 이외에도 Buildah, Skopeo가 있다. 

``` bash
curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo  https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/CentOS_7/devel:kubic:libcontainers:stable.repo

sudo yum install podman
```

``` bash
sudo podman version

sudo podman pull docker.io/ddung1203/realmytrip:latest

sudo podman images

sudo podman run -d -p 3000:3000 --security-opt seccomp=unconfined docker.io/ddung1203/realmytrip:latest

sudo podman ps
```

> Error: container_linux.go:380: starting container process caused: error adding seccomp filter rule for syscall bdflush: requested action matches default action of filter: OCI runtime error
> 이 오류는 seccomp (secure computing) 필터 규칙 설정과 관련된 문제로, 컨테이너 프로세스를 시작할 때 발생한다.
>
> 해결 방법으로는, --security-opt 플래그를 사용하여 seccomp 옵션을 변경할 수 있다.

