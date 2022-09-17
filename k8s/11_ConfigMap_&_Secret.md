# ConfigMap & Secret

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

value - base64 -> encoded data

> Hashicorp Vault AWS KMS ...

### 환경변수

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
      image: ghcr.io/c1t1d0s7/go-myweb-alpine
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

## Nginx HTTPS 서버

Nginx
- Documentation Root : /usr/share/nginx/html/
- Configuration File : /etc/nginx/conf.d

#### 자체 서명 인증서 생성

Secret:
- Type: `kubernetes.io/tls`

``` bash
mkdir x509 && cd x509
```

Private Key
``` bash
openssl genrsa -out nginx-tls.key 2048
```

Public Key
``` bash
openssl rsa -in nginx-tls.key -pubout -out nginx-tls
```

CSR
``` bash
openssl req -new -key -out nginx-tls.csr
```

인증서
``` bash
openssl req -x509 -days 3650 -key nginx-tls.key -in nginx-tls.csr -out nginx-tls.crt
```

``` bash
rm nginx-tls nginx-tls.csr
```

- nginx-tls.key
- nginx-tls.crt

#### 설정차일
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
CM 생성

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
  # base64 x509/nginx-tls.crt -w 0
  tls.crt: |
    LS0tLS1C...
  # base64 x509/nginx-tls.key -w 0
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