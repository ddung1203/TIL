# Kubespray

> https://kubernetes.io/ko/docs/setup/production-environment/tools/kubespray/
> https://kubespray.io/#/
> https://github.com/kubernetes-sigs/kubespray


Control Plane 1
Work Node 3(1 Control Plan + 2 Worker Node)

Control Plan : CPU : 2, Memory : 4GBUbuntu 20.04|
Worker Node : CPU : 2, Memory : 3GB


## 1. SSH 키 생성 및 복사
```
ssh-keygen
```

```
ssh-copy-id vagrant@192.168.100.100
ssh-copy-id vagrant@192.168.100.101
ssh-copy-id vagrant@192.168.100.102
```

## 2. kubespray 소스 다운로드
```
cd ~
```

```
git clone -b v2.18.1 https://github.com/kubernetes-sigs/kubespray.git
```

```
cd kubespray
```

## 3. ansible, netaddr, jinja 등 패키지 설치
```
sudo apt update
sudo apt install python3-pip -y
```

```
sudo pip3 install -r requirements.txt
```

## 4. 인벤토리 구성
```
cp -rpf inventory/sample/ inventory/mycluster
```

`inventory/mycluster/inventory.ini`
```ini
[all]
node1 ansible_host=192.168.100.100 ip=192.168.100.100
node2 ansible_host=192.168.100.101 ip=192.168.100.101
node3 ansible_host=192.168.100.102 ip=192.168.100.102

[kube_control_plane]
node1

[etcd]
node1

[kube_node]
node1
node2
node3

[calico_rr]

[k8s_cluster:children]
kube_control_plane
kube_node
calico_rr
```

## 5. 변수 설정
`inventory/mycluster/group_vars`


## 6. 플레이북 실행
```
ansible all -m ping -i inventory/mycluster/inventory.ini
```

```
ansible-playbook -i inventory/mycluster/inventory.ini cluster.yml -b 
```

## 7. 검증

```
mkdir ~/.kube
sudo cp /etc/kubernetes/admin.conf ~/.kube/config
sudo chown vagrant:vagrant ~/.kube/config
```

```
kubectl get nodes
```

```
kubectl get pods -A
```

## Offline Install

Kubespray를 사용하여 Kubernetes 클러스터를 오프라인 환경에서 구축하는 방법

> 오프라인 환경에서는 필요한 패키지 및 도구를 사전에 다운로드하고 전달하는 것이 중요하다.

### Pre requirements

Bastion을 제외한 서버는 외부 접근이 불가능하며, Bastion Host를 통해서 master 및 node에 접근이 가능하다.

|Host|IP|Spec|OS|
|------|---|---|---|
|bastion|192.168.100.109, Public IP|CPU 1, MEM 1|Ubuntu 20.04|
|master|192.168.100.110|CPU 4, MEM 6|Ubuntu 20.04|
|node1|192.168.100.111|CPU 2, MEM 4|Ubuntu 20.04|
|node2|192.168.100.112|CPU 2, MEM 4|Ubuntu 20.04|
|node3|192.168.100.113|CPU 2, MEM 4|Ubuntu 20.04|

### Local Mirror 구축

```bash
sudo apt install apt-mirror apache2 -y
```

`/etc/apt/mirror.list`
```
deb http://mirror.kakao.com/ubuntu focal main restricted
deb http://mirror.kakao.com/ubuntu focal-updates main restricted
deb http://mirror.kakao.com/ubuntu focal universe
deb http://mirror.kakao.com/ubuntu focal-updates universe
deb http://mirror.kakao.com/ubuntu focal multiverse
deb http://mirror.kakao.com/ubuntu focal-updates multiverse
deb http://mirror.kakao.com/ubuntu focal-backports main restricted universe multiverse
deb http://mirror.kakao.com/ubuntu focal-security main restricted
deb http://mirror.kakao.com/ubuntu focal-security universe
deb http://mirror.kakao.com/ubuntu focal-security multiverse
```

```bash
sudo apt-mirror
```

```bash
ln -s /var/spool/apt-mirror/mirror/kr.archive.ubuntu.com/ubuntu/ /var/www/html/ubuntu
service apache2 restart
```

`/etc/apt/sources.list`
```
deb http://192.168.100.109/ubuntu focal main restricted
deb http://192.168.100.109/ubuntu focal-updates main restricted
deb http://192.168.100.109/ubuntu focal universe
deb http://192.168.100.109/ubuntu focal-updates universe
deb http://192.168.100.109/ubuntu focal multiverse
deb http://192.168.100.109/ubuntu focal-updates multiverse
deb http://192.168.100.109/ubuntu focal-backports main restricted universe multiverse
deb http://192.168.100.109/ubuntu focal-security main restricted
deb http://192.168.100.109/ubuntu focal-security universe
deb http://192.168.100.109/ubuntu focal-security multiverse
deb http://192.168.100.109/docker focal stable
```

