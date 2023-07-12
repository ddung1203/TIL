# StatefuleSet

Deployment와 다르게 StatefulSet은 각 Pod의 독자성을 유지한다. 이 Pod들은 동일한 spec으로 생성되지만, 서로 교체는 불가능하다.
즉, 각각은 재 스케쥴링 간에도 지속적으로 유지되는 식별자를 가진다.
Storage Volume을 사용해서 워크로드에 지속성을 제공하려는 경우, 솔루션의 일부로 StatefulSet을 사용할 수 있다. StatefulSet의 개별 Pod는 장애에 취약하지만, Persistent Pod 식별자는 기존 Volume을 실패한 Volume을 대체하는 새 Pod에 더 쉽게 일치시킬 수 있다.

- 파드들의 순서 및 고유성을 보장한다. (배포, 업데이트, 스케일링시)
- 재 스케줄링 간에도 지속적으로 유지되는 식별자를 가진다. (네트워크)
- PV를 유지할 수 있다.

> 스테이트풀셋이란, 애플리케이션의 상태를 저장하고 관리하는 데 사용되는 쿠버네티스 객체이다. 기존의 Pod를 삭제하고 생성할 때 상태가 유지되지 않는 한계가 있다. 때문에 Pod를 삭제하고 생성하면 완전히 새로운 가상환경이 시작된다. 하지만 필요에 따라 이러한 Pod의 상태를 유지하고 싶을 수 있다. 응용프로그램의 로그나 기타 다른 정보들을 함께 저장하고자 하는 경우 단순히 PV를 하나 마운트해 이를 유지하기는 어렵다. 스테이트풀셋으로 생성되는 Pod는 영구 식별자를 가지고 상태를 유지시킬 수 있다.

## Headless Service

DB와 같이 master, slave 구조가 있는 서비스들의 경우 service를 통해 로드밸런싱을 하지 않고 개별 Pod의 주소를 알고 접속해야한다.

Pod들은 DNS 이름을 가질 수는 있으나 `{pod name}.{service name}.{namespace}.svc.cluster.local` 형식의 이름을 갖기 때문에 Pod를 DNS를 이용해 접근하려면 service name이 있어야 한다.

Statefulset에 의한 서비스들은 Kubernetes의 `Service`를 이용해서 로드 밸런싱을 하는 것이 아니기 때문에 로드 밸런서의 역할은 필요없고 논리적으로 Pod들을 묶어 줄 수 있는 `Service`만 있으면 되기 때문에 헤드리스 서비스를 사용한다.

Headless 서비스를 이용하면 `Service` 가 로드 밸런서의 역할도 하지 않고 단일 IP도 가지지 않지만 nslookup을 이용해서, headless 서비스에 의해서 묶여진 Pod들의 이름도 알 수 있고 `{pod name}.{service name}.{namespace}.svc.cluster.local` 이름으로, 각 pod 에 대한 접근 주소 역시 얻을 수 있다.

쿠버네티스 생성 시 `svc.spec.clusterIP` 필드 값을 None으로 설정하면 ClusterIP가 없는 서비스를 만들 수 있다.

헤드리스 서비스의 경우 ClusterIP가 할당되지 않고 kube-proxy가 서비스를 처리하지 않으며 로드 밸런싱 또는 프록시 동작을 수행하지 않는다. DNS가 자동으로 구성되는 방법은 서비스에 셀렉터가 정의되어 있는지 여부에 달려있다.

헤드리스 서비스에 셀렉터 필드를 구성하면 쿠버네티스 API로 확인할 수 있는 엔드포인트(endpoint)가 만들어진다.
서비스와 연결된 파드를 직접 가리키는 DNS A 레코드도 만들어진다.

만약 셀렉터가 없는 경우 엔드포인트가 만들어지지 않는다.
단, 셀렉터가 없더라도 DNS 시스템에는 ExternalName 타입의 서비스에서 사용할 CNAME 레코드가 생성된다.

> ClusterIP, NodePort, LoadBalancer와 같은 다른 타입의 서비스는 클라이언트가 Pod에 접근하기 위해 kube-proxy로 접근한 후 프록시되어 Pod에 액세스하게 된다. 프록시로 접근하는 경우, 현재 연결된 Pod와 다음번에 연결될 Pod가 같다는 보장을 할 수 없기 때문에, Stateful한 애플리케이션에 적합하지 않다.

> StatefulSet은 Pod를 생성할 때 순차적으로 기동되고, 삭제할때도 순차적으로 삭제한다. 그런데 만약 그런 요건이 필요없이 전체가 같이 기동되도 된다면 `.spec.pod.ManagementPolicy`를 통해서 설정할 수 있다. `.spec.podManagementPloicy`는 디폴트로 `Ordered Ready` 설정이 되어 있고, Pod가 순차적으로 기동되도록 설정이 되어 있고, 병렬로 동시에 모든 Pod를 기동하고자 하면 `Parallel`을 사용하면 된다.

> **개별 Pod에 대한 디스크 볼륨 관리**
>
> StatefulSet의 경우 PVC를 템플릿 형태로 정의하여, Pod 마다 각각 PVC와 PV를 생성하여 관리할 수 있도록 한다. 따라서, `.spec.accessModes` 또한 `ReadWriteOnce`로 설정하도록 한다.

`myweb-svc.yaml`

```yaml
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

```yaml
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

```yaml
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

하기와 같이 `myweb-svc`에 DNS 질의를 하면 ClusterIP 주소를 응답한다.

```bash
kubectl run nettool -it --image ghcr.io/c1t1d0s7/network-multitool --rm

> host myweb-svc
myweb-svc.default.svc.cluster.local has address 10.233.3.43
> host myweb-svc-headless
myweb-svc-headless.default.svc.cluster.local has address 10.233.92.118
myweb-svc-headless.default.svc.cluster.local has address 10.233.90.77
myweb-svc-headless.default.svc.cluster.local has address 10.233.90.79
```

Headless service에 DNS를 질의를 했을 때 응답되는 IP는 Pod의 IP이다.

Service의 자체 IP가 없는 것을 Headless servcie 라고 하며 Headless service를 질의하면 `myweb-svc-headless.default.svc.cluster.local` SVC의 ip가 응답하게 된다.

파드가 3개이기 때문에 3개의 endpoint 주소를 응답한다.

## StatefulSet

StatefulSet은 다음 중 하나 또는 이상이 필요한 애플리케이션에 유용하다.

- 안정된, 고유한 네트워크 식별자
- 안정된, 지속성을 갖는 스토리지
- 순차적인, 정상 배포와 스케일링
- 순차적인, 자동 롤링 업데이트

> StatefulSet에 붙이는 스토리지는 반드시 pvc여야 한다. emptyDir, hostPath는 붙일 수 없다.
> 스토리지 클래스가 존재해야 하며 동적 프로비저닝이 구성되어 있어야 한다.
> 파드를 삭제해도 볼륨이 삭제되지 않는다. 파드가 삭제돼도 고유성이 지켜져야하기 때문에 데이터를 유지하기 위해서다.

### 예제 1.

`myweb-svc-headless.yaml`

```yaml
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

```yaml
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

```bash
kubectl run nettool -it --image ghcr.io/c1t1d0s7/network-multitool --rm

> host myweb-svc-headless
> host myweb-sts-0.myweb-svc-headless
> host myweb-sts-1.myweb-svc-headless
> host myweb-sts-2.myweb-svc-headless
```

스케일링을 하면 예측 가능한 myweb-sts-3이 만들어진다.

스케일링을 줄여도 마찬가지다 --replicas 2로 바꾸면 myweb-sts-3, myweb-sts-2이 지워지고 지울 때도 절대로 한번에 지우지 않고 순서대로 지운다.

다시 --replicas 4로 변경하면 myweb-sts-2가 생성된 후에야 myweb-sts-3이 생성된다.

--replicas 0을 설정할 수도 있는데 3 → 2 → 1 → 0 순으로 지워진다.

StatefulSet은 파드 집합의 배포와 스케일링을 관리하며, 파드들의 순서 및 고유성을 보장한다.

### 에제 2. PVC 템플릿

`myweb-sts-vol.yaml`

```yaml
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

ReplicaSet이나 Deployment의 경우 여러개의 파드가 동시에 쓰기를 해야하는 경우가 생길 수 있어서 RWX라는 것이 필요했지만, 지금 상황은 파드가 자신만의 공간을 사용하는 것이기 때문에 굳이 Many를 세팅하지 않아도 상관없다.

여기에 `--replicas=4`로 조정하면 pv, pvc가 4개가 된다.

또한 `myweb-sts-vol-1` Pod를 지우고 새롭게 만들어진 같은 이름의 파드는 앞서 만들어둔 데이터를 볼 수 있다.

즉, 고유성을 보장할 수 있다.

### 에제 3. One Master Multi Slave

STS를 통해 MySQL 노드를 생성한다. Master는 R/W가 가능하고 나머지는 다 Slaver로 Read Only이다.

이러한 구성을 One Master Multi Slave라고 한다.

https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/

상기 문서를 참고하여 구성한다.
