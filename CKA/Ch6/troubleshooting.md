# Monitor, Log

## 문제

`Application Log 추출`

```
◾ 작업 클러스터 : kubectl config use-context hk8s
• Pod custom-app의 로그 모니터링 후 'file not found' 오류가 있는 로그 라인 추출(Extract)해서 /var/CKA2022/CUSTOM-LOG001 파일에 저장하시오
```

```bash
kubectl logs pod/custom-app | grep 'file not found' > /var/CKA2022/CUSTOM-LOG001
```

## 문제

`PV 정보 보기`

```
◾ 작업 클러스터 : hk8s
• 클러스터에 구성된 모든 PV를 capacity별로 sort하여 /var/CKA2022/my-pv-list 파일에 저장하시오.
• PV 출력 결과를 sort하기 위해 kubectl 명령만 사용하고, 그 외 리눅스 명령은 적용하지 마시오.
```

```bash
kubectl get pv --sort-by=.spec.capacity.storage > /var/CKA2022/my-pv-list
```

## 문제

`클러스터 리소스 정보 보기`

```
◾ 작업 클러스터 : kubectl config use-context hk8s
• 'name=overloaded-cpu' 레이블을 사용하는 Pod들 중 CPU 소비율이 가장 높은 Pod의 이름을 찾아서 /var/CKA2022/custom-app-log에 기록하시오.
```

```bash
kubectl get pods --show-labels | grep name=overloaded-cpu

kubectl top pods --sort-by=cpu | grep -e campus-01 -e fast-01
```

# App, Cluster, Network Troubleshooting

하기 리스트 단계별로 확인

- runtime
  - Docker Engine
  - containerd
  - CRI-O
- kubelet
- kubeproxy
- cni

## 문제

`Worker Node 동작 문제 해결`

```
◾ 작업 클러스터 : kubectl config use-context hk8s
• Worker Node 동작 문제 해결
• hk8s-w2라는 이름의 worker node가 현재 NotReady 상태에 있습니다. 이 상태의 원인을 조사하고 hk8sw2 노드를 Ready 상태로 전환하여 영구적으로 유지되도록 운영하시오.
```


```bash
$ systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
     Loaded: loaded (/lib/systemd/system/kubelet.service; disabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/kubelet.service.d
             └─10-kubeadm.conf
     Active: active (running) since Sun 2024-01-07 13:53:03 KST; 48min ago
       Docs: https://kubernetes.io/docs/home/
   Main PID: 1309 (kubelet)
      Tasks: 10 (limit: 4516)
     Memory: 110.2M
        CPU: 29.278s
     CGroup: /system.slice/kubelet.service
             └─1309 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubel
```

```bash
$ sudo systemctl enable --now kubelet
Created symlink /etc/systemd/system/multi-user.target.wants/kubelet.service → /lib/systemd/system/kubelet.service.
```

```bash
$ systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
     Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/kubelet.service.d
             └─10-kubeadm.conf
     Active: active (running) since Sun 2024-01-07 13:53:03 KST; 49min ago
       Docs: https://kubernetes.io/docs/home/
   Main PID: 1309 (kubelet)
      Tasks: 10 (limit: 4516)
     Memory: 110.2M
        CPU: 29.496s
     CGroup: /system.slice/kubelet.service
             └─1309 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubel
```

> Systemd 유닛 컨트롤
> 
> `enable`을 하면 재부팅 시 유닛이 실행되고, `start`는 지금 당장 실행된다는 차이가 있다. 따라서, `enable`로 심볼릭 링크를 생성하여 재부팅 시 유닛이 실행되도록 한다.

