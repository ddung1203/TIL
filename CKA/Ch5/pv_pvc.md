# Persistent Volume

## 문제

`PV 만들기`

```
◾ 작업 클러스터 : hk8s
- pv001라는 이름으로 size 1Gi, access mode ReadWriteMany를 사용하여 persistent volume을 생성합니다.
- volume type은 hostPath이고 위치는 /tmp/app-config입니다.
```

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv001
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  # volume types
  # ex) nfs, hostPath
  hostPath:
    path: /tmp/app-config
```

# Persistent Volume Claim

`PVC를 사용하는 애플리케이션 Pod 운영`

```
작업 클러스터 : k8s
- 다음의 조건에 맞는 새로운 PersistentVolumeClaim 생성하시오.
  - Name: pv-volume
  - Class: app-hostpath-sc
  - Capacity: 10Mi
- 앞서 생성한 pv-volume PersistentVolumeClaim을 mount하는 Pod 를 생성하시오.
  - Name: web-server-pod
  - Image: nginx
  - Mount path: /usr/share/nginx/html
- Volume에서 ReadWriteMany 액세스 권한을 가지도록 구성합니다.
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pv-volume
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Mi
  storageClassName: app-hostpath-sc
---
apiVersion: v1
kind: Pod
metadata:
  name: web-server-pod
spec:
  containers:
    - name: web-server-pod
      image: nginx
      volumeMounts:
      - mountPath: "/usr/share/nginx/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: pv-volume
```