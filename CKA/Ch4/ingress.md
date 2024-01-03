# Ingress

## 문제

`Ingress 구성`

```
◾ 작업 클러스터 : k8s
- ingress-nginx namespace에 nginx이미지를 app=nginx 레이블을 가지고 실행하는 nginx pod를 구성하세요.
- 현재 appjs-servic와 nginx 서비스는 이미 동작 중입니다. 별도 구성이 필요 없습니다.
- app-ingress.yaml 파일을 생성하고, 다음 조건의 ingress 를 구성하세요.
- name: app-ingress
- NODE_PORT:30080/ 접속했을 때 nginx 서비스로 연결
- NODE_PORT:30080/app 접속했을 때 appjs-service 서비스로 연결
- Ingress 구성에 다음의 annotations을 포함시키세요.
  annotations:
    kubernetes.io/ingress.class: nginx
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx
            port:
              number: 80
      - path: /app
        pathType: Prefix
        backend:
          service:
            name: appjs-service
            port:
              number: 80
```