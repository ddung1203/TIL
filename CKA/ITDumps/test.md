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