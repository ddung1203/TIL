# NodePort

## 문제

`Access the Service from outside the CLuster via NodePort`

```
작업 클러스터 : k8s
- 'front-end' deployment의 nginx 컨테이너를 expose하는 'front-end-nodesvc'라는 새 service를 만듭니다.
- Front-end로 동작중인 Pod에는 node의 30200 포트로 접속되어야 합니다.
- 구성 테스트 curl k8s-worker1:30200 연결 시 nginx 홈페이지가 표시되어야 합니다.
```