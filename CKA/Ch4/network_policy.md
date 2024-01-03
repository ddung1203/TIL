# Network Policy

- k8s가 지원하는 Pod 통신 접근 제한
- 방화벽으로, Pod로 inbound, outbound를 설정하는 정책
- 트래픽 컨트롤 정의
  - ipBlock
  - podSelector
  - namespaceSelector
  Protocol & Port

## 문제

`Network Policy`

```
작업 클러스터 : hk8s
- default namespace에 다음과 같은 pod를 생성하세요.
- name: poc
- image: nginx
- port: 80
- label: app=poc
- "partition=customera"를 사용하는 namespace에서만 poc의
80포트로 연결할 수 있도록 default namespace에 'allow-webfrom-customera'라는 network Policy를 설정하세요. 보안 정책상 다른 namespace의 접근은 제한합니다.
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: poc
  labels:
    app: poc
spec:
  containers:
  - name: poc
    image: nginx
    ports:
    - containerPort: 80
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-webfrom-customera
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: poc
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              partition: customera
      ports:
        - protocol: TCP
          port: 80
```