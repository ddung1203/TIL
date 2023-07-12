# ConfigMap & Secret

ConfigMap이나 Secret을 사용하면 애플리케이션과 설정값/구성값을 별도로 분리해 관리할 수 있다. ConfigMap 객체에 저장된 데이터는 볼륨에서 참조할 수 있다. 그런 다음 파일과 디렉토리로 구성된 트리처럼 애플리케이션에서 데이터를 사용할 수 있다.

ConfigMap은 DB의 IP, API를 호출하기 위한 API KEY, 개발/운영에 따른 디버그 모드, 환경 설정과 같은 설정값을,

Secret에는 보안이 중요한 패스워드나, API KEY, 인증서 파일 등 노출되어서는 안 되는 비밀값을 저장할 수 있다.

## 환경변수

`pods.spec.containers.env`

- name
- value

```yaml
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

ConfigMap은 Key/Value 형식으로 저장이 되며, 값을 Pod로 넘기는 방법은 크게 두 가지가 있다.

- 환경 변수
- 볼륨/파일 마운트
  - 설정파일
  - 암호화 키/인증서

### 환경변수

`mymessage.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mymessage
data:
  MESSAGE: Customized Hello ConfigMap
```

또는 `kubectl create configmap mymessage --from-literal=MESSAGE='Customized Hello ConfigMap'`

`myweb-env.yaml`

```yaml
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

```yaml
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

예를 들어, node의 경우 하기와 같다.

```java
var os = require('os');
var http = require('http');
var handleRequest = function(request, response) {

  response.writeHead(200);
  response.end(" my prefered language is "+process.env.LANGUAGE+ "\n");

  //log
  console.log("["+
		Date(Date.now()).toLocaleString()+
		"] "+os.hostname());
}

var www = http.createServer(handleRequest);
www.listen(8080);
```

### 환경변수로 값을 전달

```yaml
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
            name: cm-file
            key: profile.properties
```

cm-file configMap에서 키가 `profile.properties`인 값을 읽어와서 환경 변수 PROFILE에 저장한다. 저장된 값은 파일의 내용인 아래 문자열이 된다.

```
myname=Joongseok Jeon
email=jeonjungseok1203@gmail.com
address=seoul
```

profile.properties 파일안에 문자열이 Key/Value 형식으로 되어 있다고 하더라도, 개개별 문자열을 Key/Value로 인식하는 것이 아니라 전체 파일 내용을 하나의 문자열로 처리한다.

### 디스크 볼륨으로 마운트

`myweb-cm-vol.yaml`

```yaml
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

### Using a ConfigMap in Pod commands

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod
spec:
  containers:
    - name: demo-container
      image: k8s.gcr.io/busybox
      command: ["/bin/sh", "-c", "echo $(VARIABLE_DEMO)"]
      env:
        - name: VARIABLE_DEMO
          valueFrom:
            configMapKeyRef:
              name: demo
              key: lab.difficulty
```

### Using a ConfigMap by creating a Volume

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod
spec:
  containers:
    - name: demo-container
      image: k8s.gcr.io/busybox
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
    volumes:
    - name: config-volume
      configMap:
        name: demo
```

상기와 같은 경우 ConfigMap의 모든 데이터는 ConfigMap 볼륨에 파일로 저장되며, 이 볼륨은 mountPath 디렉터리를 사용해 컨테이너에 마운트된다. 또한 kubelet은 Pod 내부의 볼륨으로 마운트된 ConfigMap의 값을 초~분 단위로 새로고침한다. Secret 또한 위의 메커니즘을 따른다.

## Secret

Secret은 암호, 토큰 또는 키와 같은 소량의 중요한 데이터를 포함하는 오브젝트이다. 이를 사용하지 않으면 중요한 정보가 파드 명세나 컨테이너 이미지에 포함될 수 있다. Secret을 사용한다는 것은 사용자의 기밀 데이터를 애플리케이션 코드에 넣을 필요가 없음을 뜻한다.

Secret은 Secret을 사용하는 파드와 독립적으로 생성될 수 있기 때문에, 파드를 생성하고, 확인하고, 수정하는 워크플로우 동안 Secret(그리고 데이터)이 노출되는 것에 대한 위험을 경감시킬 수 있다. 쿠버네티스 및 클러스터에서 실행되는 애플리케이션은 비밀 데이터를 비휘발성 저장소에 쓰는 것을 피하는 것과 같이, Secret에 대해 추가 예방 조치를 취할 수도 있다.

Secret은 ConfigMap과 유사하지만 특별히 기밀 데이터를 보관하기 위한 것이다. 또한 메모리 내 파일 시스템으로 Secret을 백업하여 비휘발성 스토리지에 기록되지 않도록 한다.

> k8s secret은 기본적으로 API 서버의 etcd에 암호화되지 않은 상태로 저장된다. API access 권한이 있는 모든 사용자 또는 etcd에 접근할 수 있는 모든 사용자는 Secret을 조회하거나 수정할 수 있다. 또한 네임스페이스에서 파드를 생성할 권한이 있는 사람은 누구나 해당 접근을 사용하여 해당 네임스페이스의 모든 Secret을 읽을 수 있다. 여기에는 디플로이먼트 생성 기능과 같은 간접 접근이 포함된다.

value - base64 -> encoded data

> Secret에 저장되는 내용은 패스워드와 같은 단순 문자열의 경우에는 바로 저장이 가능하지만, SSL 인증서와 같은 바이너리 파일의 경우에는 문자열로 저장이 불가능하다. 따라서 이러한 바이너리 파일 저장을 지원하기 위해서 Secret의 경우에는 저장되는 값을 base64로 인코딩을 하여 저장하도록 되어있다.

> Hashicorp Vault AWS KMS ...

### 환경변수

> Opaque: '불투명한'이라는 뜻으로, 일반적으로 내부의 데이터를 들여다 볼 수 없는 데이터를 지칭

**Secret Type**

| 빌트인 타입                         | 사용처                               |
| ----------------------------------- | ------------------------------------ |
| Opaque                              | 임의의 서비스 정의 데이터            |
| kubernetes.io/service-account-token | 서비스 어카운트 토큰                 |
| kubernetes.io/dockercfg             | 직렬화 된 ~/.dockercfg 파일          |
| kubernetes.io/dockerconfigjson      | 직렬화 된 ~/.docker/config.json 파일 |
| kubernetes.io/basic-auth            | 기본 인증을 위한 자격 증명           |
| kubernetes.io/ssh-auth              | SSH를 위한 자격 증명                 |
| kubernetes.io/tls                   | TLS 클라이언트나 서버를 위한 데이터  |
| bootstrap.kubernetes.io/token       | 부트스트랩 토큰 데이터               |

`mydata.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mydata
type: Opaque
data:
  id: YWRtaW4K # admin을 base64로 인코딩
  pwd: UEBzc3cwcmQK # P@ssw0rd를 base64로 인코딩
```

상기 `secret`은 민감한 데이터를 저장하기 위해 만든 것이지만 인코딩만 할 뿐 암호화를 하지 않아 안전하지 않다.

```bash
 vagrant@k8s-node1 > ~/volume > echo "YWRtaW4K" | base64 -d
admin
```

이 경우 AWS의 KMS와 연동해서 암호화할 수 있으며(클라우드 서비스), vault로 base64를 연동해서 암호화할 수 있다(on-prem).

```yaml
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

```yaml
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

```yaml
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

```bash
kubectl create secret generic registry-auth \
--from-file=.dockerconfigjson=/home/vagrant/.docker/config.json \
--type=kubernetes.io/dockerconfigjson
```

또는 시크릿을 생성하는 명령어에서 직접 로그인 인증 정보를 명시할 수도 있다.

```bash
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

```bash
mkdir x509 && cd x509
```

Private Key 생성

```bash
openssl genrsa -out nginx-tls.key 2048
```

Private Key를 이용한 Public Key 생성

```bash
openssl rsa -in nginx-tls.key -pubout -out nginx-tls
```

CSR

> SSL 서버를 운영하는 회사의 정보를 암호화하여 인증 기관으로 보내 인증서를 발급받게 하는 일종의 신청서

```bash
openssl req -new -key nginx-tls.key -out nginx-tls.csr
```

인증서 자체 서명

```bash
openssl req -x509 -days 3650 -key nginx-tls.key -in nginx-tls.csr -out nginx-tls.crt
```

```bash
rm nginx-tls nginx-tls.csr
```

- nginx-tls.key
- nginx-tls.crt

#### 설정파일

ConfigMap

```bash
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

```yaml
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

```yaml
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

```yaml
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

```yaml
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

```bash
curl -k https://192.168.100.X
```

### TLS/SSL Termination with Ingress

종단간 암호화 방식은 클라이언트부터 서버까지 모든 통신 구간에 암호화를 하는 방식이다.
TLS/SSL Termination 방식은 Loadbalancer가 존재하며 노출되어 있다.

클라이언트와 LB 사이에는 HTTPS를 사용하며 LB와 실제 서비스를 제공하는 서버 사이에는 HTTP를 사용한다.

이점

- 인증서 관리 용이
- 개별 서버들이 암/복호화를 하지 않아 리소스 사용량이 낮아짐
- 여러 보안 장치를 비암호화 구간에 구성할 수 있음

Ingress의 장점 중 하나는 Kubernetes 뒤쪽에 있는 Deployment와 Service가 아닌, 앞쪽에 있는 Ingress Controller에서 편하게 SSL/TLS 보안 연결을 설정할 수 있다는 것이다. 즉, Ingress Controller 지점에서 인증서를 적용해 두면 요청이 전달되는 애플리케이션에 대해 모두 인증서 처리를 할 수 있다. 따라서 Ingress Controller가 보안 연결을 수립하기 위한 일종의 Gateway 역할을 한다고도 볼 수 있다.

`ingress-tls-secret.yaml`

```yaml
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

```yaml
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

```yaml
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

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myweb-ing-tls
spec:
  tls:
    - hosts:
        - "*.nip.io"
      secretName: ingress-tls-secret
  rules:
    - host: "*.nip.io"
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

```bash
curl -k https://192-168-100-100.nip.io
```

## Private Registry에서 Image 받아오기

Kubernetes에 Private Docker Registry에 접속하여 이미지 Pull할 수 있도록 Secret 설정

### Dockerconfig 생성

docker login을 하여 로그인 정보인 config.json을 생성한다.

```json
{
  "auths": {
    "https://index.docker.io/v1/": {
      "auth": ""
    }
  }
}
```

Docker 인증을 기반으로 Kubernetes Secret 생성

```bash
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=~/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson
```

검증

```bash
kubectl get secret regcred --output=yaml
```

결과는 다음과 같다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  ...
  name: regcred
  ...
data:
  .dockerconfigjson: eyJodHRwczovL2luZGV4L ... J0QUl6RTIifX0=
type: kubernetes.io/dockerconfigjson
```

`.dockerconfigjson` 필드의 값은 base64 인코딩의 결과이며, decode 시 `config.json`을 확인할 수 있다.

### Secret을 사용하는 Pod 생성

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: realmytrip
  labels:
    name: realmytrip
spec:
  containers:
    - name: realmytrip
      image: ddung1203/realmytrip:latest
      ports:
        - containerPort: 3000
  imagePullSecrets:
    - name: regcred
```
