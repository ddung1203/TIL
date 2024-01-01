# Deployment

`Deployment & Scaling`
```
◾ 작업 클러스터 : k8s
a. webserver 라는 이름으로 deployment를 생성하시오.
- Name: webserver 
- 2 replicas 
- label: app_env_stage=dev
- container name: webserver 
- container image: nginx:1.14
b. 다음, webserver Deployment의 pod 수를 3개로 확장하시오.
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webserver
  labels:
    app_env_stage: dev
spec:
  replicas: 2
  selector:
    matchLabels:
      app_env_stage: dev
  template:
    metadata:
      labels:
        app_env_stage: dev
    spec:
      containers:
      - name: webserver
        image: nginx:1.14
        ports:
        - containerPort: 80
```

```bash
kubectl scale deployment webserver --replicas=3
```

## 문제

`Rolling update & Roll back`

```
◾ 작업 클러스터 : k8s
Deployment를 이용해 nginx 파드를 3개 배포한 다음 컨테이너 이미지 버전을 rolling update하고 update record를 기록합니다. 마지막으로 컨테이너 이미지를 previous version으로 roll back 합니다.
- name: eshop-payment
- Image : nginx
- Image version: 1.16
- update image version: 1.17
- label: app=payment, environment=production
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eshop-payment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment
      environment: production
  template:
    metadata:
      labels:
        app: payment
        environment: production
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
```

```bash
kubectl apply -f 3-4.yaml --record
```

```bash
kubectl set image deployment eshop-payment nginx=nginx:1.17 --record
kubectl rollout undo deployment eshop-payment
```

> `nginx`는 컨테이너의 이름

> 검증
> 
> `kubectl rollout history deployment eshop-payment`