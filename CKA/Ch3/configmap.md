# ConfigMap

## 문제

`ConfigMap으로 환경변수 전달`

```
◾ 작업 클러스터 : k8s
다음의 변수를 configMap eshop으로 등록하세요.
- DBNAME: mysql
- USER: admin
등록한 eshop configMap의 DBNAME을 eshop-configmap라는 이름의 nginx 컨테이너에 DB라는 환경변수로 할당하세요
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: eshop
data:
  DBNAME: mysql
  USER: admin
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: eshop-configmap
spec:
  containers:
  - name: eshop-configmap
    image: nginx
    env:
      # 환경변수 정의
      - name: DB
        valueFrom:
          configMapKeyRef:
            # ConfigMap 이름
            name: eshop
            # value와 연관된 key
            key: DBNAME
```