# Volume mount - emptyDir

- 동일한 Pod에서 실행되는 컨테이너 간에 파일을 공유할 때 유용

## 문제

`emptyDir Volume을 공유하는 multi-pod 운영`

```
◾ 작업 클러스터 : k8s
-  다음 조건에 맞춰서 nginx 웹서버 pod가 생성한 로그파일을 받아서 STDOUT으로 출력하는 busybox 컨테이너를 운영하시오.
-  Pod Name: weblog
-  Web container:
  -  Image: nginx:1.17
  -  Volume mount : /var/log/nginx
  -  readwrite
-  Log container:
  -  Image: busybox
  -  Command: /bin/sh, -c, "tail -n+1 -f /data/access.log"
  -  Volume mount : /data
  -  readonly
  -  emptyDir 볼륨을 통한 데이터 공유
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: weblog
spec:
  containers:
  - name: web-container
    image: nginx:1.17
    volumeMounts:
    - name: log
      mountPath: /var/log/nginx
  - name: log-container
    image: busybox
    command: ['/bin/sh', '-c', 'tail -n+1 -f /data/access.log']
    volumeMounts:
    - name: log
      mountPath: /data
      readOnly: true
  volumes:
  - name: log
    emptyDir: {}
```

# Volume mount - hostPath

- 노드의 파일시스템의 디렉토리나 파일을 컨테이너에 마운트

## 문제

`HostPath Volume 구성`

```
◾ 작업 클러스터 : k8s
- /data/cka/fluentd.yaml 파일에 다음 조건에 맞게 볼륨 마운트를 설정하시오.
- Worker node의 도커 컨테이너 디렉토리를 동일 디렉토리로 pod에 마운트 하시오.
- Worker node의 /var/log 디렉토리를 fluentd Pod에 동일이름의 디렉토리 마운트하시오.
```

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluentd
        volumeMounts:
        - mountPath: /var/lib/docker/containers
          name: volume-1
        - mountPath: /var/log
          name: volume-2
      volumes:
      - name: volume-1
        hostPath:
          path: /var/lib/docker/containers
      - name: volume-2
        hostPath:
          path: /var/log
```