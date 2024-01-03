# ClusterIP

## 문제

`ClusterIP type의 서비스 운영`
```
◾ 작업 클러스터 : k8s
'devops' namespace에서 운영되고 있는 eshop-order deploymen의 Service를 만드세요.
- Service Name: eshop-order-svc
- Type: ClusterIP
- Port: 80
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: eshop-order-svc
  namespace: devops
spec:
  type: ClusterIP
  selector:
    name: order
  ports:
  - port: 80
    targetPort: 80
```

## 문제

`Pod를 이용한 Named Service 구성`

```
◾ 작업 클러스터 : k8s
- 미리 배포한 'front-end'에 기존의 nginx 컨테이너의 포트 '80/tcp'를 expose하는 'http'라는 이름을 추가합니다.
- 컨테이너 포트 http를 expose하는 'front-end-svc'라는 새 service를 만듭니다.
- 또한 준비된 node의 'NodePort'를 통해 개별 Pods를 expose되도록 Service를 구성합니다.
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: front-end
spec:
  replicas: 2
  selector:
    matchLabels:
      run: nginx
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - name: http
          containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: front-end-svc
spec:
  type: NodePort
  selector:
    run: nginx
  ports:
    - port: 80
      targetPort: http
```