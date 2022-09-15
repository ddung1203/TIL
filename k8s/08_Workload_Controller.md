# Workload Resource - Controller

## Replication Controller

`myweb-rc.yaml`
``` yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: myweb-rc
spec:
  replicas: 3
  selector:
    app: web
# Pod Configure
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
          ports:
            - containerPort: 8080
              protocol: TCP
```

``` bash
kubectl create -f myweb-rc.yaml
```

### RC 스케일링

명령형 커맨드
``` bash
kubectl scale rc myweb-rc --replicas=5
```

명령형 오브젝트 구성
``` bash
kubectl replace -f myweb-rc.yaml
```

``` bash
kubectl patch -f myweb-rc.yaml -p '{"spec": {"replicas": 3}}'
kubectl patch rc myweb-rc.yaml --patch-file replicas.json
```

`replicas.json`
``` json
{"spec": {"replicas": 3}}
```

``` bash
kubectl edit -f myweb-rc.yaml
kubectl edit rc myweb-rc
kubectl edit rc/myweb-rc
```

선언형 오브젝트 구성
``` bash
kubectl apply -f myweb-rc.yaml
```

## ReplicaSets

ReplicationController -> ReplicaSets

``` yaml
apiVersion: apps/v1
kind: ReplicaSets
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
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-rs-set
spec:
  replicas: 3
  selector:
    matchExpressions:
      - key: app
        operator: In
        values: 
          - web
      - key: env
        operator: Exists
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

## DaemonSets

노드마다 하나씩 파드 배치
``` yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: myweb-ds
spec:
  selector:
    matchExpressions:
      - key: app
        operator: In
        values:
          - myweb
      - key: env
        operator: Exists
  template:
    metadata:
      labels:
        app: myweb
        env: dev
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
          ports:
            - containerPort: 8080
              protocol: TCP
							apiVersion: apps/v1
```

## Jobs

시작 -> 완료

``` yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: mypi
spec:
  template:
    spec:
      containers:
        - image: perl  
          name: mypi
          command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: OnFailure
```

### 잡 컨트롤러의 레이블
파드 템플릿의 레이블/잡 컨트롤러의 레이블 셀렉터는 지정하지 않는다.
-> 잘못된 매핑으로 기존의 파드를 종료하지 않게 하기 위함

### 파드의 종료 및 삭제

`job.spec.activeDeadlineSeconds` : 애플리케이션이 실행될 수 있는 시간 지정
`job.spec.ttlSecondsAfterFinished` : 컨트롤러 및 파드 삭제

``` yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: mypi
spec:
  template:
    spec:
      containers:
        - image: perl
          name: mypi
          command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: OnFailure
  ttlSecondsAfterFinished: 10
```

### 작업의 병렬 처리
`job.spec.completions` : 완료 횟수
`job.spec.parallelism` : 병렬 개수

``` yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: mypi-para
spec:
  completions: 3
  parallelism: 3
  template:
    spec:
      containers:
        - image: perl
          name: mypi
          command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(1500)"]
      restartPolicy: OnFailure
```

## CronJob

> kubectl explain cj --api-version=batch/v1beta1

``` yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: sleep-cj
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: sleep
              image: ubuntu
              command: ["sleep", "80"]
          restartPolicy: OnFailure
  #concurrencyPolicy: ( Allow | Forbid | Replace )
```

`cj.spec.concurrencyPolicy`
- Allow : 동시 작업 가능
- Forbid : 동시 작업 금지(이전 작업이 계속 실행 됨)
- Replace : 교체(이전 작업은 종료되고 새로운 작업 실행)