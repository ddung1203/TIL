# k8s 설치

- **Kubeadm**
- Kubespray (Kubeadm + Ansible)
- Kops
- Docker Desktop - Kubernetes
- minikube

## Kubeadm

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

### k8s 클러스터 생성
`kubeadm init` 실패 시
``` bash
sudo kubeadm reset
```

``` bash
sudo kubeadm init --control-plane-endpoint 192.168.100.100 --pod-network-cidr 172.16.0.0/16 --apiserver-advertise-address 192.168.100.100
```

``` bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

``` bash
kubectl get nodes

NAME     STATUS     ROLES                  AGE   VERSION
docker   **NotReady**   control-plane,master   14m   v1.22.8
```

### Calico Network Add-on
``` bash
kubectl create -f https://projectcalico.docs.tigera.io/manifests/tigera-operator.yaml
```

``` bash
curl https://projectcalico.docs.tigera.io/manifests/custom-resources.yaml -O
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
docker   **Ready**    control-plane,master   30m   v1.22.8
```

``` bash
kubectl taint node docker node-role.kubernetes.io/master-
```

## Worker Node 추가
### Docker 설치
``` bash
sudo apt-get update
```

``` bash
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
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
sudo apt-get update
```

``` bash
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

``` bash
sudo kubeadm join --token 69bz9a.jd5a3qmzlhb66iua 192.168.100.100:6443 \
--discovery-token-ca-cert-hash sha256:73f2901d915c6fe5a5a37a6c1c4c1aa73e36da2c3619e36c16d2387a856bc840
```