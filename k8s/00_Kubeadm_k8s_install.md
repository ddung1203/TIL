# k8s 설치

- **Kubeadm**
- Kubespray (Kubeadm + Ansible)
- Kops
- Docker Desktop - Kubernetes
- minikube

## Kubeadm

kubeadm은 Kubernetes를 설치하기 위한 도구일 뿐 Kubernetes가 아니다.


### 컨테이너 런타임 설치

Pod에서 컨테이너를 실행하기 위해, Kubernetes는 컨테이너 런타임을 사용한다.

|런타임|유닉스 도메인 소켓 경로|
|---|---|
|containerd|unix:///var/run/containerd/containerd.sock|
|CRI-O|unix:///var/run/crio/crio.sock|
|도커 엔진 (cri-dockerd 사용)|unix:///var/run/cri-dockerd.sock|

**containerd Install**

https://github.com/containerd/containerd/blob/main/docs/getting-started.md


```bash
wget https://github.com/containerd/containerd/releases/download/v1.7.12/containerd-1.7.12-linux-amd64.tar.gz
sudo tar Cxzvf /usr/local containerd-1.7.12-linux-amd64.tar.gz

wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
sudo mkdir -p /usr/local/lib/systemd/system
sudo mv containerd.service /usr/local/lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now containerd

wget https://github.com/opencontainers/runc/releases/download/v1.1.11/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc

wget https://github.com/containernetworking/plugins/releases/download/v1.4.0/cni-plugins-linux-amd64-v1.4.0.tgz
sudo mkdir -p /opt/cni/bin
sudo tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.4.0.tgz
```

1.22.8

kubeadm, kubectl, kubelet 도구 설치
``` bash
sudo apt-get update
```

``` bash
sudo apt-get install -y apt-transport-https ca-certificates curl
```

``` bash
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
```

``` bash
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

``` bash
sudo apt-get update
```

``` bash
apt-cache madison kubeadm | grep 1.22.8
apt-cache madison kubelet | grep 1.22.8
apt-cache madison kubectl | grep 1.22.8
```

``` bash
sudo apt-get install kubeadm=1.22.8-00 kubelet=1.22.8-00 kubectl=1.22.8-00 -y
```

``` bash
sudo apt-mark hold kubelet kubeadm kubectl
```

### cgroup driver 오류

> 컨테이너 런타임과 kubelet의 cgroup 드라이버를 일치시켜야 하며, 그렇지 않으면 kubelet 프로세스에 오류가 발생한다.

``` 
sudo docker info | grep 'Cgroup Driver'
 
 Cgroup Driver: cgroupfs
```

`/etc/docker/daemon.json`
```
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
```

``` bash
sudo systemctl restart docker
```

```
sudo docker info | grep 'Cgroup Driver'

 Cgroup Driver: systemd
```

``` bash
sudo systemctl daemon-reload && sudo systemctl restart kubelet
```

> systemd란, Linux 배포판에서 유닉스 시스템 V나 BSD init 시스템 대신 사용자 공간을 부트스트래핑하고 최종적으로 모든 프로세스들을 관리하는 init 시스템이다.
> 즉, PID가 1인 프로세스로 부팅부터 서비스 관리, 로그 관리 등 시스템 전반적인 영역을 관리한다.

IPv4를 포워딩하여 iptables가 브릿지된 트래픽을 보게 하기

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 필요한 sysctl 파라미터를 설정하면, 재부팅 후에도 값이 유지된다.
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# 재부팅하지 않고 sysctl 파라미터 적용하기
sudo sysctl --system
```

containerd를 CRI 런타임으로 사용하기 위한 설정

```bash
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml

sudo systemctl restart containerd
```


### k8s 클러스터 생성
`kubeadm init` 실패 시
``` bash
sudo kubeadm reset
```

``` bash
sudo kubeadm init --control-plane-endpoint 192.168.56.100 --pod-network-cidr 172.16.0.0/16 --apiserver-advertise-address 192.168.56.100
```

> ```bash
> [preflight] Running pre-flight checks
> error execution phase preflight: [preflight] Some fatal errors occurred:
>         [ERROR CRI]: container runtime is not running: output: time="2024-01-14T03:13:39Z" level=fatal msg="validate service connection: validate CRI v1 runtime API for endpoint \"unix:///var/run/containerd/containerd.sock\": rpc error: code = Unimplemented desc = unknown service runtime.v1.RuntimeService"
> , error: exit status 1
> [preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...`
> To see the stack trace of this error execute with --v=5 or higher
> ```
> 
> container runtime을 설치 하였음에도 불구하고 상기와 같이 에러가 나온다면, 다음 링크를 참고한다.
> 
> https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd
> 
> containerd를 패키지 매니저를 통해 설치했다면, CRI integration plugin이 기본값으로 disabled 되어있다. 따라서 `etc/containerd/config.toml` 파일을 삭제하거나, 예외처리를 한 후 `containerd`를 restart 한다.

> 기본적인 설정부터 확인하자. VirtualBox 내 DHCP 서버의 설정 중 최저 서버 주소와 최고 서버 주소를 기본값으로 사용을 했는데, 이로 인한 문제로 오랜 시간 디버깅을 하였다. 문제 발생 시 항상 low level부터 검증하는 시각을 가지자.
> 
> `$ sudo kubeadm join 192.168.56.100:6443 --token 959tyd.c25osmm68aoivcy3 --discovery-token-ca-cert-hash sha256:44b9795ea70f4682d6da7c4f3201cdb8cb5512664066a57dc684d79bf7640ba6 --v=5`
> [preflight] Running pre-flight checks
> I0114 11:25:06.561804    4363 join.go:529] [preflight] Discovering cluster-info
> I0114 11:25:06.562571    4363 token.go:80] [discovery] Created cluster-info discovery client, requesting info from "192.168.56.100:6443"
> I0114 11:25:06.566754    4363 token.go:217] [discovery] Failed to request cluster-info, will try again: Get "https://192.168.56.100:6443/api/v1/namespaces/kube-public/configmaps/cluster-info?timeout=10s": dial tcp 192.168.56.100:6443: connect: protocol not available
> I0114 11:25:13.867261    4363 token.go:217] [discovery] Failed to request cluster-info, will try again: Get "https://192.168.56.100:6443/api/v1/namespaces/kube-public/configmaps/cluster-info?timeout=10s": dial tcp 192.168.56.100:6443: connect: protocol not available

``` bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

``` bash
kubectl get nodes

NAME     STATUS     ROLES                  AGE   VERSION
kubeadm-node1   **NotReady**   control-plane,master   14m   v1.22.8
```

NotReady가 나오는 이유는 아직 CNI 설치를 하지 않았기 때문이다.

### Calico Network Add-on

https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises


``` bash
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.1/manifests/tigera-operator.yaml
```

``` bash
curl https://raw.githubusercontent.com/projectcalico/calico/v3.25.1/manifests/custom-resources.yaml -O
```

`custom-resources.yaml`
```
...
      cidr: 172.16.0.0/16
...
```

``` bash
kubectl create -f custom-resources.yaml
```

### 클러스터 상태 확인
``` bash
kubectl get pods -A   

NAMESPACE          NAME                                       ...
calico-apiserver   calico-apiserver-c9565f67b-2p29k           ...
calico-apiserver   calico-apiserver-c9565f67b-slthl           ...
calico-system      calico-kube-controllers-5d74cd74bc-sg7dn   ...
calico-system      calico-node-tgxks                          ...
calico-system      calico-typha-7447fdc844-txrdb              ...
kube-system        coredns-78fcd69978-4ztkq                   ...
kube-system        coredns-78fcd69978-jpwxx                   ...
kube-system        etcd-docker                                ...
kube-system        kube-apiserver-docker                      ...
kube-system        kube-controller-manager-docker             ...
kube-system        kube-proxy-5st98                           ...
kube-system        kube-scheduler-docker                      ...
tigera-operator    tigera-operator-7cf4df8fc7-kx87z           ...
```

``` bash
kubectl get nodes

NAME     STATUS   ROLES                  AGE   VERSION
kubeadm-node1   **Ready**    control-plane,master   30m   v1.22.8
```

``` bash
kubectl taint node docker node-role.kubernetes.io/master-
```

## Worker Node 추가
### Docker 설치
``` bash
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

```
docker info | grep 'Cgroup Driver'
 
 Cgroup Driver: cgroupfs
```

`/etc/docker/daemon.json`

```
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
```

``` bash
sudo systemctl restart docker
```

```
docker info | grep 'Cgroup Driver'

 Cgroup Driver: systemd
```

``` bash
sudo systemctl daemon-reload && sudo systemctl restart kubelet
```

``` bash
sudo usermod -aG docker vagrant
```

재접속

### kubeadm, kubelet, kubectl 설치

``` bash
sudo apt-get install -y apt-transport-https ca-certificates curl
```

``` bash
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
```

``` bash
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

``` bash
sudo apt-get update
```

``` bash
sudo apt-get install kubeadm=1.22.8-00 kubelet=1.22.8-00 kubectl=1.22.8-00 -y
```

### k8s Cluster Join

Token 조회
``` bash
vagrant@kubeadm-node1:~$ kubeadm token list
TOKEN                     TTL         EXPIRES                USAGES                   DESCRIPTION                                                EXTRA GROUPS
zyr0ab.1t7vvmfslwldv5x2   23h         2023-04-18T01:06:34Z   authentication,signing   The default bootstrap token generated by 'kubeadm init'.   system:bootstrappers:kubeadm:default-node-token
```

kubeadm-node1에서 `kubeadm init` 명령어를 실행할 때 출력된 token과 discovery hash 값을 기억한다.
``` bash
vagrant@kubeadm-node1:~$ sudo kubeadm init --control-plane-endpoint 192.168.56.100 --pod-network-cidr 172.16.0.0/16 --apiserver-advertise-address 192.168.56.100

...

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of control-plane nodes by copying certificate authorities
and service account keys on each node and then running the following as root:

  kubeadm join 192.168.56.100:6443 --token nvdgs2.hmscd4zkwlzotisf \
        --discovery-token-ca-cert-hash sha256:1440245ef119cea97016c376e72585830d19c0df15efe452d63133ba863a1626 \
        --control-plane

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.56.100:6443 --token nvdgs2.hmscd4zkwlzotisf \
        --discovery-token-ca-cert-hash sha256:1440245ef119cea97016c376e72585830d19c0df15efe452d63133ba863a1626
```

Token의 경우 24시간 후에 만료된다. 만약 Token이 만료된 후 Node를 클러스터에 Join하는 경우, 새 토큰을 발급받는다.

``` bash
kubeadm token create
```

또한, `--discovery-token-ca-cert-hash`의 값이 없는 경우 하기와 같이 작성한다.

``` bash
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | \
   openssl dgst -sha256 -hex | sed 's/^.* //'
```


``` bash
sudo kubeadm join --token zyr0ab.1t7vvmfslwldv5x2 192.168.56.100:6443 \
--discovery-token-ca-cert-hash sha256:f3ad7db9786019132771d1e3c1fd9c6b0031689698b12dac4a9812614ed397ff
```

> 현재 kubeadm에서 지원하는 Docker 버전은 20.10까지이므로 23.0.3 버전은 지원되지 않는다.
> 따라서, kubeadm을 사용하여 클러스터를 구성하려면 Docker를 다운그레이드해야 한다.

``` bash
vagrant@kubeadm-node2:~$ sudo kubeadm join --token zyr0ab.1t7vvmfslwldv5x2 192.168.56.100:6443 --discovery-token-ca-cert-hash sha256:f3ad7db9786019132771d1e3c1fd9c6b0031689698b12dac4a9812614ed397ff
[preflight] Running pre-flight checks
        [WARNING SystemVerification]: this Docker version is not on the list of validated versions: 23.0.3. Latest validated version: 20.10
error execution phase preflight: couldn't validate the identity of the API Server: Get "https://192.168.56.100:6443/api/v1/namespaces/kube-public/configmaps/cluster-info?timeout=10s": x509: certificate is valid for 10.96.0.1, 10.0.2.15, not 192.168.56.100
To see the stack trace of this error execute with --v=5 or higher
```

Docker 20.10 다운그레이드

``` bash
sudo apt-get install docker-ce=5:20.10.8~3-0~ubuntu-focal docker-ce-cli=5:20.10.8~3-0~ubuntu-focal containerd.io
```