# Pod Scheduling

## nodeName

``` yaml
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

``` bash
kubectl label node node1 gpu=highend
kubectl label node node2 gpu=midrange
kubectl label node node3 gpu=lowend
```

``` bash
kubectl get nodes -L gpu
```

``` yaml
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

## Affinity

- affinity
  - pod
  - node
- anti-affinity
  - pod

`myweb-a.yaml`
``` yaml
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
                  app: a
              topologyKey: "kubernetes.io/hostname"
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
```

`myweb-b.yaml`
``` yaml
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
                  app: b
              topologyKey: "kubernetes.io/hostname"
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: a
              topologyKey: "kubernetes.io/hostname"
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
```

## Cordon & Drain

Cordon : 스케줄링 금지

``` bash
kubectl cordon <NODENAME>
```

스케줄링 허용

``` bash
kubectl uncordon <NODENAME>
```

Drain : Cordon -> 기존 파드를 제거

``` bash
kubectl drain <NODENAME> --ignore-daemonsets
```

> `kubectl uncordon <NODENAME>`

## Taint & Toleration

Control Plane Taint : "node-role.kubernetes.io/master:NoSchedule"

Taint : 특정 노드에 역할을 부여
Toleration : Taint 노드에 스케줄링 허용

``` bash
kubectl taint node node1 node-role.kubernetes.io/master:NoSchedule
```

```
      tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule
```

`myweb-a.yaml`

``` yaml
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

``` bash
kubectl cordon node2
```

``` bash
kubectl describe nodes | grep -i taint
```

``` bash
kubectl uncordon node2
```

``` bash
kubectl describe nodes | grep -i taint
```