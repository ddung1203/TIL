# CRD - 사용자 지정 리소스 정의

Kubernetes는 매우 확장 가능한 플랫폼이다. 쿠버네티스 API에 자체 리소스를 추가하고 그들을 관리하려고 kubectl 지원을 포함한 API 머신의 모든 이점을 누릴 수 있다. 가장 먼저 해야 할 일은 CRD를 정의하는 것이다. 정의는 쿠버네티스 API의 엔드포인트, 버전, 범위, 종류, 새 유형의 리소스와 상호작용하는 데 사용되는 이름을 지정한다.

## SUPERHERO CRD

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  # name은 spec 필드와 일치해야 하며, <plural>.<group> 형식이어야 함
  name: superheros.example.org
spec:
  # REST API에 사용할 그룹 이름: /apis/<group>/<version>
  group: example.org
  # CRD에서 지원되는 버전 목록
  versions:
    - name: v1
      # 각 버전은 served 플래그로 활성화/비활성화 가능
      served: true
      # 하나의 버전만 스토리지 버전으로 표시해야 함
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                size:
                  type: string
                superpower:
                  type: string
                color:
                  type: string
  # Namespace 혹은 Cluster
  scope: Cluster
  names:
    # URL에서 사용될 이름: /apis/<group>/<version>/<plural>
    plural: superheros
    # CLI에서 별명으로 사용하고 표시할 이름
    singular: superhero
    # 일반적으로 CamelCased 단수 유형. 리소스 매니페스트가 이것을 사용함
    kind: SuperHero
    # CLI의 리소스와 일치하는 짧은 문자열
    shortNames:
    - hr
```

모든 네임스페이스에서 CRD를 사용할 수 있다. 범위는 사용 가능한 URL을 구성할 때와 네임스페이스에서 모든 객체를 삭제할 때 관련된다.

## SUPERHERO 리소스 생성

```yaml
apiVersion: "example.org/v1"
kind: SuperHero
metadata:
  name: antman
spec:
  superpower: "can shrink"
  size: "tiny"
```

```yaml
apiVersion: "example.org/v1"
kind: SuperHero
metadata:
  name: hulk
spec:
  superpower: "super strong"
  size: "big"
  color: "green"
```

```bash
jeonj@ubuntu > ~ > kubectl get hr             
NAME     AGE
antman   28s
hulk     21s
```

```bash
jeonj@ubuntu > ~ > kubectl get superhero hulk -o yaml
apiVersion: example.org/v1
kind: SuperHero
metadata:
  creationTimestamp: "2023-10-31T04:50:00Z"
  generation: 1
  name: hulk
  resourceVersion: "41682"
  uid: fa4a2f8d-1a5d-4e08-950b-aa085c57be2b
spec:
  color: green
  size: big
  superpower: super strong
```

```bash
jeonj@ubuntu > ~ > kubectl describe superhero hulk
Name:         hulk
Namespace:    
Labels:       <none>
Annotations:  <none>
API Version:  example.org/v1
Kind:         SuperHero
Metadata:
  Creation Timestamp:  2023-10-31T04:50:00Z
  Generation:          1
  Resource Version:    41682
  UID:                 fa4a2f8d-1a5d-4e08-950b-aa085c57be2b
Spec:
  Color:       green
  Size:        big
  Superpower:  super strong
Events:        <none>
```

이제 CLI 지원과 안정적인 Persistent Storage를 갖춘 무료 CRUD API를 제공할 수 있다. 오브젝트 모델을 발명하고 원하는 만큼 사용자 정의 리소스를 생성, 가져오기, 조회, 업데이트, 삭제하기만 하면 된다. 그러나 훨씬 더 나아가 사용자 정의 리소스를 감시하고 필요할 때 조치를 취하는 자신만의 컨트롤러를 가질 수 있다.

## ArgoCD의 CRD

```bash
jeonj@ubuntu > ~ > kubectl get crd              
NAME                          CREATED AT
applications.argoproj.io      2023-10-31T05:03:53Z
applicationsets.argoproj.io   2023-10-31T05:03:53Z
appprojects.argoproj.io       2023-10-31T05:03:53Z
```

클러스터 전체에서 사용자 정의 리소스를 사용할 수 있으므로 네임스페이스 전체에서 공유 구성에 사용할 수 있다. CRD는 동적 구성과 같이, 중앙집중식 원격 구성 서비스 역할을 할 수 있지만 직접 구현할 필요는 없다. 또 다른 옵션은 이러한 CRD를 감시하는 컨트롤러를 생성한 다음 각 네임스페이스에 대한 적절한 컨피그맵에 자동으로 복사하는 것이다.

결론은 구성 관리가 복잡한 시스템의 경우 Kubernetes가 구성을 확장할 수 있는 도구를 제공한다. 