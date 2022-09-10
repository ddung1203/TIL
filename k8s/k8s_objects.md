# Kubernetes Objects

> https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/kubernetes-objects

## 오브젝트 종류

``` bash
kubectl api-resources
```

- Label / LabelSelector
- Workload
	- Pod
	- Controller
		- ReplicationController
		- ReplicaSets
		- DaemonSets
		- Jobs
		- CronJobs
		- Deployments
		- StatefulSets
		- HorizontalPodAutoscaler
- Network
	- Service
	- Endpoints
	- Ingress
- Storage
	- PersistentVolume
	- PersistentVolumeClaim
	- ConfigMap
	- Secret
- Authentication
	- ServiceAccount
	- RBAC
		- Role
		- ClusterRole
		- RoleBinding
		- ClusterRoleBinding
- Resource Isolation
	- Namespaces
- Resource Limits
	- Limits
	- Requests
	- ResourceQuota
	- LimitRange
- Scheduling
	- NodeName
	- NodeSelector
	- Affinity
		- Node Affinity
		- Pod Affinity
		- Pod Anti Affinity
	- Taints/Tolerations
	- Drain/Cordon

### 오브젝트의 버전

> https://kubernetes.io/ko/docs/reference/using-api/#api-%EA%B7%B8%EB%A3%B9

``` bash
kubectl api-versions
```

apps/v1
- apps : 그룹
- v1 : 버전

> 그룹이 없는 api는 core 그룹

- Stable
	- Vx
	- v1, v2
	- 안정화된 버전
- Beta
	- v1betaX, v2betaX
	- 충분히 검증 되었고, 오류 없음
	- 버전이 올라가면 기능 변경이 있을 수 있음
		- downtime 발생할 수 있음 : 특정 기능을 사용하기 위해 재시작
	- Mission Critical
- Alpha
	- v1alphaX, c2alphaX
	- 기본 비활성화
	- 개발중인 API

Alpha -> Beta -> Stable

- v1alpha1 -> v1alpha2 -> v1alpha3 -> v1beta1 -> v1beta2 -> v1

## 오브젝트 정의

```
apiVersion:
kind:
metdata:
spec:
```

- kind: 오브젝트의 종류
- apiVersion: 지원하는 오브젝트의 버전
- metadata: 오브젝트의 메타데이터
	- 이름, 네임스페이스, 레이블, 어노테이션
- spec: 오브젝트에 대한 선언

``` bash
kubectl explain pods
kubectl explain pods.metadata
kubectl explain pods.spec
kubectl explain pods.spec.containers
kubectl explain pods.spec.containers.images
kubectl explain pods.spec --recursive
```

## 오브젝트 관리

> https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/object-management/

- 명령형 커멘드 : kubectl 명령으로만 구성
	- `kubectl create`
	- `kubectl run`
	- `kubectl expose`

- **명령형 오브젝트 구성** : YAML 파일을 순서대로 하나씩 실행

	- `kubectl create -f a.yaml`
	- `kubectl replace -f a.yaml`
	- `kubectl patch -f a.yaml`
	- `kubectl delete -f a.yaml`
- 선언형 오브젝트 구성: YAML 파일의 모음을 한번에 실행
	- `kubectl apply -f resources/`