# Volume

`spec.volumes.*` : 볼륨 유형

## emptyDir

임시로 사용할 빈 볼륨, 파드 삭제 시 볼륨 같이 삭제

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myweb-pod
spec:
  containers:
    - name: myweb1
      image: httpd
      volumeMounts:
        - name: emptyvol
          mountPath: /empty
    - name: myweb2
      image: ghcr.io/c1t1d0s7/go-myweb:alpine
      volumeMounts:
        - name: emptyvol
          mountPath: /empty
  volumes:
    - name: emptyvol
      emptyDir: {}
```

``` bash
kubectl exec -it myweb-pod -c myweb1 -- bash

> cd /empty
> touch a b c
```

``` bash
kubectl exec -it myweb-pod -c myweb2 -- sh

> ls /empty
```

## initContainer(초기화 컨테이너)

> https://kubernetes.io/ko/docs/concepts/workloads/pods/init-containers/

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-pod
spec:
  initContainers:
    - name: gitpull
      image: alpine/git
      args:
        - clone
        - -b
        - v2.18.1
        - https://github.com/kubernetes-sigs/kubespray.git
        - /repo
      volumeMounts:
        - name: gitrepo
          mountPath: /repo
  containers:
    - name: gituse
      image: busybox
      args:
        - tail
        - -f
        - /dev/null
      volumeMounts:
        - name: gitrepo
          mountPath: /kube
  volumes:
    - name: gitrepo
      emptyDir: {}
```

## hostPath

`/mnt/web_contents/index.html`

``` html
<h1> Hello hostPath </h1>
```

> 참고
> 로컬 스토리지 : 다른 호스트에 스토리지 볼륨을 제공할 수 없다.
> - emptyDir
> - hostPath
> - gitRepo
> - local

## PV & PVC

- PersistentVolyme : 스토리지 볼륨 정의
- PersistentVolumeClaim : PV를 요청

PV, PVC 예제

Pod
``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: mypod
      image: httpd
      volumeMounts:
        - name: myvol
          mountPath: /tmp
  volumes:
    - name: myvol
      persistentVolumeClaim:
        name: mypvc
```

PVC
``` yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc
spec:
  volumeName: mypv
```

PV
``` yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mypv
spec:
  hostPath:
    path: /web_contents
    type: DirectoryOrCreate
```

### PV, PVC 생명주기

PV <- 1:1 -> PVC

1. 프로비저닝
2. 바인딩
3. 사용
4. 회수/반환(Reclaim)
  - Retain : 보존 - PV를 삭제하지 않음(Release <- PVC가 연결 X)
  - Delete : 삭제 - PV를 삭제 / 실제 스토리지 내용 삭제
  - Recycle : 재사용 (X) - 실제 스토리지 내용을 비우고, PV를 사용가능한 상태(Available)

### 접근 모드(Access Mode)
- ReadWriteOnce : RWO
- ReadWriteMany : RWX
- ReadOnlyMany : ROW


### NFS를 사용한 정적 프로비저닝(Static Provision)

node1 : NFS 서버

``` bash
sudo apt install nfs-kernel-server -y
```

``` bash
sudo mkdir /nfsvolume
echo "<h1> Hello NFS Volume </h1>" | sudo tee /nfsvolume/index.html
```

``` bash
sudo chown -R www-data:www-data /nfsvolume
```

`/etc/exports`

```
/nfsvolume 192.168.100.0/24(rw,sync,no_subtree_check,no_root_squash)
```
`` bash
sudo systemctl restart nfs-kernel-server
systemctl status nfs-kernel-server
```

node1, node2, node3

``` bash
sudo apt install nfs-common -y
```

또는

``` bash
ansible all -i ~/kubespray/inventory/mycluster/inventory.ini -m apt -a 'name=nfs-common' -b
```

PV
``` yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mypv
spec:
  accessModes:
    - ReadWriteMany
  capacity:
    storage: 1G
  persistentVolumeReclaimPolicy: Retain
  nfs:
    path: /nfsvolume
    server: 192.168.100.100
```


PVC
``` yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc
spec:
  accessModes:
    - ReatWriteMany
  resources:
    requests:
      storage: 1G
  storageClassName: ''
  volumeName: mypv
```

RS
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
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: myweb
          image: httpd
          volumeMounts:
            - name: myvol
              mountPath: /usr/local/apache2/htdocs
      volumes:
        - name: myvol
          persistentVolumeClaim:
            claimName: mypvc
```

SVC
``` yaml
apiVersion: v1
kind: service
metadata:
  name: myweb-svc-lb
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 80
  selector:
    app: web
```

## 동적 프로그래밍

### NFS Dynamic Provisioner 구성
> https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner

``` bash
git clone https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner.git
```

``` bash
cd nfs-subdir-external-provisioner/deploy
```

``` bash
kubectl create -f rbac.yaml
```

`deployment.yaml`
``` yaml
...
          env:
            - name: PROVISIONER_NAME
              value: k8s-sigs.io/nfs-subdir-external-provisioner
            - name: NFS_SERVER
              value: 192.168.100.100
            - name: NFS_PATH
              value: /nfsvolume
      volumes:
        - name: nfs-client-root
          nfs:
            server: 192.168.100.100
            path: /nfsvolume
```

``` bash
kubectl create -f deployment.yaml
```

``` bash
kubectl create -f class.yaml
```

`mypvc-dynamic.yaml`
``` yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc-dynamic
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1G
  storageClassName: 'nfs-client'
```

``` bash
kubectl create -f mypvc-dynamic.yaml
```

``` bash
echo "<h1> Hello NFS Dynamic Provision </h1>" | sudo tee /nfsvolume/XXX/index.html
```

`myweb-rs-dynamic.yaml`
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
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: myweb
          image: httpd
          volumeMounts:
            - name: myvol
              mountPath: /usr/local/apache2/htdocs
      volumes:
        - name: myvol
          persistentVolumeClaim:
            claimName: mypvc-dynamic
```

``` bash
kubectl create -f myweb-rs-dynamic.yaml
```

### 기본 스토리지 클래스
`~/nfs-subdir-external-provisioner/deploy/class.yaml`
``` yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner # or choose another name, must match deployment's env PROVISIONER_NAME'
parameters:
  archiveOnDelete: "false"
```

``` bash
kubectl apply -f class.yaml
```

```
kubectl get sc

NAME                   ...
nfs-client (default)   ...
```

``` yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc-dynamic
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1G
```