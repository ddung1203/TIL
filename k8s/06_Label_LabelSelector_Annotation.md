# Label & LabelSelector

> https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/labels/
> https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/common-labels/

## Label

레이블 확인

``` bash
kubectl get pods --show-labels
```

레이블 관리

``` bash
kubectl label pods myweb APP=apache
```

``` bash
kubectl label pods myweb ENV=developments
```

``` bash
kubectl label pods myweb ENV=staging --overwrite
```

``` bash
kubectl label pods myweb ENV-
```

## LabelSelector

- **검색**
- 리소스 간 연결

### 일치성(equality base)
- `=`
- `==`
- `!=`

```bash
kubectl get pods -l APP=nginx
kubectl get pods -l APP==nginx
```

```bash
kubectl get pods -l 'APP!=nginx'
```

### 집합성(set base)
- `in`
- `notin`
- `exists`: 키만 매칭
	- `kubectl get pods -l 'APP'`
- `doesnotexists`: 키 제외 매칭
	- `kubectl get pods -l '!APP'`

# Annotations
레이블과 비슷
**비 식별 메타데이타**
애플리케이션이 해당 메타데이터를 참조할 수 있음 -> 애플리케이션 작동 변경

명령형 커맨드
```bash
kubectl annotate pods myweb created-by=Jeon
```

```bash
kubectl annotate pods myweb created-by=Kim --overwrite
```

``` bash
kubectl annotate pods myweb created-by-
```

YAML
``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-label-anno
  labels:
    APP: apache
    ENV: staging
  annotations:
    Created-by: Jeon
spec:
  containers:
    - name: myweb
      image: httpd
      ports:
        - containerPort: 80
          protocol: TCP
```