# Service & DNS & Ingress
## Service - ClusterIP

ClusterIP는 클러스터 내부에서 사용하는 프록시 서비스이다.

ClusterIP에 요청을 보내면 여러 개의 Pod 중 하나로 자동으로 요청이 간다.

ClusterIP를 사용하는 이유는 Pod의 IP는 동적이기 때문이다. 따라서 Pod의 IP와는 상관없이 액세스할 수 있도록 하는 고유 IP를 가진 Service가 필요한 것이다.

`myweb-svc.yaml`
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc
spec:
  selector: # 파드 셀렉터
    app: web
  ports:
    - port: 80 # 서비스 포트
    targetPort: 8080 # 타겟(파드 포트)
```

``` bash
kubectl create -f .
```

``` bash
kubectl get svc myweb-svc
```

``` bash
kubectl describe svc myweb-svc
```

``` bash
kubectl get endpoint myweb-svc
```

``` bash
kubectl run nettool -it --image ghcr.io/c1t1d0s7/network-multitool

> curl x.x.x.x(서비스 리소스의 ClusterIP)
> host myweb-svc
> curl myweb-svc
```

### Session Affinity

세션 고정

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-ses
spec:
  type: ClusterIP
  sessionAffinity: ClientIP
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

### Named Port
`myweb-rc-named.yaml`

``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-rs-named
spec:
  raplicas: 3
  selector:
    matchLabels:
      app: web
      app: dev
  template:
    metadata:
      labes:
        app: web
        app: dev
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
          ports:
            - containerPort: 8080
              protocol: TCP
              name: web8080
```

`myweb-svc-named.yaml`

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-named
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - port: 80
      targetPort: web8080
```

### Multi Port
`myweb-rs-multi.yaml`

``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myweb-rs-multi
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      app: dev
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
            - containerPort: 8443
              protocol: TCP
```

`myweb-svc-multi.yaml`
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-multi
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
      name: http
    - port: 443
      targetPort: 8443
      name: https
```

## Service Discovery

### 환경 변수를 이용한 Service Discovery

모든 파드는 실행 시 현재 시점의 서비스 목록을 환경 변수 제공

``` bash
# env | grep MYWEB
MYWEB_SVC_PORT_80_TCP_PORT=80
MYWEB_SVC_PORT_80_TCP_PROTO=tcp
MYWEB_SVC_PORT_80_TCP=tcp://10.233.3.182:80
MYWEB_SVC_SERVICE_HOST=10.233.3.182
MYWEB_SVC_PORT=tcp://10.233.3.182:80
MYWEB_SVC_SERVICE_PORT=80
MYWEB_SVC_PORT_80_TCP_ADDR=10.233.3.182
```

### DNS를 이용한 Service Discovery

kube-dns(coredns-X 파드)
Service 생성하면 해당 이름으로 FQDN을 DNS 서버에 등록

```
[서비스 이름].[네임스페이스].[오브젝트 타입].[도메인]

myweb-svc.default.svc.cluster.local
```

#### nodelocal DNS
nodelocal DNS 캐시 사용
Pod - DNS -> 169.254.25.10(node-cache): DNS Cache Server -> coredns SVC(kube-system NS) -> coredns POD

nodelocal DNS 캐시 사용 X
Pod - DNS -> coredns SVC(kube0-system NS) -> coredns POD

## Service - NodePort

외부 브라우저에서도 접근할 수 있도록 NodePort라는 개념이 등장한다.

NodePOrt는 노드에 노출되어 외부에서도 접근이 가능한 서비스이다.

다만 노드의 IP가 변경된 경우 처리를 해줘야하기 때문에 실 서비스에서도 NodePort만으로 외부 클라이언트를 노출하는 방식은 권장되지 않는다.

NodePort는 노드가 여러개 일 때 NodePort를 생성하면 모든 노드에 NodePort가 생성된다.

이때 어떤 노드에 요청을 보내도 내부의 원하는 ClusterIP로 자동으로 연결되도록 작동한다.

`svc.spec.type`

- ClusterIP : 클러스터 내에서 사용하는 LB
- NodePort : 클러스터 외부에서 접근하는 포인트
- LoadBalancer: 클러스터 외부에서 접근하는 LB

NodePort의 범위 : 30000 - 32767

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
      nodePort: 31313
```

## Service - LoadBalancer

모든 노드에 외부 접속 분산 요청을 처리하기 위해서는 NodePort보다는 LoadBalancer를 사용하는 것이 적절하다.

NodePort앞에 LB가 붙어있는 것을 볼 수 있는데 이는 단 1개의 IP만을 외부에 노출하게 되며 해당 IP로 모든 트래픽을 부하 분산하기 위한 것이다.

HTTP, TCP, UDP 등 흔히 사용되는 네트워크 프로토콜과 통신할 수 있다.

#### L4 LB

`myweb-svc-lb.yaml`

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-lb
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 31313
```

### Metallb - Addon
`~/kubespray/inventory/mycluster/group_vars/k8s-cluster/addons.yml`

```
...
139 metallb_enabled: true
140 metallb_speaker_enabled: true
141 metallb_ip_range:
142   - "192.168.100.240-192.168.100.249"
...
168 metallb_protocol: "layer2"
...
```

`~/kubespray/inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml`

```
129 kube_proxy_strict_arp: true
```

``` bash
ansible-playbook -i inventory/mycluster/inventory.ini cluster.yml -b
```

## Service - ExternalName

클러스터 내부에서 클러스터 외부의 특정 서비스에 접속하기 위해 DNS CNAME을 설정

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: weather-ext-svc
spec:
  type: External Name
  externalName: www.google.com
```

## Ingress

Ingress는 도메인 이름, 도메인 Path에 따라 내부에 있는 ClusterIP에도 같은 이름으로 연결할 수 있도록 해준다.

Ingress 하나만 만들어도 여러개의 LB를 만들어 자원을 낭비하는 것을 방지할 수 있다.

L7 LB = ALB

``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myweb-ing
spec:
  rules:
    - host: '*.jeonj.xyz'
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

방법 1.

``` bash
curl --resolve www.jeonj.xyz:80:192.168.100.100 http://www.jeonj.xyz
```

방법 2.
``` bash
...
192.168.100.100 www.jeonj.xyz
```

방법 3.
> https://nip.io/
> https://sslip.io/


``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myweb-ing
spec:
  rules:
    - host: '*.nip.io
    ...
```

``` bash
kubectl replace -f myweb-ing.yaml
```

``` bash
curl http://192-168-100-100.nip.io
```

### 인그레스 예제

hello:one 이미지

`Dockerfile`

```
FROM httpd
COPY index.html /usr/local/apache2/htdocs/index.html
```

`index.html`
``` html
<h1> Hello One </h1>
```

hello:two 이미지
`Dockerfile`
```
FROM httpd
COPY index.html /usr/local/apache2/htdocs/index.html
```

`index.html`
``` html
<h1> Hello Two </h1>
```

``` bash
docker push X/hello:one
docker push X/hello:two
```

#### ReplicaSet
`one-rs.yaml`

``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: one-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-one
  template:
    metadata:
      labels:
        app: hello-one
    spec:
      containers:
        - name: hello-one
          image: c1t1d0s7/hello:one
          ports:
            - containerPort: 80
              protocol: TCP
```

`two-rs.yaml`
``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: two-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-two
  template:
    metadata:
      labels:
        app: hello-two
    spec:
      containers:
        - name: hello-two
          image: c1t1d0s7/hello:two
          ports:
            - containerPort: 80
              protocol: TCP
```

`one-svc-np.yaml`
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: one-svc-np
spec:
  type: NodePort
  selector:
    app: hello-one
  ports:
    - port: 80
      targetPort: 80
```

`two-svc-np.yaml`
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: two-svc-np
spec:
  type: NodePort
  selector:
    app: hello-two
  ports:
    - port: 80
      targetPort: 80
```

`hello-ing.yaml`
``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-ing
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: / # URL 재작성, /one -> /, /two -> /
spec:
  rules:
    - host: '*.nip.io'
      http:
        paths:
          - path: /one
            pathType: Prefix
            backend:
              service:
                name: one-svc-np
                port:
                  number: 80
          - path: /two
            pathType: Prefix
            backend:
              service:
                name: two-svc-np
                port:
                  number: 80
```

``` bash
kubectl create -f .
```

## Readiness Probe

파드의 헬스체크를 통해 서비스의 엔드포인트 리소스에 타겟 등록

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
          image: ghcr.io/c1t1d0s7/go-myweb:alpine
          ports:
            - containerPort: 8080
              protocol: TCP
          readinessProbe:
            exec:
              command:
                - ls
                - /tmp/ready
```

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-lb
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

``` bash
kubectl create -f .
```

``` bash
watch -n1 -d kubectl get po,svc,ep
```

``` bash
kubectl exec <POD> -- touch /tmp/ready