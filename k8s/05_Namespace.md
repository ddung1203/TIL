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

```bash
kubectl get namespaces
```

- kube-system: Kubernetes의 핵심 컴포넌트
- kube-public: 모든 사용자가 읽기 권한
- kube-node-lease: 노드의 HeartBeat 체크를 위한 Lease 리소스가 존재
- default: 기본 작업 공간

```bash
kubectl create ns developments
```

```bash
kubectl delete ns developments
```

```bash
kubectl get pods -A | --all-namespaces
```

```bash
kubectl get pods -n kube-system
```

`ns-dev.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

```bash
kubectl create -f ns-dev.yaml
```

`myweb-dev.yaml`

```yaml
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

```bash
kubectl create -f myweb-dev.yaml
```

```bash
kubectl delete -f myweb-dev.yaml
```

## 네임스페이스에 종속되는 쿠버네티스 오브젝트와 독립적인 오브젝트

네임스페이스를 사용하면 쿠버네티스 리소스를 사용 목적에 따라 논리적으로 격리할 수 있지만, 모든 리소스가 네임스페이스에 의해 구분되는 것은 아니다.
네임스페이스에 속하는 오브젝트의 종류는 하기 명령어로 확인할 수 있다.

```bash
kubectl api-resources --namespace=true
kubectl api-resources --namespace=false
```

## 다중 개발자를 위한 공용 클러스터 구축

K8s의 Namespace를 통해 개발자 분리를 간단하게 진행한다. NS는 서비스 배포 범위를 제한하여 특정 사용자의 프런트엔드 서비스가 다른 사용자의 프런트엔드 서비스에 피해를 주지 않도록 만든다. 또한 RBAC의 범위도 제한하기 때문에 특정 개발자가 실수로 다른 개발자의 작업 결과를 삭제하는 것을 막을 수 있다. 따라서 공용 클러스터에서 개발자의 작업 공간으로 NS를 사용하도록 설정한다.

> 클러스터를 관리하고 있는 admin은 클러스터 내의 모든 권한을 갖지만, 이 권한을 모든 사용자가 가져서는 안된다. 개발자나, 특정 리소스에만 접근이 필요한 사용자에게 최소 권한의 원칙에 맞추어 필요한 만큼의 권한만 부여해야 하는데, 특정 NS를 생성하고, read/write 권한을 갖는 kubeconfig를 생성하여 이 config를 사용하는 사용자가 적절한 권한을 이용하여 클러스터에 접근할 수 있도록 한다.

`Service Account`

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
name: sa-dev
  namespace: dev
```

`RoleBinding`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-rolebinding
  namespace: dev
subjects:
  - kind: ServiceAccount
    name: sa-dev
    namespace: dev
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: edit
  # SA에 부여할 Role을 생성하여 부여 가능
```

참고: [16_RBAC](./16_RBAC.md)

> `1.24` 버전부터 SA token이 자동으로 생성되지 않는다. 따라서 수동으로 생성해야 한다.
>
> 참고: https://kubernetes.io/docs/concepts/configuration/secret/#service-account-token-secrets

`sa-dev-token.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: sa-dev-token
  annotations:
    kubernetes.io/service-account.name: sa-dev
type: kubernetes.io/service-account-token
```

```bash
kubectl create -f sa-dev-token.yaml -n dev
kubectl describe secret sa-dev -n dev
# 하기 명령어와 같음
kubectl get secret/sa-dev-token -n dev -o jsonpath="{.data['token']}" | base64 --decode

Name:         sa-dev-token
Namespace:    dev
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: sa-dev
              kubernetes.io/service-account.uid: 4817ec07-6e71-41a1-87e4-36949e8dba8d

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1099 bytes
namespace:  3 bytes
token:      <TOKEN>
```

```bash
kubectl get secret/sa-dev-token -n dev -o jsonpath="{.data['ca\.crt']}"
```

이제 생성된 kubeconfig를 `--kubeconfig` 혹은 `kubectx`를 사용하여 해당 namespace에서 read, write가 가능한 환경이 조성된다.

````bash
 jeonj@ubuntu > ~ > kubectl get ns --kubeconfig ./kubeconfig
Error from server (Forbidden): namespaces is forbidden: User "system:serviceaccount:dev:sa-dev" cannot list resource "namespaces" in API group "" at the cluster scope```
````
