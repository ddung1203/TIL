# RBAC : Role Based Access Control

## Kubeconfig

`~/.kube/config`

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

``` bash
kubectl config view
```

``` bash
kubectl config get-clusters
kubectl config get-contexts
kubectl config get-users
```

``` bash
kubectl config use-context myadmin@mycluster
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

#### ClusterRole

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