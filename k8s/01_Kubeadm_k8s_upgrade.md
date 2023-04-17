# k8s 클러스터 업그레이드

> Ubuntu 패키지 저장소 변경
> sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
> sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
> sudo apt update

> https://kubernetes.io/ko/releases/version-skew-policy/

1. kube-apiserver
2. kube-controller-manager, kube-cloud-controller-manage, kube-scheduler
3. kubelet(Control Plane -> Worker Node)
4. kube-proxy(Control Plane -> Worker Node)

Control Plane(api -> cm, ccm, sched -> let,proxy) --> Work Node(let, proxy)

## kubeadm 업그레이드

1. Control Plane의 kubeadm 업그레이드
2. Control Plane의 kubeadm으로 api, cm, sched 업그레이드
3. Control Plane의 kubelet, kubectl 업그레이드
4. Work Node의 kubeadm 업그레이드
5. Work Node의 kubeadm으로 업그레이드
6. Work Node의 kubelet, kubectl 업그레이드

### Control Plane

**`kubeadm` 업그레이드**

패키지 버전 hold 해제
``` bash
sudo apt-mark unhold kubeadm
```

``` bash
sudo apt update
sudo apt upgrade kubeadm=1.22.9-00 -y
kubeadm version
```

kubeadm 버전 hold
``` bash
sudo apt-mark hold kubeadm
```

``` bash
sudo kubeadm upgrade plan
```

kubeadm upgrade
``` bash
sudo kubeadm upgrade apply v1.22.9
```

**kubectl, kubectl 업그레이드**

``` bash
sudo apt-mark unhold kubelet kubectl
```

``` bash
sudo apt upgrade kubectl=1.22.9-00 kubelet=1.22.9-00 -y
```

``` bash
sudo apt-mark hold kubelet kubectl
```

``` bash
kubelet --version
kubectl version
```

> drain 작업

``` bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

> uncordon 작업

``` bash
systemctl status kubelet
```

### Work Node

**kubeadm 업그레이드**

``` bash
sudo apt-mark unhold kubeadm
```

``` bash
sudo apt update
```

``` bash
sudo apt upgrade kubeadm=1.22.9-00 -y
```

``` bash
kubeadm version
```

``` bash
sudo apt-mark hold kubeadm
```

``` bash
sudo kubeadm upgrade node
```

> drain 작업

``` bash
sudo apt-mark unhold kubelet kubectl
```

``` bash
sudo apt upgrade kubectl=1.22.9-00 kubelet=1.22.9-00 -y
```

``` bash
sudo apt-mark hold kubelet kubectl
```

``` bash
kubelet --version
kubectl version
```

``` bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

> uncordon 작업

