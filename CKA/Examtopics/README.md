# Page 1

## 1

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

혹은

```bash
kubectl create clusterrole deployment-clusterrole --verb=create --resource=Deployment,StatefuleSet,DaemonSet
```

```bash
kubectl create sa cicd-token -n app-team1
```

```bash
kubectl create clusterrolebinding deployment-clusterrolebinding --clusterrole=deployment-clusterrole --serviceaccount=app-team1:cicd-token
```

## 2

```bash
kubectl drain ek8s-node-0 --ignore-daemonsets --delete-emptydir-data
```

## 3

```bash
ssh mk8s-master-0

sudo apt update

sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.22.2-00' && \
sudo apt-mark hold kubeadm

sudo kubeadm upgrade apply v1.22.2

kubectl drain mk8s-master-0 --ignore-daemonsets

sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet='1.22.2-00' kubectl='1.22.2-00' && \
sudo apt-mark hold kubelet kubectl

sudo systemctl daemon-reload
sudo systemctl restart kubelet

kubectl uncordon mk8s-master-0
```

## 4

```bash
sudo ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cert=/opt/KUIN00601/etcd-client.crt \
  --key=/opt/KUIN00601/etcd-client.key \
  --cacert=/opt/KUIN00601/ca.crt \
  snapshot save /var/lib/backup/etcd-snapshot.db
```

```bash
sudo ETCDCTL_API=3 etcdctl --data-dir /var/lib/etcd-previous snapshot restore /var/lib/backup/etcd-snapshot-previous.db
```

`/etc/kubernetes/manifests/etcd.yaml`
```yaml
# Volume의 hostPath 수정
```

## 5

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-port-from-namespace
  namespace: fubar
spec:
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              project: myproject
      ports:
        - protocol: TCP
          port: 9000
```

## 6

```bash
kubectl edit deployment front-end
# port 추가
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: front-end-svc
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - port: 80
      targetPort: http
```

## 7

```bash
kubectl edit deployment presentation
# replica 수정
```

## 8

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-kusc00401
spec:
  containers:
  - name: nginx-kusc00401
    image: nginx:1.14.2
    ports:
    - containerPort: 80
  nodeSelector:
    disk: ssd
```

