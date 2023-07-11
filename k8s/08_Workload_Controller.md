# Workload Resource - Controller

## Replication Controller

`myweb-rc.yaml`

```yaml
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

```bash
kubectl create -f myweb-rc.yaml
```

### RC 스케일링

명령형 커맨드

```bash
kubectl scale rc myweb-rc --replicas=5
```

명령형 오브젝트 구성

```bash
kubectl replace -f myweb-rc.yaml
```

```bash
kubectl patch -f myweb-rc.yaml -p '{"spec": {"replicas": 3}}'
kubectl patch rc myweb-rc.yaml --patch-file replicas.json
```

`replicas.json`

```json
{ "spec": { "replicas": 3 } }
```

```bash
kubectl edit -f myweb-rc.yaml
kubectl edit rc myweb-rc
kubectl edit rc/myweb-rc
```

선언형 오브젝트 구성

```bash
kubectl apply -f myweb-rc.yaml
```

## ReplicaSets

- Pod, ReplicaSet이 어떻게 구성되어야 하는지 정의한다.
  - ReplicaSet: 지정된 수의 Pod Replica가 항상 실행되도록 보장
  - 단독으로 사용 가능하지만, Deployment가 많은 기능을 제공하는 상위 개념이기 때문에 Deployment를 사용하는 것이 권장된다.
- 버전 업데이트 등으로 인해 원하는 정의가 변경되었을 때는 현재 상태에서 원하는 상티로 바뀌도록 변경한다.

ReplicationController -> ReplicaSets

### Controller 역할

1. Auto Healing

- Pod가 실행이 되고 있는 Node에 문제가 생겼을 경우 자동으로 복구하는 기능
- ex) ReplicaSet, DaemonSet

2. Software Update

- Pod를 업데이트하는 기능 / 롤백 기능 또한 존재
- ex) Deployment

3. Auto Scaling

- Pod의 리소스가 부족할 때 Pod를 추가적으로 생성하는 기능

4. Job

- 일시적인 작업을 위해 필요한 순간에만 Pod를 만들었다가 삭제할 수 있는 기능
- ex) Job, CronJob

```yaml
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

```yaml
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

- 모든 노드 또는 특정 label을 가진 노드에 하나씩의 동일한 Pod를 배포
- Worker Node의 Resource Monitoring App이나 Log 수집기를 배포할 때 사용
- 별도의 Replicas를 설정하지 않음
- DaemonSet이 구동중인 Cluster에 노드가 추가되면 해당 노드에도 DaemonSet Pod가 배포
- 삭제된 DatemonSet Pod가 다른 노드로 이동하지 않음

```yaml
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
```

## Jobs

- 하나 이상의 Pod를 지정하고 지정된 수의 Pod를 성공적으로 실행하고 종료될 때까지 Pod의 실행을 재시도
- 백업이나 특정 배치 파일들처럼 한번 실행하고 종료되는 성격의 작업에 사용

```yaml
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
          command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: OnFailure
```

### 잡 컨트롤러의 레이블

파드 템플릿의 레이블/잡 컨트롤러의 레이블 셀렉터는 지정하지 않는다.
-> 잘못된 매핑으로 기존의 파드를 종료하지 않게 하기 위함

### 파드의 종료 및 삭제

`job.spec.activeDeadlineSeconds` : 애플리케이션이 실행될 수 있는 시간 지정
`job.spec.ttlSecondsAfterFinished` : 컨트롤러 및 파드 삭제

```yaml
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
          command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: OnFailure
  ttlSecondsAfterFinished: 10
```

### 작업의 병렬 처리

`job.spec.completions` : 완료 횟수
`job.spec.parallelism` : 병렬 개수

```yaml
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
          command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(1500)"]
      restartPolicy: OnFailure
```

### Parallel job with fixed completion count

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-app-job
spec:
  completions: 3
  parallelism: 2
  template:
    spec:
```

컨트롤러는 3개의 Pod가 성공적으로 종료될 때까지 동시에 Pod 최대 두 개를 실행하여 태스크를 처리한다. 실행 중인 Pod 중 하나가 성공적으로 완료되면 컨트롤러는 다음 Pod를 시작한다. 지정된 완료 횟수에 도달하면 작업이 완료된 것으로 간주된다. 남은 완료 횟수가 parallelism 값보다 작으면, 해당 시점에 작업에 대해 원하는 총 횟수를 완료하기에 충분한 나머지 Pod가 실행되고 있기 때문에 컨트롤러는 새 Pod를 예약하지 않는다.

### Failing a Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-app-job
spec:
  backoffLimit: 4
  activeDeadlineSeconds: 300
  template:
    spec:
```

Pod 실패를 제한하는 한 가지 방법은 backoffLimit을 사용하는 것이다. 또 다른 옵션은 activeDeadlineSeconds 설정을 사용하여 작업 완료에 대한 활성 기한을 설정한다. 시한데 도달하면 작업과 모든 Pod는 deadline exceeded를 이유로 종료된다(활성 기한이 backoffLimit 보다 우선).

## CronJob

- 지정한 일정에 따라 반복적으로 Job을 실행

> kubectl explain cj --api-version=batch/v1beta1

```yaml
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
