# etcd Backup

## Kubernetes Backup

1. 재해로부터 복구
2. 디버깅, 개발, 준비 또는 주요 업그레이드 전 환경 복제
3. 한 환경에서 다른 환경으로 Kubernetes 클러스터 마이그레이션

Linux etcd install
``` bash
ETCD_VER=v3.5.8

# choose either URL
GOOGLE_URL=https://storage.googleapis.com/etcd
GITHUB_URL=https://github.com/etcd-io/etcd/releases/download
DOWNLOAD_URL=${GOOGLE_URL}

rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
rm -rf /tmp/etcd-download-test && mkdir -p /tmp/etcd-download-test

curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
tar xzvf /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz -C /tmp/etcd-download-test --strip-components=1
rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz

/tmp/etcd-download-test/etcd --version
/tmp/etcd-download-test/etcdctl version
/tmp/etcd-download-test/etcdutl version

sudo cp etcd /usr/local/bin/
sudo cp etcdctl /usr/local/bin/
sudo cp etcdutl /usr/local/bin/
```

## 백업

| etcdctl 명령 옵션 | etcd 프로세스 실행 옵션 | 값 | 커맨드로 빨리 찾기 |
| --- | --- | --- | --- |
| --cacert | --trusted-ca-file | /etc/kubernetes/pki/etcd/ca.crt | `ps -ef | grep etcd | grep trusted` |
| --cert | --cert-file | /etc/kubernetes/pki/etcd/server.crt | `ps -ef | grep etcd | grep "\--cert"` |
| --key | --key-file | /etc/kubernetes/pki/etcd/server.key | `ps -ef | grep etcd | grep "\--key"` |

상기 표와 같이 Kubernetes의 인증서를 작성한다.

``` bash
sudo etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
snapshot save /home/vagrant/backup/$(date "+%Y-%m-%d")
```

## 복원

| etcdctl 명령 옵션 | etcd 프로세스 실행 옵션 | 값 | 커맨드로 빨리 찾기 |
| --- | --- | --- | --- |
| --cacert | --trusted-ca-file | /etc/kubernetes/pki/etcd/ca.crt | `ps -ef | grep etcd | grep trusted` |
| --cert | --cert-file | /etc/kubernetes/pki/etcd/server.crt | `ps -ef | grep etcd | grep "\--cert"` |
| --key | --key-file | /etc/kubernetes/pki/etcd/server.key | `ps -ef | grep etcd | grep "\--key"` |
| --initial-advertise-peer-urls | --initial-advertise-peer-urls | https://192.168.56.100:2380 | `ps -ef | grep etcd | grep initial` |
| --initial-cluster=master | --initial-cluster=kubeadm-node1 | https://192.168.56.100:2380 | `ps -ef | grep etcd | grep initial` |
| --data-dir | --data-dir | /var/lib/etcd | `ps -ef | grep etcd | grep "\--data-dir"` |
| --name | --name | kubeadm-node1(마스터노드 이름) | `ps -ef | grep etcd | grep "\--name"` |

``` bash
sudo etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
--initial-advertise-peer-urls=https://192.168.56.100:2380 \
--initial-cluster=kubeadm-node1=https://192.168.56.100:2380 \
--data-dir=/var/lib/etcd \
--name=kubeadm-node1 \
snapshot restore /home/vagrant/backup/2023-04-30 
```