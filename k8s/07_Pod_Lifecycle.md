# Pod Lifecycle / Lifetime

# Pod 상태

- Pending : 스케줄링되기 전, 이미지 받기 전, 컨테이너가 준비되기 전
- Running : 컨테이너가 실행 중, 실행 전, 재시작 중
- Succeed : 정상 종료 (0)
- Failed : 비정상 종료 (!0)
- Unknown : 노드의 통신 문제로 상태 알 수 없음

## Container 상태

- Waiting : 이미지 받기 전, 볼륨 연결 되기 전
- Running : 실행 중
- Terminated : 종료

## 재시작 정책

- pod.spec.restartPolicy
  - Always(기본)
  - OnFailure
  - Never

## 지수 백오프

- 파드 실패 시 재시작 정책에 의해 재시작을 하게 됨
  - 재시작 시간 10, 20, 40, 80, ..., 300초 까지 유예기간

## 컨테이너 프로브

### 프로브 종류

- liveness : 애플리케이션 실행/작동 여부
- readiness
- startup : 애플리케이션이 시작되었는지 확인, 성공하지 않으면 나머지 프로브 비활성화

livenessProbe는 애플리케이션이 정상 상태를 유지하고 있는지 지속해서 검사하는 것이고, readinessProbe는 애플리케이션이 시작된 뒤 초기화 작업이 마무리되어 준비가 되었는지 검사하는 것이 목적이다.

livenessProbe 검사에 실패했다는 것은 애플리케이션 내부에서 문제가 발생했다는 것이기 때문에 컨테이너를 재시작한다.

readinessProbe가 실패했다는 것은 애플리케이션이 실행 직후 초기화 동의 작업으로 인해 아직 준비되지 않다는 뜻이기 때문에 사용자의 요청이 전달되지 않도록 서비스의 라우팅 대상에서 Pod의 IP를 제외한다. 어느 정도 시간이 지나 애플리케이션의 초기화 작어빙 끝나 준비가 되면 readinessProbe 검사에 성공하고 사용자의 요청이 Pod로 전달될 수 있게 서비스의 라우팅 대상에 Pod의 IP가 추가된다. 

### 프로브 매커니즘

- httpGet
  - Web, WebApp
  - 응답 코드 2XX, 3XX
- tcpSocket
  - 해당 포트 TCP 연결
- grpc
  - grpc 프로토콜 연결
- exec
  - 명령 실행
  - 종료 코드 0!

### Running 상태가 되기 위한 조건

Running은 Pod의 컨테이너들이 정상적으로 생성됐다는 것을 의미한다.

- Init Container
- postStart
- livenessProbe, readinessProbe

**Init Container**

Init 컨테이너는 컨테이너 내부에서 애플리케이션이 실행되기 전에 초기화를 수행하는 컨테이너이다. Pod의 애플리케이션 컨테이너가 실행되기 전에 특정 작업을 미리 수행하는 용도로 사용할 수 있다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-container-example
spec:
  initContainers:
    - name: my-init-container
      image: busybox
      command: ["sh", "-c", "echo Hello world"]
  containers:
    - name: nginx
      image: nginx
```

상기의 `initConatainers` 항목이 먼저 실행된 뒤, `containers` 항목에 정의한 컨테이너가 생성된다.

이때 Init 컨테이너가 하나라도 실패하게 된다면 Pod의 애플리케이션 커넽이너는 실행되지 않으며, Pod의 restartPolicy에 따라서 Init 컨테이너가 재시작된다. 따라서 Pod가 최종적으로 Running 상태가 되려면 Init 컨테이너 실행이 완료되어야 한다.

이러한 성질로, Init 컨테이너 내부에서 하기와 같이 `dig`나 `nslookup` 명령어 등을 이용해 다른 Deployment가 생성되기를 기다리거나, 애플리케이션 커네티언가 사용할 설정 파일 등을 미리 준비해 둘 수 있다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-container
spec:
  containers:
    - name: nginx
      image: nginx
  initContainers:
    - name: wait
      image: busybox
      command:
        [
          "sh",
          "-c",
          "until nslookup myservice; do echo waiting..; sleep 1; done;",
        ]
```

**postStart**

Pod의 컨테이너가 실행되거나 삭제될 떄, 특정 작업을 수행하도록 Hook을 정의할 수 있다.

- HTTP: 컨테이너가 시작한 직후, 특정 주소로 HTTP 요청을 전송
- Exec: 컨테이너가 시작한 직후, 컨테이너 내부에서 특정 명령어를 실행

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: poststart-hook
spec:
  containers:
    - name: poststart-hook
      image: nginx
  lifecycle:
    postStart:
      exec:
        command: ["sh", "-c", "touch /myfile"]
```

postStart는 컨테이너의 Entrypoint와는 비동기적으로 실행되며, Init 컨테이너와 마찬가지로 요청이 실행되지 않으면 Running 상태로 전환되지 않는다.

> Init 컨테이너의 로그는 확인이 가능하지만, postStart의 실행 로그는 에러가 발생하지 않는 한 별도로 확인할 수 없다.

**livenessProbe, readinessProbe**

- livenessProbe: 컨테이너 내부의 애플리케이션이 살아있는지 검사한다. 검사에 실패할 경우 해당 컨테이너는 restartPolicy에 따라 재시작된다.
- readinessProbe: 컨테이너 내부의 애플리케이션이 사용자 요청을 처리할 준비가 되었는지 검사한다. 검사에 실패할 경우 컨테니어는 서비스의 라우팅 대상에서 제외된다.

`livenessProbe.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: livenessprobe
spec:
  containers:
    - name: livenessprobe
      image: nginx
      livenessProbe:
        httpGet:
          port: 80
          path: /
```

- httpGet: HTTP 요청을 전송해 상태 검사
- exec: 컨테이너 내부에서 명령어를 실행해 상태 검사
- tcpSocket: TCP 연결이 수립될 수 있는지 체크함으로써 상태 검사

`readinessProbe.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: readinessprobe
spec:
  containers:
    - name: readinessprobe
      image: nginx
      readinessprobe:
        httpGet:
          port: 80
          path: /
```

readinessProbe의 실패의 경우 RESTARTS 횟수가 증가하지 않으며, 단순히 READY 상태인 컨테이너가 하나 줄어들게 된다. 따라서 서비스 리소스는 사용자 요청을 이 Pod로 전달하지 않는다.

### 프로브 결과

- success
- failure
- unknown

`pods.spec.containers.livenessProbe`

- exec
- httpGet
- tcpSocker
- periodSeconds : 프로브 주기
- failureThreshold : 실패 임계값
- successThreshold : 성공 임계값
- initialDelaySecond : 프로브 유예 기간
- timeoutSeconds : 프로브 타임아웃

## 리소스 관리

### 기본 리소스 요청과 상한

컨테이너의 리소스 요구 사항을 매번 미리 파악하는 것은 어렵다. `LimitRange` 리소스를 사용하면 네임스페이스 내 모든 컨테이너의 기본 요청과 상한을 설정할 수 있다.

리소스 요청과 상한을 지정하지 않은 네임스페이스의 모든 컨테이너는 LimitRange에서 기본값을 상속받는다. 예를 들어 지정된 cpu 요청이 없는 컨테이너는 LimitRange에서 200m 값을 상속받는다. 마찬가지로 지정된 memory 상한이 없는 컨테이너는 256Mi를 상속받는다.

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: demo-limitrange
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "256Mi"
    defaultRequest:
      cpu: "200m"
      memoty: "128Mi"
    type: Container
```

### 워크로드를 균형 있게 유지

쿠버네티스 스케줄러는 워크로드를 가능한 많은 노드에 고르게 분산하고 고가용성을 위해 각각 다른 노드에 레플리카 파드를 배치한다.

일반적으로 스케줄러는 잘 작동하지만 주의해야 할 몇 가지 예외 상황이 있다.

예를 들어 두 개의 서비스를 가진 두 개의 노드가 있고 서비스 A와 B는 각각 두 개의 복제본을 가지고 있다고 가정하자. 균형 잡힌 클러스터라면 각 노드에 서비스 A와 B의 레플리카가 하나씩 있을 것이다.

```
A, B        A, B
노드 1       노드 2
```

만약 노드 2가 종료되었다고 가정해보자. 스케줄러는 A와 B가 추가 레플리카가 필요하다는 것을 인지할 것이고 수용 가능한 노드는 단 한 대 뿐이다. 이제 노드 1에서는 서비스 A와 B의 레플리카 두 개가 실행 중이다.

고장난 노드 2를 교체하기 위해 새로운 노드를 스핀업 한다고 가정하자. 새로운 노드가 사용 가능한 상태지만 수용 중인 파드는 없을 것이다. 스케줄러는 실행 중인 파드를 다른 노드로 이동시키지 않기 때문이다.

```
A, A, B, B
노드 1       노드 2
```

더 나빠질 수 있다. 서비스 A에 롤링 업데이트를 배포한다고 가정하자. 스케줄러는 서비스 A의 새로운 레플리카를 두 개를 실행하고 실행 완료를 기다렸다가 이전 레플리카를 종료한다. 노드 1은 이미 네 개의 파드를 실행 중이므로 유휴 상태인 새로운 노드 2에서 실행된다. 이제 새로운 서비스 A의 레플리카 두 개는 노드 2에서 실행되고 이전 레플리카는 노드 1에서 제거된다.

```
B, B        A, A
노드 1       노드 2
```

서비스 B의 레플리카가 노드 1에 있고 서비스 A의 레플리카는 동일한 노드에 있기 때문에 상황이 더 나빠졌다. 두 개의 노드가 있지만 고가용성을 보장하지 못하는 상태로 노드 1이나 노드 2에서 장애가 발생하면 서비스가 중단될 것이다.

문제는 스케줄러는 재시작하지 않는 한 파드를 다른 노드로 이동시키지 않는다는 것이다. 또한 워크로드를 노드에 고르게 분산시키는 스케줄러의 목적은 개별 서비스의 고가용성을 유지하는 것과 때로는 상충된다.

이를 해결하는 방법은 [디스케줄러](https://github.com/kubernetes-incubator/descheduler) 도구를 사용하는 것이다. 쿠버네티스 잡으로 자주 실행할 수 있으며 이동이 필요한 파드를 찾고 종료하여 클러스터의 균형을 재조정하는 데 최선을 다할 것이다.

한 정책은 사용률이 낮은 노드를 찾고 다른 노드에서 실행 중인 파드를 강제로 종료하여 유휴 노드로 다시 스케줄되게 한다.

또 다른 정책은 두 개 이상의 레플리카가 동일한 노드에서 실행 중인 중복 파드를 찾아 퇴출한다. 이러헤 하면 예제와 같이 워크로드가 균형을 이루지만 두 서비스 모두 실제로는 고가용성을 보장하지 못하는 문제를 해결할 수 있다.