# Volume

`spec.volumes.*` : 볼륨 유형

## emptyDir

임시로 사용할 빈 볼륨, 파드 삭제 시 볼륨 같이 삭제

Pod가 실행되는 노드의 디스크 공간에 마운트 된다.

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

hostPath는 노드의 파일시스템의 특정 파일이나 디렉토리를 Pod에 마운트하여 사용한다.

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

Pod 내부에서 특정 데이터를 보유해야 하는 statefule한 app의 경우 stateless한 데이터를 영속적으로 저장하기 위한 방법이 필요하다.

Pod에서 실행중인 애플리케이션이 디스크에 데이터를 유지해야한다면 emptyDir, hostPath를 사용할 수 없다.

어떤 클러스터 노드에서도 접근할 수 있어야 하므로 NAS 유형의 스토리지에 저장이 되어야 한다.


- PersistentVolyme : 스토리지 볼륨 정의

PV는 Volume 자체를 의미한다.

Kubernetes Cluster에서 관리되는 저장소로 Pod와는 별개로 관리되고 별도의 생명주기를 가지고 있어 Pod가 재실행되더라도 PV 데이터는 정책에 따라 유지/삭제된다.

특징
  - Cluster Storage의 일부
  - Cluster Node와 같은 리소스
  - Namespace에 속하지 않음
  - Pod와 독립적인 lifeCycle을 가짐


- PersistentVolumeClaim : PV를 요청

PVC는 Pod의 볼륨과 PVC를 연결하는 관계 선언이다.

PVC는 사용자가 PV에 요청으로 PV를 추상화해 개발자가 손쉽게 PV를 사용할 수 있도록 해주는 기능이다.

사용하고 싶은 용량은 얼마인지 읽기/쓰기는 어떤 모드로 설정하고 싶은지 등을 정해서 PV에게 전달하는 역할을 한다.

개발자는 Pod를 생성할 때 Volume을 정의하고 이 볼륨 정의 부분에 물리적 디스크에 대한 특성을 정의하는 것이 아닌 PVC를 지정해 관리자가 생성한 PV와 연결한다.

Storage를 Pod에 직접 할당하는 것이 아닌 중간에 PVC를 통해 사용하기 때문에 Pod와 Storage 관리를 명확히 구분할 수 있다.

예를 들어 가동 중인 Pod의 Storage를 변경하기 위해 Pod 자체를 재시작, 재생성 할 필요 없이 Pod에 연결된 PVC만 수정하면 Pod와 별개로 PVC를 통해 Storage를 관리할 수 있다.

특징
  - Storage에 대한 사용자의 요청
  - PV Resource 소비
  - 특정 Size나 Access mode를 요청


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
  - 저장할 수 있는 공간 확보
    - Static Provisioning
    - Dynamic Provisioning
2. 바인딩
  - 상위의 Provisioning을 통해 만들어진 PV를 PVC와 연결하는 단계
3. 사용
4. 회수/반환(Reclaim)
  - Retain : 보존 - PV를 삭제하지 않음(Release <- PVC가 연결 X)
  - Delete : 삭제 - PV를 삭제 / 실제 스토리지 내용 삭제
  - Recycle : 재사용 (X) - 실제 스토리지 내용을 비우고, PV를 사용가능한 상태(Available)

### 접근 모드(Access Mode)
- ReadWriteOnce : RWO
- ReadWriteMany : RWX
- ReadOnlyMany : ROW

### Volume 모드

- filesystem : default 옵션으로 volume을 일반 파일시스템 형식으로 붙여서 사용하게 한다.
- raw : volume을 RAW 파일시스템 형식으로 붙여서 사용하게 한다.
- block : Filesystem이 없는 Block 장치와 연결될 때는 Block으로 설정한다.


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

## PV & PVC, NFS를 이용한 Jenkins CI Pod 구축

`jenkins.yaml`

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jenkins
  template:
    metadata:
      labels:
        app: jenkins
    spec:
      serviceAccountName: jenkins-admin
      securityContext:
            fsGroup: 1000 
            runAsUser: 1000
      containers:
        - name: jenkins
          image: jenkins/jenkins:lts
          resources:
            limits:
              memory: "500Mi"
              cpu: "500m"
            requests:
              memory: "500Mi"
              cpu: "500m"
          ports:
            - name: httpport
              containerPort: 8080
            - name: jnlpport
              containerPort: 50000
          livenessProbe:
            httpGet:
              path: "/login"
              port: 8080
            initialDelaySeconds: 90
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 5
          readinessProbe:
            httpGet:
              path: "/login"
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          volumeMounts:
            - name: jenkins
              mountPath: /var/jenkins_home         
      volumes:
        - name: jenkins
          persistentVolumeClaim:
            claimName: jenkins
# Service Config
---
apiVersion: v1
kind: Service
metadata:
  name: jenkins-service
  annotations:
      prometheus.io/scrape: 'true'
      prometheus.io/path:   /
      prometheus.io/port:   '8080'
spec:
  selector: 
    app: jenkins
  type: NodePort  
  ports:
    - name: httpport
      port: 8080
      targetPort: 8080
      nodePort: 32000
    - name: jnlpport
      port: 50000
      targetPort: 50000
```

`pv.yaml`

``` yaml
# Persistent Volume
apiVersion: v1
kind: PersistentVolume
metadata:
  name: jenkins
spec:
  capacity:
    storage: 15G
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  nfs:
    path: /home/vagrant/nfs/jenkins
    server: 192.168.100.100
```

`pvc.yaml`

``` yaml
# Persistent Volume Claim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jenkins
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  volumeName: jenkins
  storageClassName: ''
```

`service-account.yaml`
``` yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins-admin
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: jenkins
  namespace: default
  labels:
    "app.kubernetes.io/name": 'jenkins'
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["create","delete","get","list","patch","update","watch"]
- apiGroups: [""]
  resources: ["pods/exec"]
  verbs: ["create","delete","get","list","patch","update","watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get","list","watch"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: jenkins-role-binding
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: jenkins
subjects:
- kind: ServiceAccount
  name: jenkins-admin
  namespace: default
```