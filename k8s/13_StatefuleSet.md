# StatefuleSet

Deployment와 다르게 StatefulSet은 각 Pod의 독자성을 유지한다. 이 Pod들은 동일한 spec으로 생성되지만, 서로 교체는 불가능하다.
즉, 각각은 재 스케쥴링 간에도 지속적으로 유지되는 식별자를 가진다.
Storage Volume을 사용해서 워크로드에 지속성을 제공하려는 경우, 솔루션의 일부로 StatefulSet을 사용할 수 있다. StatefulSet의 개별 Pod는 장애에 취약하지만, Persistent Pod 식별자는 기존 Volume을 실패한 Volume을 대체하는 새 Pod에 더 쉽게 일치시킬 수 있다.

- 파드들의 순서 및 고유성을 보장한다. (배포, 업데이트, 스케일링시)
- 재 스케줄링 간에도 지속적으로 유지되는 식별자를 가진다. (네트워크)
- PV를 유지할 수 있다.

## Headless Service

`myweb-svc.yaml`

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

`myweb-svc-headless.yaml`

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-headless
spec:
  type: ClusterIP
  clusterIP: None # <-- Headless Service
  selector:
    app: web
  ports:
    - port: 80
    targetPort: 8080
```

`myweb-rs.yaml`
``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      env: dev
  template:
    metadata:
      labels:
        app: web
        env: dev
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
          ports:
            - containerPort: 8080
              protocol: TCP
```

``` bash
kubectl run nettool -it --image ghcr.io/c1t1d0s7/network-multitool --rm

> host myweb-svc
> host myweb-svc-headless
```

## StatefuleSet

### 예제 1.

`myweb-svc-headless.yaml`

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-headless
spec:
  type: ClusterIP
  clusterIP: None # <-- Headless Service
  selector:
    app: web
  ports:
    - port: 80
    targetPort: 8080
```

`myweb-sts.yaml`

``` yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: myweb-sts
spec:
  replicas: 3
  serviceName: myweb-svc-headless
  selector:
    matchLabels:
      app: web
      env: dev
  template:
    metadata:
      labels:
        app: web
        env: dev
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
          ports:
            - containerPort: 8080
              protocol: TCP
```

``` bash
kubectl run nettool -it --image ghcr.io/c1t1d0s7/network-multitool --rm

> host myweb-svc-headless
> host myweb-sts-0.myweb-svc-headless
> host myweb-sts-1.myweb-svc-headless
> host myweb-sts-2.myweb-svc-headless
```

### 에제 2. PVC 템플릿

`myweb-sts-vol.yaml`

``` yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: myweb-sts-vol
spec:
  replicas: 3
  serviceName: myweb-svc-headless
  selector:
    matchLabels:
      app: web
      env: dev
  template:
    metadata:
      labels:
        app: web
        env: dev
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb:alpine
          ports:
            - containerPort: 8080
              protocol: TCP
          volumeMounts:
            - name: myweb-pvc
              mountPath: /data
  volumeClaimTemplates:
    - metadata:
        name: myweb-pvc
      spec:
        accessMode:
          - ReadWriteOnce
        resources:
          requests:
            storage: 1G
        storageClassName: nfs-client
```