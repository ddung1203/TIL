# Pod Scheduling

## Node Selector

- Worker node에 할당된 label을 이용해 node를 선택

```bash
kubectl label nodes <노드 이름> <키>=<값>

kubectl get nodes -L gpu
```

## 문제

`Pod Scheduling`

```
◾ 작업 클러스터 : k8s
다음의 조건으로 pod를 생성하세요.
Name: eshop-store
Image: nginx
Node selector: disktype=ssd
```

```bash
ubuntu@console:~$ kubectl get nodes -L disktype
NAME          STATUS   ROLES           AGE    VERSION   DISKTYPE
k8s-master    Ready    control-plane   313d   v1.26.0
k8s-worker1   Ready    <none>          313d   v1.26.0   ssd
k8s-worker2   Ready    <none>          313d   v1.26.0   std
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: eshop-store
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disktype: ssd
```