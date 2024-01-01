# Node 관리

## Node 스케줄링 중단 및 허용

- cordon
  - 스케줄링 중단
- drain
  - 노드 비움
  - `--ignore-daemonsets`
  - `--force`
- uncordon
  - 스케줄링 허용

## 문제

`노드 비우기`
```
◾ 작업 클러스터 : k8s
k8s-worker2 노드를 스케줄링 불가능하게 설정하고, 해당 노드에서 실행 중인 모든 Pod을 다른 node로 reschedule 하세요.
```

```bash
kubectl drain k8s-worker2 --ignore-daemonsets --force --delete-emptydir-data
```

```bash
kubectl uncordon k8s-worker2
```