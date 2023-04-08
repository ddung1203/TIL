# RBAC : Role Based Access Control

## Kubeconfig

`~/.kube/config`: Kubernetes 설정 파일

``` yaml
apiVersion: v1
kind: Config
preferences: {}
clusters:
- name: cluster.local
  cluster:
    certificate-authority-data: LS0tLS1...
    server: https://127.0.0.1:6443
- name: mycluster
  cluster:
    server: https://1.2.3.4:6443
users:
- name: myadmin
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1...
    client-key-data: LS0tLS1...
contexts:
- context:
    cluster: mycluster
    user: myadmin
  name: myadmin@mycluster
- context:
    cluster: cluster.local
    user: kubernetes-admin
  name: kubernetes-admin@cluster.local
current-context: kubernetes-admin@cluster.local
```

상기 파일은 `kubectl` 명령어가 api-server에 접근할 때 사용할 인증 정보를 가지고 있다. 

- cluster.local : 설정하지 않아도 기본적으로 구성되는 클러스터 이름
- client-authority-data : kubectl이 어떤 서버에 요청할 것인지에 대한 정보와 CA 인증서를 base64로 인코딩한 것
- server : 실제 api-server의 주소
- name : 사용자의 계정명
- client-certificate-data, client-key-data : 사용자가 사용할 클라이언트의 인증서(공개키)와 개인키

`~/.kube/config` 파일을 수정해서 새로운 cluster와 context를 추가 후 하기 명령어를 실행한다.

``` yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: ==
    server: https://127.0.0.1:6443
  name: cluster.local
- clusters:
    server: https://1.1.1.1
  name: jeonj-cluster
contexts:
- context:
    cluster: cluster.local
    user: kubernetes-admin
  name: kubernetes-admin@cluster.local
- context:
    cluster: jeonj-cluster
    user: jeonj
  name: jeonj@jeonj-cluster
current-context: kubernetes-admin@cluster.local
kind: Config
preferences: {}
users:
- name: jeonj
- name: kubernetes-admin
  user:
    client-certificate-data: ==
    client-key-data:  ==

```

``` bash
kubectl config view
```

``` bash
kubectl config get-clusters
kubectl config get-contexts
kubectl config get-users
```

``` bash
kubectl config use-context jeonj@jeonj-cluster
```

## 인증
쿠버네티스의 사용자

- Service Account(sa) : 쿠버네티스가 관리하는 SA 사용자
  - 사용자 X
  - Pod 사용
- Normal User : 일반 사용자(쿠버네티스가 관리 X)
  - 사용자 O
  - Pod 사용 X

인증 방법
- x509 인증서
- 토큰
  - Bearer Token
    - HTTP 헤더:
    - `Authorization: Bearer 31ada4fd-adec-460c-809a-9e56ceb75269`
  - SA Token
    - JSON Web Token : JWT
  - OpenID Connect(OIDC)
    - 외부 인증 표준화 인터페이스
    - okta, AWS IAM
    - OAuth2 Provider

## RBAC
- Role : 권한(NS)
- ClusterRole : 권한(Global)
- RoleBinding
  - Role <-> RoleBinding <-> SA/User
- ClusterRoleBinding
  - ClusterRole <-> ClusterRoleBinding <-> SA/User
> https://kubernetes.io/docs/reference/access-authn-authz/rbac/

#### Role

``` yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

rules에는 사용자가 어떤 권한을 사용할 수 있는지를 설정한다.
Pods 리소스에 대해서 get, watch, list를 할 수 있다는 것이다. rules와 verbs는 리스트이므로 여러개를 지정할 수 있다.


#### 요청 동사
- create
  - `kubectl create`, `kubectl apply`
- get
  - `kubectl get po myweb`
- list
  - `kubectl get pods`
- watch
  - `kubectl get po -w`
- update
  - `kubectl edit`, `kubectl replace`
- patch
  - `kubectl patch`
- delete
  - `kubectl delete po myweb`
- deletecollection
  - `kubectl delete po --all`

``` bash
 vagrant@k8s-node1 > ~ > kubectl get po -v=7
I0408 00:08:14.717424   13976 loader.go:372] Config loaded from file:  /home/vagrant/.kube/config
I0408 00:08:14.760262   13976 round_trippers.go:463] GET https://127.0.0.1:6443/api/v1/namespaces/default/pods?limit=500
I0408 00:08:14.760367   13976 round_trippers.go:469] Request Headers:
I0408 00:08:14.760492   13976 round_trippers.go:473]     Accept: application/json;as=Table;v=v1;g=meta.k8s.io,application/json;as=Table;v=v1beta1;g=meta.k8s.io,application/json
I0408 00:08:14.760566   13976 round_trippers.go:473]     User-Agent: kubectl/v1.24.6 (linux/amd64) kubernetes/b39bf14
I0408 00:08:14.801163   13976 round_trippers.go:574] Response Status: 200 OK in 40 milliseconds
```
`-v`: 상세정보를 보는 옵션으로, 0~9 값을 지정한다(0<9).


#### ClusterRole

``` yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  # "namespace" omitted since ClusterRoles are not namespaced
  name: secret-reader
rules:
- apiGroups: [""]
  #
  # at the HTTP level, the name of the resource for accessing Secret
  # objects is "secrets"
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

- view : 읽을 수 있는 권한
- edit : 생성/삭제/변경할 수 있는 권한
- admin : 모든것 관리(-RBAC : ClusterRole 제외)
- cluster-admin : 모든것 관리

## SA

``` bash
kubectl create sa <NAME>
```

## 사용자 생성을 위한 x509 인증서
Private Key
``` bash
openssl genrsa -out myuser.key 2048
```

x509 인증서 요청 생성
``` bash
openssl req -new -key myuser.key -out myuser.csr -subj "/CN=myuser"
```

``` bash
cat myuser.csr | base64 | tr -d "\n"
```

`csr.yaml`
``` yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: myuser-csr
spec:
  usages:
  - client auth
  signerName: kubernetes.io/kube-apiserver-client
  request: LS0tLS1CRUdJTiB
```

``` bash
kubectl create -f csr.yaml
```

``` bash
kubectl get csr
```

상태 : Pending
``` bash
kubectl certificate approve myuser-csr
```

``` bash
kubectl get csr
```

상태 : Approved, Issued
``` bash
kubectl get csr myuser-csr -o yaml
```

status.certificates
``` bash
kubectl get csr myuser-csr -o jsonpath='{.status.certificate}' | base64 -d > myuser.crt
```

Kubeconfig 사용자 생성

``` bash
kubectl config set-credentials myuser --client-certificate=myuser.crt --client-key=myuser.key --embed-certs=true
```

Kubeconfig 컨텍스트 생성
``` bash
kubectl config set-context myuser@cluster.local --cluster=cluster.local --user=myuser --namespace=default
```

``` bash
kubectl config get-users
kubectl config get-clusters
kubectl config get-contexts
```

``` bash
kubectl config use-context myuser@cluster.local
```

클러스터 롤 바인딩 생성
``` yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: myuser-view-crb
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: view
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: myuser
```

`nfs-subdir-external-provisioner/deploy/rbac.yaml`
``` yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nfs-client-provisioner # SA 계정 생성
  # replace with namespace where provisioner is deployed
  namespace: default
---
kind: ClusterRole # 클러스터 전체의 역할
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nfs-client-provisioner-runner
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list", "watch"]
    # nfs 파드는 다른 노드의 정보를 볼 수 있어야 한다.
    # 해당되는 노드의 어떤 파드에 어떤 pv를 만들어 줄 것인지를 결정할 수 있다.
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    verbs: ["get", "list", "watch", "create", "delete"]
    # nfs가 pv를 만들어주기 때문
  - apiGroups: [""]
    resources: ["persistentvolumeclaims"]
    verbs: ["get", "list", "watch", "update"]
     # pvc는 우리가 만들지만 pv를 만들어서 pv와 pvc를 연결시켜줘야 하는데 pvc에는 pv에 대한 정보가 있어야 하고 pvc에서 pv에 대한 정보를 업데이트 할 수 있어야 한다.
     # pv는 pvc를 가리켜야 한다. pv에 이름을 지정하거나 셀렉터로 지정하거나 결과적으로 pv를 셀렉팅할 수 있어야 하기 때문에 pvc를 업데이트할 수 있어야 한다.    
  - apiGroups: ["storage.k8s.io"]
    resources: ["storageclasses"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["create", "update", "patch"]
    # describe 명령을 통해 보는 각 리소스마다의 Events 값을 만들고, 업데이트하고, 변경할 수 있어야 한다.
---
kind: ClusterRoleBinding # ClusterRole과 sa 계정을 연결
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: run-nfs-client-provisioner
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    # replace with namespace where provisioner is deployed
    namespace: default
roleRef:
  kind: ClusterRole
  name: nfs-client-provisioner-runner
  apiGroup: rbac.authorization.k8s.io
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-client-provisioner
  # replace with namespace where provisioner is deployed
  namespace: default
rules:
  - apiGroups: [""]
    resources: ["endpoints"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-client-provisioner
  # replace with namespace where provisioner is deployed
  namespace: default
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    # replace with namespace where provisioner is deployed
    namespace: default
roleRef:
  kind: Role
  name: leader-locking-nfs-client-provisioner
  apiGroup: rbac.authorization.k8s.io
```