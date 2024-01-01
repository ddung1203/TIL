# Secret

## 문제

`Create a Kubernetes secret`

```
◾ 작업 클러스터 : k8s
Name: super-secret
password: bob
Create a pod named pod-secrets-via-file, using the redis Image, which mounts a secret named super-secret at /secrets.
Create a second pod named pod-secrets-via-env, using the redis Image, which exports password as CONFIDENTIAL
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: super-secret
data:
  Password: Ym9iCg==
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-secrets-via-file
spec:
  containers:
    - name: pod-secrets-via-file
      image: redis
      volumeMounts:
        - name: foo
          mountPath: "/secrets"
  volumes:
    - name: foo
      secret:
        secretName: super-secret
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-secrets-via-env
spec:
  containers:
    - name: pod-secrets-via-env
      image: redis
      env:
      - name: CONFIDENTIAL
        valueFrom:
          secretKeyRef:
            name: super-secret
            key: Password
```