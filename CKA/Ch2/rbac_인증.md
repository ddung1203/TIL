# RBAC 인증

## API 인증: RBAC

- API 서버에 접근하기 위해서는 인증 작업이 필요하다.
- 사용자의 역할에 따라 리소스에 대한 접근 권한을 가진다.
- User: 클러스터 외부에서 k8s를 조작하는 사용자 인증
- ServiceAccount: Pod가 k8s API를 다룰 떄 사용하는 계정

1. API 요청
2. **Authentication(인증)**
3. Authorization(권한)
4. Admission Control
5. Approval

## Role & RoleBinding

- 특정 유저나 ServiceAccount가 접근하려는 API에 접근 권한을 가짐
- 권한 있는 User 만 접근하도록 허용
- 권한제어
  - Role
    - 어떤 API를 이용할 수 있는지의 정의
    - k8s의 사용 권한을 정의
    - 지정된 NS에서만 유효
  - RoleBinding
    - 사용자/그룹 또는 Service Accout와 role을 연결

1. API 요청
2. Authentication(인증)
3. **Authorization(권한)**
4. Admission Control
5. Approval

## ClusterRole, ClusterRoleBinding

- ClusterRole
  - 어떤 API를 사용할 수 있는지 권한 정의. 전체 클러스터에 적용됨
- ClusterRoleBinding
  - 사용자/그룹 또는 Service Account와 role을 연결

**Role은 특정 NS, ClusterRole은 모든 NS에 적용됨**

## 문제

`ServiceAccount, Role, RoleBinding`
https://kubernetes.io/docs/reference/access-authn-authz/rbac/

```
◾ 작업 클러스터 : k8s
애플리케이션 운영중 특정 namespace의 Pod들을 모니터할수 있는 서비스가 요청되었습니다. api-access 네임스페이스의 모든 pod를 view할 수 있도록 다음의 작업을 진행하시오.

- api-access라는 새로운 namespace에 pod-viewer라는 이름의 Service Account를 만듭니다.
- podreader-role이라는 이름의 Role과 podreader-rolebinding이라는 이름의 RoleBinding을 만듭니다.
- 앞서 생성한 ServiceAccount를 API resource Pod에 대하여 watch, list, get을 허용하도록 매핑하시오.
```

1. NS 생성: api-access

```bash
kubectl create ns api-access
```

2. Service Account: pod-viewer

```bash
kubectl create sa pod-viewer -n api-access
```

3. podreader-role: Pod watch, list, get

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: api-access
  name: podreader-role
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

혹은 

```bash
kubectl create role podreader-role --verb=get --verb=list --verb=watch --resource=pods -n api-access
```

4. rolebinding 생성: podreader-rolebinding podreader-role pod-viewer

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: podreader-rolebinding
  namespace: api-access
subjects:
- kind: ServiceAccount
  name: pod-viewer
  namespace: api-access
roleRef:
  kind: Role
  name: podreader-role
  apiGroup: rbac.authorization.k8s.io
```

혹은

```bash
kubectl create rolebinding podreader-rolebinding --role=podreader-role --serviceaccount=api-access:pod-viewer -n api-access
```

## 문제

`ServiceAccount, ClusterRole, ClusterRoleBinding`
```
◾ 작업 클러스터 : k8s
- 작업 Context에서 애플리케이션 배포를 위해 새로운 ClusterRole을 생성하고 특정 namespace의 ServiceAccount를 바인드하시오.
- 다음의 resource type에서만 Create가 허용된 ClusterRole deployment-clusterrole을 생성합니다.
  - Resource Type: Deployment StatefulSet DaemonSet
- 미리 생성된 namespace api-access 에 cicd-token이라는 새로운 ServiceAccount를 만듭니다.
- ClusterRole deployment-clusterrole을 namespace api-access 로 제한된 새 ServiceAccount cicd-token에 바인딩하는 합니다.
```

> NS와 상관없이 k8s 클러스터 안에 있는 모든 NS에 대해 Pod에 리스트 액세스가 가능

1. ClusterRole 생성: deployment-clusterrole: Deployment, StatefuleSet, Daemonset - Create

```bash
kubectl create clusterrole deployment-clusterrole --verb=create --resource=deployment,statefulset,daemonset
```

2. ServiceAccount: cicd-token, -n api-access

```bash
kubectl create sa cicd-token -n api-access
```

3. ClusterroleBinding: deployment-clusterrolebinding, deployment-clusterrole api-access:cicd-token

```bash
kubectl create clusterrolebinding deployment-clusterrolebinding --clusterrole=deployment-clusterrole --serviceaccount=api-access:cicd-token
```

## 문제

`User, ClusterRole, ClusterRoleBinding`
```
◾ 작업 클러스터 : k8s
CSR(Certificate Signing Request)를 통해 app-manager 인증서를 발급받은 user app-manager 에게 cluster내 모든 namespace의 deployment, pod, service 리소스를 create, list, get, update, delete 할 수 있는 권한을 할당하시오.
- user name : app-manager
- certificate name: app-manager
- clusterRole name : app-access
- clusterRoleBinding name: app-access-binding
```

1. user: app-manager
1-1. 인증서(보통 제공됨)

```bash
openssl genrsa -out app-manager.key 2048
openssl req -new -key app-manager.key -out app-manager.csr -subj "/CN=app-manager"
```

```bash
cat app-manager.csr | base64 | tr -d "\n"
```

`app-manager.yaml`
```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: app-manater
spec:
  request: <base64 인코딩된 파일>
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
```

```bash
kubectl apply -f app-manager.yaml
```

```bash
kubectl certificate approve app-manager
```

1-2. (검증) app-manager.crt 인증서를 사용하는 user app-manager 등록
```bash
kubectl get csr app-manager -o jsonpath='{.status.certificate}'| base64 -d > app-manager.crt
```

2. clusterrole: app-access

```bash
kubectl create clusterrole app-access --verb=create,list,get,update,delete --resource=deployment,pod,service
```


3. clusterrolebinding: app-access-binding

```bash
kubectl create clusterrolebinding app-access-binding --clusterrole=app-access --user=app-manager
```

4. (검증) Add to kubeconfig - app-manager context-switch

```bash
kubectl config set-credentials app-manager --client-key=app-manager.key --client-certificate=app-manager.crt --embed-certs=true
```

```bash
kubectl config set-context app-manager --cluster=kubernetes --user=app-manager
```