# Kubespray

> https://kubernetes.io/ko/docs/setup/production-environment/tools/kubespray/
> https://kubespray.io/#/
> https://github.com/kubernetes-sigs/kubespray


Control Plane 1
Work Node 3(1 Control Plan + 2 Worker Node)

Control Plan : CPU : 2, Memory : 4GB
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

WIP