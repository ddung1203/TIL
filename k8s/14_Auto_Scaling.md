# Auto Scaling

## Resource Request & Limit

요청 : Request
제한 : Limit

요청 <= 제한

QoS(서비스 품질) Class:
1. BestEffort : 가장 나쁨
2. Burstable
3. Guaranteed : 가장 좋음

- 요청/제한 설정되어 있지 않으면 : BestEffort
- 요청 < 제한 : Bustable
- 요청 = 제한 : Guartanteed

`pod.spec.containers.resources`
- resuests
  - cpu
  - memory
- limits
  - cpu
  - memory

CPU 요청 & 제한 : milicore
ex) 1500m : 1.5개
ex) 1000m : 1개

Memory 요청 & 제한 : M, G, T, Mi, Gi, Ti

`myweb-reqlim.yaml`

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-reqlim
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb
      resources:
        requests:
          cpu: 200m
          memory: 200M
        limits:
          cpu: 200m
          memory: 200M
```

노드별 CPU/Memory 사용량 확인

``` bash
kubectl top nodes
```

파드별 CPU/Memory 사용량 확인
``` bash
kubectl top pods
kubectl top pods -A
```

리소스 모니터링(인프라 모니터링) Heapster:
-> metric=server : 실시간
-> cpu/memory 모니터링
-> prometheus : 실시간/이전 cpu/memory/network/disk 모니터링

노드별 요청/제한 양 확인

``` bash
kubectl describe nodes node1
```

실행 할 수 없는 리소스
`myweb-big.yaml`

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-reqlim
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb
      resources:
        limits:
          cpu: 3000m
          memory: 4000M
```

## HPA : Horizontal Pod AutoScaler

AutoScaling
- Pod
  - HPA
  - VPA : Vertical Pod Autoscaler
- Node
  - ClusterAutoScaler

HPA : Deployment, ReplicaSet, StatefulSet의 복제본 개수를 조정

> 스케일 아웃: 180초
> 스케인 인: 300초

`myweb-deploy.yaml`

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myweb-deploy
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb:alpine
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 200m
            limits:
              cpu: 200m
```

HPA를 위해 최소 request는 설정되야 함

`myweb-hpa.yaml`

``` yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: myweb-hpa
spec:
  minReplcias: 1
  maxReplicas: 10
  targerCPUUtilizationPercentage: 50
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myweb-deploy
```

부하
``` bash
kubectl exec <POD> -- sha256sum /dev/zero
```

`myweb-hpa-v2beta2.yaml`
``` yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: myweb-hpa
spec:
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          avarageUtilization: 50
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myweb-deploy
```