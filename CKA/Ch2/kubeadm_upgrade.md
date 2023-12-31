# Kubeadm upgrade

## 문제

`Cluster Upgrade`
```
■ 작업 클러스터: hk8s
마스터 노드의 모든 Kubernetes control plane 및 node 구성 요소를 버전 1.27.6으로 업그레이드합니다.
master 노드를 업그레이드하기 전에 drain 하고 업그레이드 후에 uncordon해야 합니다.
```

https://kubernetes.io/ko/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

### 컨트롤 플레인 노드 업그레이드

```bash
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm=1.27.6-00 && \
sudo apt-mark hold kubeadm
```

```bash
sudo kubeadm version
sudo kubeadm upgrade plan v1.27.6
```

```bash
sudo kubeadm upgrade apply v1.27.6
```

```bash
kubectl drain hk8s-master --ignore-daemonsets
```

```bash
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet=1.27.6-00 kubectl=1.27.6-00 && \
sudo apt-mark hold kubelet kubectl
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

```bash
kubectl uncordon hk8s-master
```


### 워커 노드 업그레이드

hk8s-worker1, hk8s-worker2 반복

```bash
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm=1.27.6-00 && \
sudo apt-mark hold kubeadm
```

```bash
kubectl drain hk8s-worker1 --ignore-daemonsets
```

```bash
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet=1.27.6-00 kubectl=1.27.6-00 && \
sudo apt-mark hold kubelet kubectl
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

```bash
kubectl uncordon hk8s-worker1
```