# Pod

## 문제

`Pod 생성하기`

```
◾ 작업 클러스터 : k8s
'cka-exam'이라는 namespace를 만들고, 'cka-exam' namespace에 아래와 같은 Pod를 생성하시오.
- pod Name: pod-01
- image: busybox
- 환경변수 : CERT = "CKA-cert"
- command: /bin/sh
- args: -c "while true; do echo $(CERT); sleep 10;done"
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-01
  namespace: cka-exam
spec:
  containers:
  - name: pod-01
    image: busybox
    env:
    - name: CERT
      value: "CKA-cert"
    command: ["/bin/sh"]
    args: ["-c", "while true; do echo $(CERT); sleep 10; done"]
```

## 문제

`Pod의 로그 확인해서 결과 추출하기`

```
◾ 작업 클러스터 : hk8s
Pod "custom-app"의 log를 모니터링하고 'file not found'메세지를 포함하는 로그 라인인 추출하세요.
추출된 결과는 /opt/REPORT/2022/custom-app-log에 기록하세요.
```

## Static Pod

- API 서버 없이 특정 노드에 있는 kubelet에 의해 직접 관리
- `/etc/kubernetes/manifests` 디렉토리에 `yaml` 파일 작성 시 적용됨
- static pod 디렉토리 구성

  cat /var/lib/kubelet/config.yaml

  staticPodPath: /etc/kubernetes/manifests

- 디렉토리 수정 시 kubelet 데몬 재실행

  systemctl restart kubelet

> staticPodPath에 Pod에 해당하는 yaml을 저장하면 kubelet이 파일을 인식해서 컨테이너 Pod를 동작시켜주는 형태

## 문제

`static pod 생성하기`

```
hk8s-w1 노드에 nginx-static-pod.yaml 라는 이름의 Static Pod를 생성하세요.
- pod name: nginx-static-pod
- image: nginx
- port : 80
```

1. hk8s-worker1 노드 내 접속하여 sudo 권한으로 작성

`/var/lib/kubelet/config.yaml` 파일 내 staticPodPath를 확인 가능

2. staticPodPath 내 yaml 작성

`/etc/kubernetes/manifests/nginx-static-pod.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-static-pod
spec:
  containers:
  - name: nginx-static-pod
    image: nginx
    ports:
    - containerPort: 80
```

## 문제

`multi container Pod 생성하기`

```
◾ 작업 클러스터 : k8s
4개의 컨테이너를 동작시키는 eshop-frontend Pod를 생성하시오.
- pod image: nginx, redis, memcached, consul
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: eshop-frontend
spec:
  containers:
  - name: nginx
    image: nginx
  - name: redis
    image: redis
  - name: memcached
    image: memcached
  - name: consul
    image: consul
```

## 문제

`sidecar container Pod 생성하기`
```
◾ 작업 클러스터 : k8s
현재 운영중인 eshop-cart-app Pod의 로그를 Kubernetes built-in logging 아키텍처(예: kubectl logs)에
통합하는 로그 스트리밍 사이드카 컨테이너를 운영하시오.
- busybox 이미지를 사용하여 price라는 이름의 사이드카 컨테이너를 기존 eshop-cart-app에 추가합니다.
- 새 price 컨테이너는 다음과 같은 command를 실행해야 합니다.
Command: /bin/sh, -c, “tail -n+1 -f /var/log/cart-app.log”
- /var/log에 마운트 된 볼륨을 사용하여 사이드카 컨테이너에서 로그 파일 cart-app.log를 사용해야 합니다.
- eshop-cart-app Pod와 cart-app 컨테이너를 수정하지 마시오.
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: eshop-cart-app
spec:
  containers:
  - name: cart-app
    image: busybox
    imagePullPolicy: Always
    command:
    - /bin/sh
    - -c
    - 'i=1;while :;do  echo -e "$i: Price: $((RANDOM % 10000 + 1))" >> /var/log/cart-app.log; i=$((i+1)); sleep 2; done'
    volumeMounts:
    - name: varlog
      mountPath: /var/log

  - name: price
    image: busybox
    args: [/bin/sh, -c, 'tail -n+1 -f /var/log/cart-app.log']
    volumeMounts:
    - name: varlog
      mountPath: /var/log

  volumes:
  - emptyDir: {}
    name: varlog
```