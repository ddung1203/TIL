# ConfigMap & Secret

ConfigMap이나 Secret을 사용하면 애플리케이션과 설정값을 별도로 분리해 관리할 수 있다. 

ConfigMap은 설정값을, Secret에는 노출되어서는 안 되는 비밀값을 저장할 수 있다.


## 환경변수
`pods.spec.containers.env`

- name
- value

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-env
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb:alpine
      env:
        - name: MESSAGE
          value: "Customized Hello World"
```

## ConfigMap
사용 용도

ConfigMap은 일반적인 설정값을 담아 저장할 수 있는 k8s 오브젝트이며, 네임스페이스에 속하기 때문에 네임스페이스별로 ConfigMap이 존재한다.


- 환경 변수
- 볼륨/파일
    - 설정파일
    - 암호화 키/인증서

### 환경변수
`mymessage.yaml`

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mymessage
data:
  MESSAGE: Customized Hello ConfigMap
```

`myweb-env.yaml`

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-env
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb:alpine
      envFrom:
        - configMapRef:
            name: mymessage
```

valueFrom과 configMapKeyReg를 사용하여 여러 키:값 쌍이 들어있는 ConfigMap에서 특정 데이터만을 선택해 환경 변수로 가져올 수 있다.

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-env
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb:alpine
      env:
        valueFrom:
          configMapKeyRef:
            name: mymessage
            key: MESSAGE
```

### 파일
`myweb-cm-vol.yaml`

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-cm-vol
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb:alpine
      volumeMounts:
        - name: cmvol
          mountPath: /myvol
  volumes:
    - name: cmvol
      configMap:
        name: mymessage
```

## Secret

시크릿은 암호, 토큰 또는 키와 같은 소량의 중요한 데이터를 포함하는 오브젝트이다. 이를 사용하지 않으면 중요한 정보가 파드 명세나 컨테이너 이미지에 포함될 수 있다. 시크릿을 사용한다는 것은 사용자의 기밀 데이터를 애플리케이션 코드에 넣을 필요가 없음을 뜻한다.

시크릿은 시크릿을 사용하는 파드와 독립적으로 생성될 수 있기 때문에, 파드를 생성하고, 확인하고, 수정하는 워크플로우 동안 시크릿(그리고 데이터)이 노출되는 것에 대한 위험을 경감시킬 수 있다. 쿠버네티스 및 클러스터에서 실행되는 애플리케이션은 비밀 데이터를 비휘발성 저장소에 쓰는 것을 피하는 것과 같이, 시크릿에 대해 추가 예방 조치를 취할 수도 있다.

시크릿은 컨피그맵과 유사하지만 특별히 기밀 데이터를 보관하기 위한 것이다.

> k8s secret은 기본적으로 API 서버의 etcd에 암호화되지 않은 상태로 저장된다. API access 권한이 있는 모든 사용자 또는 etcd에 접근할 수 있는 모든 사용자는 시크릿을 조회하거나 수정할 수 있다. 또한 네임스페이스에서 파드를 생성할 권한이 있는 사람은 누구나 해당 접근을 사용하여 해당 네임스페이스의 모든 시크릿을 읽을 수 있다. 여기에는 디플로이먼트 생성 기능과 같은 간접 접근이 포함된다.



value - base64 -> encoded data

> Hashicorp Vault AWS KMS ...

### 환경변수

> Opaque: '불투명한'이라는 뜻으로, 일반적으로 내부의 데이터를 들여다 볼 수 없는 데이터를 지칭

`mydata.yaml`

``` yaml
apiVersion: v1
kind: Secret
metadata:
  name: mydata
type: Opaque
data:
  id: YWRtaW4K
  pwd: UEBzc3cwcmQK
```

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-secret
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb:alpine
      envFrom:
        - secretRef:
            name: mydata
```

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-env
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb:alpine
      env:
        valueFrom:
          secretKeyRef:
            name: mydata
            key: id
```

### 파일
``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-sec-vol
spec:
  containers:
    - name: myweb
      image: ghcr.io/c1t1d0s7/go-myweb:alpine
      volumeMounts:
        - name: secvol
          mountPath: /secvol
  volumes:
    - name: secvol
      secret:
        secretName: mydata
```

## 이미지 레지스트리 접근을 위한 docker-registry 타입의 시크릿 사용하기

private registry, docker hub, GCR, ECR 등의 클라우드 레지스트리를 사용하고 있다면 로그인 등과 같은 인증 절차가 필요하다.

`docker login` 명령어로 로그인에 성공했을 때 도커 엔진이 자동으로 생성하는 `~/.docker/config.json` 파일을 그대로 사용하는 것이다. `config.json` 파일에는 인증을 위한 정보가 담겨 있기 때문에 이를 그대로 시크릿으로 가져오면 된다.

``` bash
kubectl create secret generic registry-auth \
--from-file=.dockerconfigjson=/home/vagrant/.docker/config.json \
--type=kubernetes.io/dockerconfigjson
```

또는 시크릿을 생성하는 명령어에서 직접 로그인 인증 정보를 명시할 수도 있다.

``` bash
kubectl create secret docker-registry registry-auth-by-cmd \
--docker-username=ddung1203 \
--docker-password=PASSWORD
```

`--docker-server` 옵션을 사용하지 않으면 기본적으로 docker.io를 사용하도록 설정되지만, 다른 사설 레지스트리를 사용하려면 도메인을 입력하면 된다.

## TSL 키를 저장할 수 있는 TLS 타입의 시크릿 사용하기

Pod 내부의 애플리케이션이 보안 연결을 위해 인증서나 비밀키 등을 가져와야 할 때 시크릿의 값을 Pod에 제공하는 방식으로 사용할 수 있다.


### Nginx HTTPS 서버

Nginx
- Documentation Root : /usr/share/nginx/html/
- Configuration File : /etc/nginx/conf.d

#### 자체 서명 인증서 생성

Secret:
- Type: `kubernetes.io/tls`

``` bash
mkdir x509 && cd x509
```

Private Key 생성
``` bash
openssl genrsa -out nginx-tls.key 2048
```

Private Key를 이용한 Public Key 생성
``` bash
openssl rsa -in nginx-tls.key -pubout -out nginx-tls
```

CSR

> SSL 서버를 운영하는 회사의 정보를 암호화하여 인증 기관으로 보내 인증서를 발급받게 하는 일종의 신청서

``` bash
openssl req -new -key nginx-tls.key -out nginx-tls.csr
```

인증서 자체 서명
``` bash
openssl req -x509 -days 3650 -key nginx-tls.key -in nginx-tls.csr -out nginx-tls.crt
```

``` bash
rm nginx-tls nginx-tls.csr
```

- nginx-tls.key
- nginx-tls.crt

#### 설정파일
ConfigMap

``` bash
mkdir conf && cd conf
```

`nginx-tls.conf`
```
server {
    listen              80;
    listen              443 ssl;
    server_name         myapp.example.com;
    ssl_certificate     /etc/nginx/ssl/tls.crt;
    ssl_certificate_key /etc/nginx/ssl/tls.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    location / {
        root   /usr/share/nginx/html;
        index  index.html;
    }
}
```

#### 리소스 생성
ConfigMap 생성

`nginx-tls-config.yaml`

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-tls-config
data:
  nginx-tls.conf: |
    server {
      listen              80;
      listen              443 ssl;
      server_name         myapp.example.com;
      ssl_certificate     /etc/nginx/ssl/tls.crt;
      ssl_certificate_key /etc/nginx/ssl/tls.key;
      ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
      ssl_ciphers         HIGH:!aNULL:!MD5;
      location / {
        root   /usr/share/nginx/html;
        index  index.html;
      }
    }
```

Secret 생성
`nginx-tls-secret.yaml`
``` yaml
apiVersion: v1
kind: Secret
metadata:
  name: nginx-tls-secret
type: kubernetes.io/tls
data:
  # base64 x509/nginx-tls.crt -w 0 # 인코딩
  tls.crt: |
    LS0tLS1C...
  # base64 x509/nginx-tls.key -w 0 # 인코딩
  tls.key: |
    LS0tLS1C...
```


Pod 생성
`nginx-https-pod.yaml`

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-https-pod
  labels:
    app: nginx
spec:
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
      - name: nginx-config
        mountPath: /etc/nginx/conf.d
      - name: nginx-certs
        mountPath: /etc/nginx/ssl
  volumes:
    - name: nginx-config
      configMap:
        name: nginx-tls-config
    - name: nginx-certs
      secret:
        secretName: nginx-tls-secret
```

SVC 생성
`nginx-svc-lb.yaml`
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc-lb
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - name: http
      port: 80
      targetPort: 80
    - name: https
      port: 443
      targetPort: 443
```

Test

``` bash
curl -k https://192.168.100.X
```

### TLS/SSL Termination with Ingress

`ingress-tls-secret.yaml`
``` yaml
apiVersion: v1
kind: Secret
metadata:
  name: ingress-tls-secret
type: kubernetes.io/tls
data:
  # base64 x509/nginx-tls.crt -w 0
  tls.crt: |
    LS0tLS1CRUd...
  # base64 x509/nginx-tls.key -w 0
  tls.key: |
    LS0tLS1CRUdJ...
```

`myweb-rs.yaml`
``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      env: dev
  template:
    metadata:
      labels:
        app: web
        env: dev
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
          ports:
            - containerPort: 8080
              protocol: TCP
```

`myweb-svc-np.yaml`
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-np
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

`myweb-ing-tls.yaml`
``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myweb-ing-tls
spec:
  tls:
    - hosts:
        - '*.nip.io'
      secretName: ingress-tls-secret
  rules:
    - host: '*.nip.io'
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myweb-svc-np
                port:
                  number: 80
```

``` bash
curl -k https://192-168-100-100.nip.io
```
