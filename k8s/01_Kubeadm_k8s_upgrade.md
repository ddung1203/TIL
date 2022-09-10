# k8s 클러스터 업그레이드

> Ubuntu 패키지 저장소 변경 sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list sudo apt update

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

Control Plane

```
sudo apt-mark unhold kubeadm
```

```
sudo apt update
```

```
sudo apt upgrade kubeadm=1.22.9-00 -y
```

```
kubeadm version
```

```
sudo apt-mark hold kubeadm
```

```
sudo kubeadm upgrade plan
```

```
sudo kubeadm upgrade apply v1.22.9
```

```
sudo apt-mark unhold kubelet kubectl
```

```
sudo apt upgrade kubectl=1.22.9-00 kubelet=1.22.9-00 -y
```

```
sudo apt-mark hold kubelet kubectl
```

```
kubelet --version
kubectl version
```

> drain 작업

```
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

> uncordon 작업

```
systemctl status kubelet
```

Work Node

```
sudo apt-mark unhold kubeadm
```

```
sudo apt update
```

```
sudo apt upgrade kubeadm=1.22.9-00 -y
```

```
kubeadm version
```

```
sudo apt-mark hold kubeadm
```

```
sudo kubeadm upgrade node
```

> drain 작업

```
sudo apt-mark unhold kubelet kubectl
```

```
sudo apt upgrade kubectl=1.22.9-00 kubelet=1.22.9-00 -y
```

```
sudo apt-mark hold kubelet kubectl
```

```
kubelet --version
kubectl version
```

```
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

> uncordon 작업

