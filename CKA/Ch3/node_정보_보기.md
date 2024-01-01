# Node 정보 보기

## Node Taint, Toleration

- Worker Node에 taint가 설정된 경우 동일 값의 toleration이 있는 Pod만 배치된다.
- toleration이 있는 Pod는 동일한 taint가 있는 node를 포함하여 모든 node에 배치된다.
  - NoSchedule: toleration이 맞지 않으면 배치되지 않음
  - PreferNoSchedule: toleration이 맞지 않으면 배치되지 않으나, 클러스터 리소스가 부족하면 할당
  - NoExecute: toleration이 맞으면 동작중인 pod를 종료

## 문제

`Ready 노드 확인하기`

```
◾ 작업 클러스터 : hk8s
Ready 상태(NoSchedule로 taint된 node는 제외)인 node를 찾아 그 수를 /var/CKA2022/notaint_ready_node에 기록하세요.
```

```bash
ubuntu@console:~/ch03$ kubectl describe node hk8s-master | grep Taint
Taints:             node-role.kubernetes.io/control-plane:NoSchedule
ubuntu@console:~/ch03$ kubectl describe node hk8s-worker1 | grep Taint
Taints:             <none>
ubuntu@console:~/ch03$ kubectl describe node hk8s-worker2 | grep Taint
Taints:             <none>
```

> master에 pod를 배치하기 위해선,
> 
> ```yaml
> apiVersion: v1
> kind: Pod
> metadata:
>   name: nginx
>   labels:
>     env: test
> spec:
>   containers:
>   - name: nginx
>     image: nginx
>     imagePullPolicy: IfNotPresent
>   tolerations:
>   - key: "node-role.kubernetes.io/control-plane"
>     operator: "Equal"
>     effect: "NoSchedule"
> ```