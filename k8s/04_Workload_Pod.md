# Workload - Pod

> https://kubernetes.io/ko/docs/concepts/workloads/pods/

파드 : 컨테이너의 모음
> 쿠버네티스가 관리할 수 있는 가장 작은 워크로드는 파드

## 파드 생성 및 관리

명령형 커맨드로 파드 생성

``` bash
kubectl run myweb --image httpd
```

파드 목록 확인

``` bash
kubectl get pods
```

특정 파드 확인

``` bash
kubectl get pods myweb
```

파드 상세 정보
``` bash
kubectl get pods -o wide
```

``` bash
kubectl get pods -o yaml
```

``` bash
kubectl get pods -o json
```

``` bash
kubectl describe pods myweb
```

## YAML 파일로 파드 정의

`myweb.yaml`

``` yaml
apiVersion: v1
kind: Pod
metadata:
	name: myweb
spec:
	containers:
		- name: myweb
			image: httpd
			ports:
				- containerPort: 80
					protocol: TCP
```

``` bash
kubectl create -f myweb.yaml
```

``` bash
kubectl get -f myweb.yaml
```

``` bash
kubectl describe -f myweb.yaml
```

``` bash
kubectl delete -f myweb.yaml
```

## kubectl 명령의 서브 명령

- create
- get
- describe
- logs
- delete
- replace
- patch
- apply
- diff

## 파드 디자인

![04_1](./img/04_1.png)

- 단일 컨테이너 : 일반적인 형태
- 멀티 컨테이너 : 메인 애플리케이션이 존재
	메인 애플리케이션 기능을 확장하기 위한 컨테이너를 배치

> 사이드카 패턴 : https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns/

- sidecar : 기능의 확장
- ambassador : 프록시 / LB
- adaptor : 출력의 표준

## 포트 및 포트포워딩

테스트 & 디버깅 목적

``` bash
kubectl port-forward pods/myweb 8080:80
```

## 이름 & UID
이름 : 네임스페이스 유일
UID : 클러스터에서 유일