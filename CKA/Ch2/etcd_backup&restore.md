# etcd backup & restore

- etcd backup
  - etcd db를 하나의 스냅샷 파일로 생성
- etcd restore
  - 별도의 db 공간으로 다시 원래대로 복원


## 문제

`ETCD backup`
```
■ 작업 클러스터: k8s
https://127.0.0.1:2379에서 실행 중인 etcd의 snapshot을 생성하고 snapshot을 /data/etcd-snapshot.db에 저장합니다.
그런 다음 /data/etcd-snapshot-previous.db에 있는 기존의 이전 스냅샷을 복원합니다.
etcdctl을 사용하여 서버에 연결하기 위해 다음 TLS 인증서/키가 제공됩니다.
• CA certificate: /etc/kubernetes/pki/etcd/ca.crt
• Client certificate: /etc/kubernetes/pki/etcd/server.crt
• Client key: /etc/Kubernetes/pki/etcd/server.key
```

https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/


```bash
sudo ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /data/etcd-snapshot.db
```

```bash
sudo ETCDCTL_API=3 etcdctl --data-dir /var/lib/etcd-previous snapshot restore /data/etcd-snapshot-previous.db
```

`/etc/kubernetes/manifests/etcd.yaml`
```yaml
# hostPath 변경
  - hostPath:
      path: /var/lib/etcd-previous
      type: DirectoryOrCreate
    name: etcd-data
```