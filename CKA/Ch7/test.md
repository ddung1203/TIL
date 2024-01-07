# Test

1. Retrieve Error Messages from a Container Log

```
Cluster: kubectl config use-context hk8s
In the customa namespace, check the log for the nginx container in the custom-app Pod.
Save the lines which contain the text “error” to the file /var/CKA2022/errors.txt.
```

```bash
kubectl get logs pod/custom-app -n customa | grep error > /var/CKA2022/errors.txt
```

2. Node Troubleshooting

```
Cluster: kubectl config use-context hk8s
A Kubernetes worker node, named hk8s-w2 is in state NotReady.
Investigate why this is the case, and perform any appropriate steps to bring the node to a Ready state, ensuring that any changes are made permanent.
```

```bash
# containerd
# kubelet
sudo systemctl enable --now kubelet
```

3. Count the Number of Nodes That Are Ready to Run Normal Workloads

```
Cluster: kubectl config use-context hk8s
Determine how many nodes in the cluster are ready to run normal workloads (i.e., workloads that do not have any special tolerations).
Output this number to the file /var/CKA2022/count.txt
```

```bash
kubectl get nodes | grep Ready
echo 3 > /var/CKA2022/count.txt
```

> `kubectl get nodes | grep -i -w ready | wc -l > /var/CKA2022/count.txt`

4. Management Node

```
Cluster: kubectl config use-context k8s
Set the node named k8s-worker1 as unavailable and reschedule all the pods running on it
```

```bash
kubectl drain k8s-worker1 --ignore-daemonsets --delete-emptydir-data --force
```

5. ETCD backup & restore

```
작업 클러스터 : kubectl config use-context k8s
First, create a snapshot of the existing etcd instance running at https://127.0.0.1:2379 , saving the snapshot to /data/etcdsnapshot.db .
Next, restore an existing, previous snapshot located at /data/etcd-snapshot-previous.db .
The following TLS certificates/key are supplied for connecting to the server with etcdctl:
 CA certificate: /etc/kubernetes/pki/etcd/ca.crt
 Client certificate: /etc/kubernetes/pki/etcd/server.crt
 Client key: /etc/kubernetes/pki/etcd/server.key
```

```bash
sudo ETCDCTL_API=3 etcdctl --endpoints 127.0.0.1:2379 \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  snapshot save /data/etcdsnapshot.db
```

```bash
sudo ETCDCTL_API=3 etcdctl --data-dir /var/lib/etcd-previous snapshot restore /data/etcd-snapshot-previous.db
```

> `/data/etcd-snapshot-previous.db`의 파일로 restore를 진행하고, etcd 백업했던 걸 restore 시켜준다.
> 
> 따라서, 현재 etcd는 여전히 과거 정보(`/var/lib/etcd`)를 사용하고 있고, 변경된 restore된 디렉토리(`/var/lib/etcd-previous`)를 사용하도록 구성해야 한다.

> `--data-dir`의 경우, 주어지지 않으면 원하는 디렉토리 지정

`/etc/kubernetes/manifests/etcd.yaml`

```yaml
...
  volumes:
  - hostPath:
      path: /var/lib/etcd-previous
      type: DirectoryOrCreate
    name: etcd-data
```

6. Cluster Upgrade - only Master

```
작업 클러스터 : kubectl config use-context k8s
upgrade system : hk8s-m
Given an existing Kubernetes cluster running version 1.22.4 ,
upgrade all of the Kubernetes control plane and node components on the master node only to version 1.23.3 .
Be sure to drain the master node before upgrading it and uncordon it after the upgrade
```

```bash
sudo apt update
sudo apt-cache madison kubeadm

sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.23.3-00' && \
sudo apt-mark hold kubeadm
```

```bash
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.23.3-00' && \
sudo apt-mark hold kubeadm
```

```bash
kubeadm version

sudo kubeadm upgrade plan v1.23.3
sudo kubeadm upgrade apply v1.23.3
```

```bash
kubectl drain k8s-master --ignore-daemonsets
```

```bash
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet='1.23.3-00' kubectl='1.23.3-00' && \
sudo apt-mark hold kubelet kubectl
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

```bash
kubectl uncordon k8s-master
```

> kubeadm 뿐만 아니라, kubelet과 kubectl 또한 업그레이드 필요


7. Authentication and Authorization

```
Cluster : k8s
Context You have been asked to create a new ClusterRole for a deployment pipeline and bind it to a specific ServiceAccount scoped to a specific namespace.
Task:
 - Create a new ClusterRole named deployment-clusterrole , which only allows to create the following resource types:
Deployment StatefulSet DaemonSet
 - Create a new ServiceAccount named cicd-token in the existing namespace app-team1 .
 - Bind the new ClusterRole deployment-clusterrole to the new ServiceAccount cicd-token , limited to the namespace app-team1 .
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: deployment-clusterrole
rules:
- apiGroups: [""]
  resources: ["Deployment", "StatefulSet", "DaemonSet"]
  verbs: ["create"]
```

```bash
kubectl create sa cicd-token -n app-team1
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: deployment-clusterrolebinding
subjects:
- kind: ServiceAccount
  name: cicd-token
  namespace: app-team1
roleRef:
  kind: ClusterRole
  name: deployment-clusterrole
  apiGroup: rbac.authorization.k8s.io
```

8. Pod 생성하기

```
작업 클러스터 : kubectl config use-context k8s
 Create a new namespace and create a pod in the namespace
TASK:
namespace name: cka-exam
pod Name: pod-01
image: busybox
environment Variable: CERT = "CKA-cert"
command: /bin/sh
args: -c "while true; do echo $(CERT); sleep 10;done"
```

```bash
kubectl create ns cka-exam
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-01
spec:
  containers:
  - name: pod-01
    image: busybox
    env:
    - name: CERT
      value: "CKA-cert"
    command: ['/bin/sh', '-c', 'while true; do echo $(CERT); sleep 10;done']
```

9. multi-container Pod 생성

```
cluster : kubectl config use-context hk8s
Create a pod with 4 containers running : nginx, redis, memcached and consul
pod name: eshop-frontend
image: nginx
image: redis
image: memcached
image: consul
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

10. Side-car Container Pod 실행

```
작업 클러스터 : kubectl config use-context k8s
현재 운영 중인 eshop-cart-app Pod의 로그를 Kubernetes built-in logging 아키텍처(예: kubectl logs)에 통합하는 로그 스트리밍 사이드카 컨테이너를 운영하시오.
- busybox 이미지를 사용하여 price 라는 이름의 side-car container를 기존 eshop-cart-app에 추가합니다.
- 새 price 컨테이너는 다음과 같은 command를 실행해야 합니다.
 Command: /bin/sh, -c, “tail -n+1 -f /var/log/cart-app.log”
- /var/log에 마운트 된 볼륨을 사용하여 사이드카 컨테이너에서 로그 파일 cart-app.log를 사용해야 합니다.
- eshop-cart-app Pod와 cart-app 컨테이너를 수정하지 마시오
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
    command: ['/bin/sh', '-c', 'i=1;while :;do  echo -e "$i: Price: $((RANDOM % 10000 + 1))" >> /var/log/cart-app.log; i=$((i+1)); sleep 2; done']
    volumeMounts:
    - name: varlog
      mountPath: /var/log
  - name: price
    image: busybox
    command: ["/bin/sh", "-c", "tail -n+1 -f /var/log/cart-app.log"]
    volumeMounts:
    - name: varlog
      mountPath: /var/log
  volumes:
  - name: varlog
    emptyDir: {}
```

11. Pod Scale-out

```
Cluster: kubectl config use-contex k8s
Expand the number of running Pods in "eshop-order" to 5.
- namespace: devops
- deployment: eshop-order
- replicas: 5
```

```bash
$ kubectl edit deployment.apps/eshop-order -n devops
deployment.apps/eshop-order edited

$ kubectl get all -n devops
NAME                               READY   STATUS    RESTARTS   AGE
pod/eshop-order-74dbc8f5bf-2lr6j   1/1     Running   0          62m
pod/eshop-order-74dbc8f5bf-n5fnl   1/1     Running   0          62m
pod/eshop-order-74dbc8f5bf-pjhvq   1/1     Running   0          4s
pod/eshop-order-74dbc8f5bf-qstr7   1/1     Running   0          4s
pod/eshop-order-74dbc8f5bf-smcd2   1/1     Running   0          4s

NAME                      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/eshop-order-svc   ClusterIP   10.109.63.46   <none>        80/TCP    3d20h

NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/eshop-order   5/5     5            5           311d

NAME                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/eshop-order-74dbc8f5bf   5         5         5       311d
```

> `kubectl scale deployment eshop-order --replicas=5 -n devops`

12. Rolling Update

```
Cluster: kubectl config use-context k8s
Create a deployment as follows:
- TASK:
  - name: nginx-app
  - Using container nginx with version 1.11.10-alpine
  - The deployment should contain 3 replicas
- Next, deploy the application with new version 1.11.13-alpine, by performing a rolling update
- Finally, rollback that update to the previous version 1.11.10-alpine
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
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
        image: nginx:1.11.10-alpine
        ports:
        - containerPort: 80
```

```bash
$ kubectl create -f 12.yaml --record
```

```bash
$ kubectl set image deployment.apps/nginx-app nginx=nginx:1.11.13-alpine --record
```

```bash
$ kuebctl rollout undo deployment.apps/nginx-app
```

13. Network Policy with Namespace

```
작업 클러스터 : kubectl config use-context k8s
Create a new NetworkPolicy named allow-port-from-namespace in the existing namespace devops.
Ensure that the new NetworkPolicy allows Pods in namespace migops(using label team=migops) to connect to port 80 of Pods in namespace devops.
Further ensure that the new asdasd: does not allow access to Pods, which don't listen on port 80 does not allow access from Pods, which are not in namespace migops
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-port-from-namespace
  namespace: devops
spec:
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              team: migops
      ports:
        - protocol: TCP
          port: 80
```

14. Create a persistent volume

```
Cluster: kubectl config use-context k8s
Create a persistent volume with name app-config, of capacity 1Gi and access mode ReadWriteMany.
The type of volume is hostPath and its location is /var/app-config
```

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-config
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: /var/app-config
```

15. Deploy and Service

```
작업 클러스터 : kubectl config use-context k8s
Reconfigure the existing deployment front-end and add a port specification named http exposing port 80/tcp of the existing container nginx.
Create a new service named front-end-svc exposing the container port http.
Configure the new service to also expose the individual Pods via a NodePort on the nodes on which they are scheduled
```

```bash
$ kubectl edit deployment.apps/front-end
    # spec:
    #   containers:
    #   - image: nginx
    #     imagePullPolicy: Always
    #     name: http
    #     ports:
    #     - containerPort: 80
    #       name: http
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: front-end-svc
spec:
  type: NodePort
  selector:
    run: nginx
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: http
```

> `targetPort`의 경우, deployment에서 http의 이름으로 지정했기 때문에, 상기와 같이 작성 가능

16. DNS Lookup

```
작업 클러스터 : kubectl config use-context k8s
Create a nginx pod called nginx-resolver using image nginx, expose it internally with a service called nginx-resolver-service.
Test that you are able to look up the service and pod names from within the cluster. Use the image: busybox:1.28 for dns lookup.
 - Record results in /var/CKA2022/nginx.svc and /var/CKA2022/nginx.pod
 - Pod: nginx-resolver created
 - Service DNS Resolution recorded correctly
 - Pod DNS resolution recorded correctly
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-resolver
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-resolver-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dnslookup-pod
spec:
  containers:
  - name: dns
    image: busybox:1.28
    command: ['sh', '-c', 'nslookup 192-168-194-93.default.pod.cluster.local']
  restartPolicy: Never
---
apiVersion: v1
kind: Pod
metadata:
  name: dnslookup-service
spec:
  containers:
  - name: dns
    image: busybox:1.28
    command: ['sh', '-c', 'nslookup nginx-resolver-service']
  restartPolicy: Never
```

> Pod DNS의 경우, 상기의 방식을 따라야 한다.

```bash
$ nslookup 192.168.194.102
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      192.168.194.102
Address 1: 192.168.194.102 192-168-194-102.nginx-resolver-service.default.svc.cluster.local

$ nslookup nginx-resolver-service
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      nginx-resolver-service
Address 1: 10.101.101.149 nginx-resolver-service.default.svc.cluster.local
```

> `kubectl run test-nslookup --image=busybox:1.28 -it --restart=Never --rm -- nslookup nginx-resolver-service > /var/CKA2022/nginx.svc` 또한 가능하다.

17. Application with PVC

```
Cluster: kubectl config use-context k8s
Create a new PersistentVolumeClaim:
  - Name: pv-volume
  - Class: csi-hostpath-sc
  - Capacity: 10Mi
Create a new Pod which mounts the PersistentVolumeClaim as a volume:
  - Name: web-server
  - Image: nginx
  - Mount path: /usr/share/nginx/html
Configure the new Pod to have ReadWriteOnce access on the volume
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pv-volume
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi
  storageClassName: csi-hostpath-sc
---
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  containers:
  - name: web-server
    image: nginx
    volumeMounts:
    - name: vol
      mountPath: /usr/share/nginx/html
  volumes:
  - name: vol
    hostPath:
      path: /usr/share/nginx/html
```