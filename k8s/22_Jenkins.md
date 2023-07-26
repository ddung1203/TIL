# Jenkins CD

Jenkins는 빌드, 테스트, 파이프라인을 유연하게 조정할 수 있는 오픈소스 자동화 서버이다. Jenkins를 사용하면 개발자는 지속적 배포로 인해 발생할 수 있는 오버헤드 문제에 대한 걱정 없이 프로젝트를 신속하게 변경 및 개선할 수 있다.

## Jenkins Helm 설정

[Helm 참고](https://github.com/ddung1203/DevOps/blob/main/DevOps/Helm.md)

Helm repo 추가

```bash
helm repo add jenkins https://charts.jenkins.io
```

저장소 최신 상태 확인

```bash
helm repo update
```

## Jenkins 구성 및 설치

```bash
helm install cd jenkins/jenkins --wait
```

Jenkins 차트에서는 자동으로 admin password를 만들어 준다.

```bash
printf $(kubectl get secret cd-jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo
```

## Sample 앱 배포

```bash
kubectl apply -f . -n production
```

`backend.yaml`

```yaml
kind: Deployment
apiVersion: apps/v1
metadata:
  name: gceme-backend-production
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gceme
      role: backend
      env: production
  template:
    metadata:
      name: backend
      labels:
        app: gceme
        role: backend
        env: production
    spec:
      containers:
        - name: backend
          image: corelab/gceme:1.0.0
          resources:
            limits:
              memory: "500Mi"
              cpu: "100m"
          imagePullPolicy: Always
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
          command: ["sh", "-c", "app -port=8080"]
          ports:
            - name: backend
              containerPort: 8080
---
kind: Service
apiVersion: v1
metadata:
  name: gceme-backend
spec:
  ports:
    - name: http
      port: 8080
      targetPort: 8080
      protocol: TCP
  selector:
    role: backend
    app: gceme
```

`frontend.yaml`

```yaml
kind: Deployment
apiVersion: apps/v1
metadata:
  name: gceme-frontend-production
spec:
  replicas:
  selector:
    matchLabels:
      app: gceme
      role: frontend
      env: production
  template:
    metadata:
      name: frontend
      labels:
        app: gceme
        role: frontend
        env: production
    spec:
      containers:
        - name: frontend
          image: corelab/gceme:1.0.0
          resources:
            limits:
              memory: "500Mi"
              cpu: "100m"
          imagePullPolicy: Always
          readinessProbe:
            httpGet:
              path: /healthz
              port: 80
          command:
            [
              "sh",
              "-c",
              "app -frontend=true -backend-service=http://gceme-backend:8080 -port=80",
            ]
          ports:
            - name: frontend
              containerPort: 80
---
kind: Service
apiVersion: v1
metadata:
  name: gceme-frontend
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      targetPort: 80
      protocol: TCP
  selector:
    app: gceme
    role: frontend
```

정상적으로 배포 시 서비스의 버전을 확인한다.

```bash
curl http://<EXTERNAL-IP>/version
```
