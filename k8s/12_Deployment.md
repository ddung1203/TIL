# Deployments

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myweb-deploy
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
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb:v1
          ports:
            - containerPort: 8080
```

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-lb
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

``` bash
kubectl rollout status deploy myweb-deploy
```

``` bash
kubectl rollout history deploy myweb-deploy
```

``` bash
kubectl set image deployments myweb-deploy myweb=ghcr.io/c1t1d0s7/go-myweb:v2.0 --record
```

`--record` : 명령을 히스토리에 저장

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myweb-deploy
  annotations:
    kubernetes.io/change-cause: "Change Go Myweb version from 3 to 4"
    ...
```

``` bash
kubectl apply -f myweb-deploy.yaml
```

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myweb-deploy
  annotations:
    kubernetes.io/change-cause: "Change Go Myweb version from 3 to 4"
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  replicas: 3
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
          image: ghcr.io/c1t1d0s7/go-myweb:v4.0
          ports:
            - containerPort: 8080
```

## Deployment Update
Deployment Update 방식

1. Rolling Update
2. Recreate
3. Blue/Green
4. Canary

### 1. Rolling Update

![Rolling_Update](./img/12_1.png)

Rolling Update는 별다른 설정을 하지 않을 시 기본적으로 적용되는 방식이다.
V1을 V2로 업데이트 할 때, V2를 하나 생성한 뒤 V1을 삭제하는 방식으로 Pod를 하나씩 점진적으로 교체해나가는 방법이다.
이 방법은 무중단 배포가 가능하다는 장점이 있지만, V1과 V2의 Pod가 공존하는 순간이 있다는 단점이 있다.

### 2. Recreate

![Recreate](./img/12_2.png)

Recreate는 재생성이다.
기존의 Pod를 모두 삭제한 뒤, 새로운 버전의 Pod를 선언한 개수만큼 생성해주는 방식이다.
단점으로는 순간적으로 Pod가 존재하지 않는 순간이 있다는 단점이 있다.

### 3. Blue/Green

![Blue/Green](./img/12_3.png)

Blue/Green 배포는 기존 버전의 Pod를 유지한채로 새로운 버전의 Pod를 선언한 개수만큼 생성하고 Service가 트래픽을 전달하는 대상을 교체한 뒤 기존의 Pod를 삭제하는 방식이다.
이 방법은 무준단 배포가 가능하고, 기존에 Rolling Update가 가지고 있던 V1, V2가 공존하는 순간이 있는 문제를 해결할 수 있지만, 배포시 자원을 2배로 사용한다는 단점이 있다.

### 4. Canary

![Canary](./img/12_4.png)

Canary는 테스트라는 특징을 가지고 있다.
구버전과 신버전 Pod를 모두 구성한 뒤, 트래픽의 양을 조절하여 테스트를 진행한 다음 교체하는 방식이다.