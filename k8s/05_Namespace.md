# Namespace

Namespace란 Kubernetes 클러스터 내 논리적인 분리 단위이자 오브젝트를 묶는 하나의 가상 공간 또는 그룹이다.

리소스를 분리
- 서비스 별
- 사용자 별
- 환경 : 개발, 스테이징, 프로덕션

> 서비스 : DNS 이름이 분리되는 용도
> RBAC : 권한을 NS에 설정

> https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/namespaces/


**주의**
namespace는 물리적으로 분리하는 것이 아니다.

다른 namespace 간의 Pod라도 통신은 가능하며 클러스터의 장애가 발생할 경우 모든 namespace가 타격을 입게되므로 namespace를 통한 fault-tolerance 확보는 불가능하다.

- 사용자별 namespace 접근 권한 (ABAC, RBAC)
- namespace 별 리소스 할당량 지정

<br>

기본 namespace

- default: 다른 namespace가 없는 오브젝트를 위한 기본 namespace
- kube-system: Kubernetes 시스템에서 생성한 오브젝트를 위한 namespace
- kube-public: 오든 사용자가 읽기 권한으로 접근할 수 있으며 이 namespace는 주로 전체 클러스터 중에 공개적으로 확인되어 읽을 수 있는 리소스를 위해 예약되어 있음



``` bash
kubectl get namespaces
```

- kube-system: Kubernetes의 핵심 컴포넌트
- kube-public: 모든 사용자가 읽기 권한
- kube-node-lease: 노드의 HeartBeat 체크를 위한 Lease 리소스가 존재
- default: 기본 작업 공간

``` bash
kubectl create ns developments
```

``` bash
kubectl delete ns developments
```

``` bash
kubectl get pods -A | --all-namespaces
```

``` bash
kubectl get pods -n kube-system
```


`ns-dev.yaml`
``` yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

``` bash
kubectl create -f ns-dev.yaml
```

`myweb-dev.yaml`
``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb
  namespace: dev
spec:
  containers:
    - name: myweb
      image: httpd
      ports:
        - containerPort: 80
          protocol: TCP          
```

``` bash
kubectl create -f myweb-dev.yaml
```

``` bash
kubectl delete -f myweb-dev.yaml
```

## 네임스페이스에 종속되는 쿠버네티스 오브젝트와 독립적인 오브젝트

네임스페이스를 사용하면 쿠버네티스 리소스를 사용 목적에 따라 논리적으로 격리할 수 있지만, 모든 리소스가 네임스페이스에 의해 구분되는 것은 아니다.
네임스페이스에 속하는 오브젝트의 종류는 하기 명령어로 확인할 수 있다.

``` bash
kubectl api-resources --namespace=true
kubectl api-resources --namespace=false
```
