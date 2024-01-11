# Mock Test

## 1

```bash
kubectl get pod nginx-dev nginx-prod
kubectl delete pod nginx-dev nginx-prod
```

## 2

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kucc1
spec:
  containers:
  - name: nginx
    image: nginx
  containers:
  - name: consul
    image: consul
```

## 3

```bash
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.startTime}{"\n"}{end}'
```

## 4

```bash
kubectl logs pod foo | grep unable-to-access-website
```

## 5

```bash
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/opt/KUIN00601/ca.crt --cert=/opt/KUIN00601/etcd-client.crt --key=/opt/KUIN00601/etcd-client.key \
  snapshot save /src/data/etcd-snapshot.db
```

```bash
ETCDCTL_API=3 etcdctl --data-dir /var/lib/backup/etcd-snapshot.db snapshot restore /var/lib/backup/etcd-snapshot-previous.db
```

`/etc/kubetnetes/manifests/etcd.yaml`
```yaml
  volumes:
  - hostPath:
      path: /var/lib/backup/etcd-snapshot-previous.db
      type: DirectoryOrCreate
    name: etcd-data
```

## 6

```bash
kubectl get pod -o custom-columns=POD_NAME:.metadata.name,POD_STATUS:.status.phase
```

## 7

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hungry-bear
spec:
  containers:
  - name: checker
    image: alpine
    command: ['/bin/sh', '-c', 'if [ -f /work/dir/calm.txt ]; then sleep 100000; else exit 1; fi']
    volumeMounts:
      - name: workdir
        mountPath: /workdir
  initContainers:
  - name: create
    image: alpine
    command: ['/bin/sh', '-c', 'touch /workdir/calm.txt']
    volumeMounts:
      - name: workdir
        mountPath: /workdir
  volumes:
  - name: workdir
    emptryDir: {}
```

## 8

```bash
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.namespace}{"\n"}{end}'
```

## 9

```bash
kubectl edit deployment webserver
```

## 10

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-kusc00101
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disk: ssd
```

## 11

```bash
kubectl get pod nginx-dev -o wide
```

```bash
kubectl get pods busybox-sleep -o=jsonpath='{.metadata.name}{"\t"}{.status.podIP}{"\n"}'
```

## 12

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-data
spec:
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: /srv/app-data
```

## 13

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.10.10-alpine
        ports:
        - containerPort: 80
```

```bash
kubectl apply -f 13.yaml --record
```

```bash
kubectl set image deployment nginx-app nginx=nginx:1.11.13-alpine --record
```

```bash
kubectl rollout undo deployment nginx-app
```

## 14

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: big-corp-app
spec:
  containers:
  - name: big-corp-app
    image: busybox
    command: ['/bin/sh', '-c', 'i=0; while true; do echo "(date) INFO $i" >> /var/log/big-corp-app.log; i=$((i+1)); sleep 1; done']
    volumeMounts:
      - name: log
        mountPath: /var/log
  - name: sidecar
    image: busybox
    command: ['/bin/sh', '-c', 'tail -n+1 -f /var/log/big-corp-app.log']
    volumeMounts:
      - name: log
        mountPath: /var/log
  volumes:
    - name: log
      emptyDir: {}
```

## 15

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: ds-kusc00201
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
```

## 16

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
```

```bash
kubectl get pod/nginx --v=5
kubectl get pod/nginx --v=6
kubectl get pod/nginx --v=7
kubectl get pod/nginx --v=8
kubectl get pod/nginx --v=9
```

> verbosity: 로그 상세 레벨

## 17

```bash
kubectl get pods -A > /opt/pods-list.yaml
```

## 18

```bash
# ik8s-master-0
kubeadm token list

# if the tokens expires
kubeadm token create

# hash
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | \
   openssl dgst -sha256 -hex | sed 's/^.* //'

kubeadm join --token <token> <control-plane-host>:<control-plane-port> --discovery-token-ca-cert-hash sha256:<hash>
```

## 19

```bash
kubectl get pod nginx -o custom-columns=POD_NAME:.metadata.name,POD_STATUS:.status.phase
```

## 20

```bash
kubectl get pod nginx -o jsonpath='{.spec.containers[].image}'
```

## 21

```bash
systemctl status containerd
systemctl status kubelet

sudo systemctl enable --now kubelet
```

## 22

```bash
kubectl get pod nginx -o jsonpath='{.spec.containers[].image}'
```

## 23

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: busybox
spec:
  containers:
  - name: busybox
    image: busybox
    command: ['/bin/sh', '-c', 'env > /var/log/envpod']
  restartPolicy: Never
```

검증

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: busybox
spec:
  containers:
  - name: busybox
    image: busybox
    command: ['/bin/sh', '-c', 'env > /var/log/envpod']
    volumeMounts:
      - name: volume
        mountPath: /var/log
  - name: test
    image: busybox
    command: ['/bin/sh', '-c', 'sleep 10000']
    volumeMounts:
      - name: volume
        mountPath: /var/log
  restartPolicy: Never
  volumes:
    - name: volume
      emptyDir: {}
```

## 24

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: engineering
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
```

## 25

```bash
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/opt/KUCM00302/ca.crt --cert=/opt/KUCM00302/etcd-client.crt --key=/opt/KUCM00302/etcd-client.key \
  snapshot save /src/data/etcd-snapshot.db
```