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
	- grcp 프로토콜 연결
- exec
	- 명령 실행
	- 종료 코드 0!

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