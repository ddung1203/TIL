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

``` yaml
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

``` yaml
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
    command: ["sh", "-c", "until nslookup myservice; do echo waiting..; sleep 1; done;"]
```

**postStart**

Pod의 컨테이너가 실행되거나 삭제될 떄, 특정 작업을 수행하도록 Hook을 정의할 수 있다.

- HTTP: 컨테이너가 시작한 직후, 특정 주소로 HTTP 요청을 전송
- Exec: 컨테이너가 시작한 직후, 컨테이너 내부에서 특정 명령어를 실행

``` yaml
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
``` yaml
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
``` yaml
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