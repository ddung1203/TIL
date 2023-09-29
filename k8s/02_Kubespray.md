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

Bastion 내에 구축을 진행한다.

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
deb https://download.docker.com/linux/ubuntu focal stable
```

```bash
sudo apt-mirror
```

> 현재 cnf 파일을 제대로 가져오지 못하는 이슈가 있어, apt-mirror 파일만 하기와 같이 변경하도록 한다.
> 
> [apt-mirror 참고](./apt-mirror)

```bash
sudo ln -s /var/spool/apt-mirror/mirror/mirror.kakao.com/ubuntu/ /var/www/html/ubuntu
sudo ln -s /var/spool/apt-mirror/mirror/download.docker.com/linux/ubuntu/ /var/www/html/docker-ce
service apache2 restart
```

Master 및 Node들의 `sources.list`를 하기와 같이 변경 후 `apt update`로 테스트 성공을 확인할 수 있다.

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
deb http://192.168.100.109/docker-ce focal stable
```

> apt 업데이트 시 `NO_PUBKEY` 에러가 발생한다. 해당 저장소의 공개키가 시스템에 등록되어 있지 않아 발생하는 에러이며, Docker 저장소의 공개키를 시스템에 추가하여 이 문제를 해결할 수 있다.
> 
> ```bash
> sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 7EA0A9C3F273FCD8
> ```
> 
> ```bash
> vagrant@master:~$ sudo apt update
> Hit:1 http://192.168.100.109/ubuntu focal InRelease
> Hit:2 http://192.168.100.109/ubuntu focal-updates InRelease
> Hit:3 http://192.168.100.109/ubuntu focal-backports InRelease
> Hit:4 http://192.168.100.109/ubuntu focal-security InRelease
> Hit:5 http://192.168.100.109/docker-ce/linux/ubuntu focal InRelease
> Reading package lists... Done
> Building dependency tree       
> Reading state information... Done
> 11 packages can be upgraded. Run 'apt list --upgradable' to see them.
> ```

### Private Docker Registry 구축

```bash
docker run -d -p 5000:5000 --restart=always --name docker-registry \
  -v /home/vagrant/certs:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/server.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/server.key \
  registry
```

```bash
docker pull hello-world
docker tag hello-world localhost:5000/hello-world
```

```bash
docker push localhost:5000/hello-world

curl -X GET https://localhost:5000/v2/_catalog --insecure
curl -X GET https://localhost:5000/v2/hello-world/tags/list --insecure
```

#### Remote Host

테스트 서버 환경이기에, hosts 파일과 사설 인증서를 통해 진행하겠다.

`/etc/hosts`
```
192.168.100.109 bastion
```
