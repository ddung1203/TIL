# Kube-dns

- k8s에서 사용하는 DNS
- 각 Pod 의 네임서버는 kube-dns로 정의되어 있다.
  - `/etc/resolf.conf`

## 문제

`Service and DNS Lookup`

```
 작업 클러스터 : k8s
- image nginx를 사용하는 resolver pod를 생성하고 resolver-service라는 service를 구성합니다.
- 클러스터 내에서 service와 pod 이름을 조회할 수 있는지 테스트합니다.
- dns 조회에 사용하는 pod 이미지는 busybox:1.28이고, service와 pod 이름 조회는 nlsookup을 사용합니다.
- service 조회 결과는 /var/CKA2022/nginx.svc에 pod name 조회 결과는 /var/CKA2022/nginx.pod 파일에 기록합니다
```

```bash
kubectl run test-nslookup --image=busybox:1.28 -it --restart=Never --rm -- nslookup nginx-resolver-service > /var/CKA2022/nginx.svc

kubectl run test-nslookup --image=busybox:1.28 -it --restart=Never --rm -- nslookup nginx-resolver-service.default.pod.cluster.local > /var/CKA2022/nginx.pod
```