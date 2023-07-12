# Pod Scheduling

https://kubernetes.io/ko/docs/concepts/scheduling-eviction/kube-scheduler/

Kube-scheduler는 Pod나 Controller를 만들었을 때 또는 스케줄링을 할 때 Pod를 어디에 배치시킬 것인지 결정한다.

노드가 여러개 있는 경우 각 노드마다 점수를 매겨서 Pod를 만들었을 때 Pod를 어디에 배치할 것인지 결정하는 것이 kube-scheduler가 하는 역할이다.

## nodeName

https://kubernetes.io/ko/docs/concepts/scheduling-eviction/assign-pod-node/

nodeName의 경우 kube-scheduler의 영향을 받지 않고 특정 노드에 강제로 배치할 수 있다.

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-rs-nn
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      nodeName: node2
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
```

## nodeSelector

필요한 특정 구성이 있는 경우 특정 노드 그룹을 만들어서 배치시킬 수 있다.
노드에 레이블을 적절하게 붙여서 특정 Pod를 원하는 위치에만 배치시킬 수 있다.

노드 레이블 확인

```bash
 vagrant@k8s-node1 > ~/configure > kubectl get nodes --show-labels
```

노드 레이블 node1

```
beta.kubernetes.io/arch=amd64
beta.kubernetes.io/os=linux
kubernetes.io/arch=amd64
kubernetes.io/hostname=node1
kubernetes.io/os=linux
node-role.kubernetes.io/control-plane=
node-role.kubernetes.io/master=
node.kubernetes.io/exclude-from-external-load-balancers=
```

node2

```
beta.kubernetes.io/arch=amd64
beta.kubernetes.io/os=linux
kubernetes.io/arch=amd64
kubernetes.io/hostname=node2
kubernetes.io/os=linux
```

node3

```
beta.kubernetes.io/arch=amd64
beta.kubernetes.io/os=linux
kubernetes.io/arch=amd64
kubernetes.io/hostname=node3
kubernetes.io/os=linux
```

노드에 레이블 부여

```bash
kubectl label node node1 gpu=highend
kubectl label node node2 gpu=midrange
kubectl label node node3 gpu=lowend
```

```bash
 vagrant@k8s-node1 > ~/configure > kubectl get nodes -L gpu
NAME    STATUS   ROLES           AGE   VERSION   GPU
node1   Ready    control-plane   22h   v1.24.6   highend
node2   Ready    <none>          22h   v1.24.6   midrange
node3   Ready    <none>          22h   v1.24.6   lowend
```

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-rs-ns
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      nodeSelector:
        gpu: lowend
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
```

상기 ReplicaSet을 배포 시 모두 node3에 배치된 것을 확인할 수 있다.

node2의 gpu를 lowend로 바꾸고 app이 web인 Pod를 전부 삭제하면 Pod가 재생성되고 다시 스케줄링된다. node2와 node3에 걸쳐 Pod가 배치되는 것을 확인할 수 있다.

## Affinity

nodeSelector의 정책이 경직되어 있다면 Affinity는 선호도를 이용해 가능하면 선호하는 것을 사용하고 아니어도 허용한다. 즉, 스케줄링에 유연성을 둔다.

### Pod 간 Affinity와 anti-Affinity

RS에 의해 만들어진 Web Pod에는 app: web, STS에 의해 만들어진 DB Pod에는 app : db 라는 레이블이 붙어있다.

여기서 web Pod에서 affinity를 설정하는데 셀렉터를 이용해 app : db 레이블이 붙은 Pod와 친하다고 선언한다.
그러면 web Pod 입장에서 항상 DB Pod를 셀렉팅하는 것이기 때문에 web Pod와 DB Pod 쌍은 항상 같은 노드에 배치된다.

물론 여기서 또 worst 상황이 발생할 수도 있다. 모든 web Pod와 DB Pod 쌍이 하나의 노드에만 배치되는 상황이다.

이때 봐야하는 것이 podAntiAffinity이다.
같은 RS에 의해 만들어진 web Pod는 서로를 anti 한다고 선언한다.
서로를 anti 하므로 같은 노드에 배치될 수 없다. 반드시 떨어져 있어야 한다.

즉, 같은 RS에 의해 생성된 web Pod들은 서로를 anti하고 같은 STS에 의해 생성된 DB Pod들도 서로를 anti해야 한다. 그리고 web Pod와 DB Pod는 affinity 해야 한다. 그러면 web Pod, DB Pod 쌍이 하나씩 노드에 배치되며 각 쌍은 서로를 배척하게 된다.

+) 노드의 레이블이 변경되면 Affinity 및 Anti-Affinity 규칙은 이미 실행중인 Pod에 적용되지 않는다.

- affinity
  - pod
  - node
- anti-affinity
  - pod

`myweb-a.yaml`

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-a
spec:
  replicas: 2
  selector:
    matchLabels:
      app: a
  template:
    metadata:
      labels:
        app: a
    spec:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            # 만족하면 좋은 조건
            - weight: 10
              preference:
                matchExpressions:
                  - key: gpu
                    operator: Exists
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            # 꼭 필요한 조건
            - labelSelector:
                matchLabels:
                  app: a # Pod 간 anti
              topologyKey: "kubernetes.io/hostname"
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
```

`myweb-b.yaml`

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-b
spec:
  replicas: 2
  selector:
    matchLabels:
      app: b
  template:
    metadata:
      labels:
        app: b
    spec:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            # 만족하면 좋은 조건
            - weight: 10
              preference:
                matchExpressions:
                  - key: gpu
                    operator: Exists
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            # 꼭 필요한 조건
            - labelSelector:
                matchLabels:
                  app: b # 자기 자신과는 anti
              topologyKey: "kubernetes.io/hostname"
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: a # a라는 label을 가진 Pod와 Affinity
              topologyKey: "kubernetes.io/hostname"
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
```

- `nodeAffinity` : Pod에 대한 노드 어피니티 스케줄링 규칙
- `podAffinity` : Pod 선호도 스케줄링 규칙
- `podAntiAffinity` : Pod의 반선호도 스케줄링 규칙 - 노드 자체의 라벨이 아닌, 노드에서 이미 실행 중인 Pod 라벨을 기반으로 하는 규칙 포함. 다른 Pod와 동일한 노드에 예약되지 않아야 하는 Pod를 구성할 수 있다.

## Cordon & Drain

Cordon : 스케줄링 금지

```bash
kubectl cordon <NODENAME>
```

스케줄링 허용

```bash
kubectl uncordon <NODENAME>
```

Drain : Cordon -> 기존 Pod를 제거

```bash
kubectl drain <NODENAME> --ignore-daemonsets
```

> `--ignore-daemonsets`을 활성화를 통해 데몬셋에 의해 관리되는 Pod들을 해당 노드에서 drain을 강제로 실행한다.
> 패치를 하거나 커널 업데이트를 해야할 때 안전하게 작업하기 위해서 drain을 시켜주는 것이 좋다.

<br>

> `kubectl uncordon <NODENAME>`
> drain하게 되면 자동으로 cordon이 걸리는데, 시스템을 재부팅해도 여전히 cordon 상태이다. 따라서 배치를 시키기 위해서는 반드시 uncordon을 해줘야 한다.

## Taint & Toleration

Control Plane Taint : "node-role.kubernetes.io/master:NoSchedule"

Taint : Pod가 특정 노드에 예약되는 것을 방지
Toleration : Taint 노드에 스케줄링 허용

Taint를 설정한 노드에는 Pod들이 스케줄링 되지 않는다. Taint가 걸린 Node에 Pod들을 스케줄링 하려면 Toleration을 이용해서 지정해 주어야한다.
Taint는 Cordon이나 Drain처럼 모든 Pod가 스케줄링 되지 않게 막는것이 아니고, Toleration을 이용한 특정 Pod들만 실행하게 하고 다른 Pod들은 들어오지 못하게 하는 역할을 한다.

```bash
kubectl taint node node1 node-role.kubernetes.io/master:NoSchedule
```

```
      tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule
```

`myweb-a.yaml`

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-a
spec:
  replicas: 3
  selector:
    matchLabels:
      app: a
  template:
    metadata:
      labels:
        app: a
    spec:
      tolerations:
        - key: nore-role.kubernetes.io/master
          operator: exists
          effect: NoSchedule
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            # 만족하면 좋은 조건
            - weight: 10
              preference:
                matchExpressions:
                  - key: gpu
                    operator: Exists
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            # 꼭 필요한 조건
            - labelSelector:
                matchLabels:
                  app: a
              topologyKey: "kubernetes.io/hostname"
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
```

```bash
kubectl cordon node2
```

```bash
kubectl describe nodes | grep -i taint
```

```bash
kubectl uncordon node2
```

```bash
kubectl describe nodes | grep -i taint
```
