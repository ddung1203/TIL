# AWS EKS

```bash
aws configure
```

```bash
eksctl create cluster --name myeks --nodes=3 --region=ap-northeast-2
```

> 안되는 것들 Load Balancer Service = class lb -> nlb Ingress: X kubectl top: X -> HPA X

## YAML 파일을 이용한 EKS 배포

```bash
mkdir aws-eks
cd aws-eks
```

`myeks.yaml`

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: myeks-custom
  region: ap-northeast-2
  version: "1.24"

# AZ
availabilityZones: ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]

# IAM OIDC & Service Account
# EKS와 AWS IAM 계정 연동
iam:
  withOIDC: true # EKS 입장에서 AWS IAM은 외부 서버
  serviceAccounts:
    - metadata:
        name: aws-load-balancer-controller
        namespace: kube-system
      wellKnownPolicies:
        awsLoadBalancerController: true
    - metadata:
        name: ebs-csi-controller-sa # SA 계정의 이름
        namespace: kube-system
      wellKnownPolicies: # 해당 기능을 켜면 계정에 해당되는 정책 자동 부여
        ebsCSIController: true
    - metadata:
        name: cluster-autoscaler # SA 계정의 이름
        namespace: kube-system
      wellKnownPolicies:
        autoScaler: true

# Managed Node Groups
managedNodeGroups: # 워커 노드의 그룹
  # On-Demand Instance
  - name: myeks-ng1
    instanceType: t3.medium
    minSize: 2
    desiredCapacity: 3
    maxSize: 4
    privateNetworking: true # private network에 배치하기 위함함
    ssh:
      allow: true
      publicKeyPath: ./keypair/myeks.pub
    availabilityZones: ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
    iam: # 3가지 정책을 node에도 부여
      withAddonPolicies:
        autoScaler: true
        albIngress: true
        cloudWatch: true
        ebs: true

# Fargate Profiles
# EC2 인스턴스를 사용하지 않는 형태
fargateProfiles:
  - name: fg-1
    selectors:
      - namespace: dev
        labels:
          env: fargate

# CloudWatch Logging
# 컨트롤 플레인이 숨겨져 있어 직접 관리하지 못함
cloudWatch: # 컨트롤 플레인의 구성 요소들은 로그를 수집하지 못함
  clusterLogging:
    enableTypes: ["*"] # 컨트롤 플레인에서 수집할 수 있는 모든 것을 수집
```

```bash
mkdir keypair
ssh-keygen -f keypair/myssh
```

```bash
eksctl create cluster -f myeks.yaml
```

## EKS LoadBalancer

| 기능                  | Application LoadBalancer | Network LoadBalancer | Classic LoadBalancer      |
| --------------------- | ------------------------ | -------------------- | ------------------------- |
| 유형                  | 계층7                    | 계층4                | 계층4/7                   |
| 대상 유형             | IP, 인스턴스, Lambda     | IP, 인스턴스, ALB    | -                         |
| 흐름/프록시 동작 종료 | 예                       | 예                   | 예                        |
| 프로토콜 리스너       | HTTP, HTTPS, gRPC        | TCP, UDP, TLS        | TCP, SSL/TLS, HTTP, HTTPS |
| 다음을 통해 연결 가능 | VIP                      | VIP                  | -                         |

## NLB for LoadBalancer Service

EKS에서 LoadBalancer를 생성하면 기본적으로 Classic LoadBalancer가 생성된다.

EC2 인스턴스를 사용하는 경우 Classic LoadBalancer는 정상 작동하지만 Fargate를 사용하는 경우에는 Classic LoadBalancer가 작동하지 않는다.

Classic LoadBalancer는 반드시 EC2 인스턴스에만 연결이 될 수 있는데 Fargate 같은 경우에는 EC2 인스턴스가 생성되지 않기 때문이다.

> https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/network-load-balancing.html > https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/alb-ingress.html > https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/aws-load-balancer-controller.html

### AWS Load Balancer Controller 설치

```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update
```

```bash
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=myeks-custom --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller --set image.repository=602401143452.dkr.ecr.ap-northeast-2.amazonaws.com/amazon/aws-load-balancer-controller
```

## 샘플 코드

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myweb-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb
          ports:
            - containerPort: 8080
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myweb-svc-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "external"
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "instance"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

**EC2 인스턴스에 NLB 설정**

```yaml
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "instance"
```

로드밸런서를 만들 때 annotation을 붙여야한다.

external은 외부용이라는 의미이며, nlb-target-type은 NLB가 생성되고 NLB의 타겟이되는 대상은 인스턴스라는 의미이다.

정확히는 EC2 인스턴스의 NodePort가 타겟이 된다. 로드밸런서 서비스는 NodePort를 사용한다.

그리고 EC2 인스턴스 내부에 파드가 존재하며 파드 안에는 App이 실행되고 있다.

즉, NLB를 통해 파드 내의 App에 부하 분산한다.

**Fargate에 NLB 설정**

```yaml
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
```

상기는 Fargate를 위한 aws-load-balancer-nlb-target-type이다.

IP 타입은 파드에 NLB가 직접적으로 연결되는 방식이다.
즉, Fargate에 사용하기 위해 만들어 놓은 것이다.

인스턴스가 private network에 배치되었으므로 퍼블릭 IP를 가지지 않으며 private 서브넷에 배치되어 있다.

하기와 같이 정리가 가능하다.

- service.beta.kubernetes.io/aws-load-balancer-nlb-target-type
  - instance: EC2 타겟
  - ip: Pod 타겟(Fargate)
- service.beta.kubernetes.io/aws-load-balancer-scheme
  - internal: 내부
  - internet-facing: 외부

## Ingress for ALB

L7에서 애플리케이션 트래픽을 로드 밸런싱하려면 Kubernetes ingress를 배포해야한다. 이는 AWS Application Load Balancer를 프로비저닝한다.

Ingress도 마찬가지로 AWS LoadBalancer Controll이 설치되어 있어야 한다.

> https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/alb-ingress.html

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myweb-ing
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/target-type: instance
    alb.ingress.kubernetes.io/scheme: internet-facing
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myweb-svc-lb
                port:
                  number: 80
```

- alb.ingress.kubernetes.io/target-type
  - instance: EC2 타겟
  - ip: Pod 타겟(Fargate)
- alb.ingress.kubernetes.io/scheme
  - internal: 내부
  - internet-facing: 외부

## EBS for CSI

CSI Driver란, Container Storage Interface(CSI)는 Kubernetes, Mesos 같은 Container Orchestration System과 Storage를 제어하는 Plugin 사이의 Interface를 의미한다.

- EBS 스냅샷
- EBS 크기 변경

> https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/managing-ebs-csi.html

```bash
eksctl get iamserviceaccount --cluster myeks-custom

NAMESPACE       NAME                            ROLE ARN
kube-system     aws-load-balancer-controller    arn:aws:iam::065144736597:role/eksctl-myeks-custom-addon-iamserviceaccount-Role1-11N0OKMVG2DYY
kube-system     aws-node                        arn:aws:iam::065144736597:role/eksctl-myeks-custom-addon-iamserviceaccount-Role1-CLMK7A6K5NL3
kube-system     cluster-autoscaler              arn:aws:iam::065144736597:role/eksctl-myeks-custom-addon-iamserviceaccount-Role1-1S02W28MZOSL4
kube-system     ebs-csi-controller-sa           arn:aws:iam::065144736597:role/eksctl-myeks-custom-addon-iamserviceaccount-Role1-15HLE8HBOD9CN
```

```bash
eksctl create addon --name aws-ebs-csi-driver --cluster myeks-custom --service-account-role-arn  arn:aws:iam::065144736597:role/eksctl-myeks-custom-addon-iamserviceaccount-Role1-15HLE8HBOD9CN --force
```

## Metrics Server

> https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/metrics-server.html

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Cluster Autoscaler

Auto Scaling으로 노드 풀의 크기가 감소하면 replication controller에서 관리하지 않는 삭제된 노드의 모든 Pod가 손실된다.

노드 풀의 크기를 수동으로 줄이면 삭제된 노드의 모든 Pod가 다른 노드에서 다시 시작된다.

노드 풀의 크기를 늘리면 기존 Pod가 새 노드로 이동된다.

-> FALSE

클러스터 확장과 축소는 드물게 발생해야 하는 작업이다.

Auto Scaling은 pending중인 scale-up 이벤트를 확인한다.

Pod 조건에 따른 노드 삭제 예방

- Controller에서 관리하지 않는 Pod
  - Deployment, ReplicaSet, Job, StatefulSet 등에 속하지 않는 Pod
- local storage를 가지고 있는 Pod
- Pod가 다른 노드에서 실행되지 않도록 constraint rule에 의해 제한된 Pod

노드 삭제를 방지하기 위해 명시적으로 설정

- cluster-autoscaler.kubernetes.io/safe-to-evict=False
  - Pod를 제거할 수 없다는 사실을 Pod 수준에서 Auto Scaler에 알려줌
  - 클러스터가 축소될 때 해당 Pod를 실행중인 노드는 삭제 대상으로 선택되지 않는다.
- PodDisruptionBudget
  - 언제든지 사용 가능한 replicas 수를 지정할 수 있다.
  - ex) 3개의 replica가 있는 Deployment에서 PodDisruptionBudget이 2로 설정되어 있다면, 한 번에 하나의 replica만 제거하거나 중단할 수 있다.
- kubernetes.io/scale-down-disabled=True
  - 노드 단에서 설정
  - 축소 작업에서 항상 제외

### 수동 스케일링

```bash
eksctl scale nodegroup --name myeks-ng1 --cluster myeks-custom --nodes 2
```

### 자동 스케일링

> https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/autoscaling.html

```bash
curl -o cluster-autoscaler-autodiscover.yaml https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
```

`cluster-autoscaler-autodiscover.yaml`

```yaml
163: - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/myeks-custom
```

```bash
kubectl apply -f cluster-autoscaler-autodiscover.yaml
```

```bash
kubectl patch deployment cluster-autoscaler -n kube-system -p '{"spec":{"template":{"metadata":{"annotations":{"cluster-autoscaler.kubernetes.io/safe-to-evict": "false"}}}}}'
```

```bash
kubectl -n kube-system edit deployment.apps/cluster-autoscaler
```

```
      - command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/myeks-custom
        - --balance-similar-node-groups
        - --skip-nodes-with-system-pods=false
        image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.22.6
```

수정

```
--node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/myeks-custom
--balance-similar-node-groups
--skip-nodes-with-system-pods=false
image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.22.2
```

```bash
kubectl set image deployment cluster-autoscaler -n kube-system cluster-autoscaler=k8s.gcr.io/autoscaling/cluster-autoscaler:v1.22.2
```

### 샘플 코드

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myweb-deploy
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: myweb
          image: ghcr.io/c1t1d0s7/go-myweb:alpine
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 200m
              memory: 200M
            limits:
              cpu: 200m
              memory: 200M
```

## CloudWatch Container Insight

안정적인 서비스의 운영을 위해서는 서비스의 CPU, Memory 등을 모니터링하고 Application Log를 확인하는 것이 중요하다.

쿠버네티스에서도 마찬가지로 Cluster, Namespace, Service, Pod 등에 대한 모니터링과 필요에 따라 Application 로그 수집이 필요하다.

AWS에서 제공하는 Container Insights와 로그 수집기인 Fluent Bit로 로그를 수집하고 모니터링 할 수 있다.

- Container Insights (모니터링)
  - ECS, EKS Cluster에 대하여 CPU, Memory, 디스크, 네트워크 등 리소스에 대한 지표를 자동으로 수집
  - CloudWatch agent로 수집된 지표를 사용하여 CloudWatch DashBoard 구성 가능
- Fluent-bit (로깅)
  - fluentd보다 Memory를 적게 사용하는 경량화된 로그 수집기, 전달자 역할 수행
  - 수집된 지표를 Output Plugin을 통해 CloudWatch Logs, ElasticSearch, S3 등으로 전달 가능

> https://docs.aws.amazon.com/ko_kr/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-EKS-quickstart.html > https://github.com/git-for-windows/git/releases/download/v2.36.1.windows.1/Git-2.36.1-64-bit.exe

### CloudWatch Container 로그 수집하기

```bash
ClusterName=myeks-custom
RegionName=ap-northeast-2
FluentBitHttpPort='2020'
FluentBitReadFromHead='Off'
[[ ${FluentBitReadFromHead} = 'On' ]] && FluentBitReadFromTail='Off'|| FluentBitReadFromTail='On'
[[ -z ${FluentBitHttpPort} ]] && FluentBitHttpServer='Off' || FluentBitHttpServer='On'
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluent-bit-quickstart.yaml | sed 's/{{cluster_name}}/'${ClusterName}'/;s/{{region_name}}/'${RegionName}'/;s/{{http_server_toggle}}/"'${FluentBitHttpServer}'"/;s/{{http_server_port}}/"'${FluentBitHttpPort}'"/;s/{{read_from_head}}/"'${FluentBitReadFromHead}'"/;s/{{read_from_tail}}/"'${FluentBitReadFromTail}'"/' | kubectl apply -f -
```

```bash
kubectl get po -A
NAMESPACE           NAME                                            READY   STATUS             RESTARTS   AGE
amazon-cloudwatch   cloudwatch-agent-4z2cf                          1/1     Running            0          117s
amazon-cloudwatch   cloudwatch-agent-77sh4                          1/1     Running            0          117s
amazon-cloudwatch   cloudwatch-agent-rp6gj                          1/1     Running            0          117s
amazon-cloudwatch   fluent-bit-dzvch                                1/1     Running            0          116s
amazon-cloudwatch   fluent-bit-s8ls5                                1/1     Running            0          116s
amazon-cloudwatch   fluent-bit-xlm2f                                1/1     Running            0          116s
```

상기와 같이 amazon-cloudwatch라는 네임스페이스가 있고 cloudwatch-agent와 fluent-bit가 있다.

fluent-bit가 로그를 수집하고 그 로그를 cloudwatch-agent가 cloudwatch로 전송시킨다.

CloudWatch의 Container Insights 내에서 확인 가능하다.

## Fargate

AWS Fargate는 서버리스형 컨테이너 서비스로서 Amazon EKS 클러스터의 일부로, Kubernetes 파드로 실행되는 컨테이너에 대해 적절한 크기의 온디맨드 컴퓨팅 용량을 제공한다.

컨테이너를 실행하는 리소스 비용만 초단위에 따라 지불하면 된다.

Fargate를 이용해 EC2 인스턴스를 사용하지 않고 파드를 실행할 수 있다.
우리가 EKS를 사용할 때 컨트롤 플레인은 AWS에서 관리해주지만, 워커 노드들은 오토 스케일링 그룹을 이용해 EC2 인스턴스를 배포해서 사용한다.

→ 즉, EC2 인스턴스의 관리는 사용자의 몫이다.

Fargate는 EC2 인스턴스를 추상화시켰기 때문에 사용자가 관리할 필요가 없다. 사용자는 운영체제 버전 업데이트, 패치 등을 할 필요없이 오로지 파드만을 관리하면 된다.

> Fargate 사용 시 상기 LoadBalancer 부분을 참고하여 작성한다.

<br>

> https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/fargate.html

```bash
kubectl create ns dev
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myfg
  namespace: dev
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myfg
  template:
    metadata:
      labels:
        app: myfg
        env: fargate
    spec:
      containers:
        - name: myfg
          image: ghcr.io/c1t1d0s7/go-myweb
          resources:
            limits:
              memory: "128Mi"
              cpu: "500m"
          ports:
            - containerPort: 8080
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysvc
  namespace: dev
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "external"
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  selector:
    app: myfg
  ports:
    - port: 80
      targetPort: 8080
  type: LoadBalancer
```

Fargate는 EC2 인스턴스 관리 콘솔에서 확인할 수 없다.

## VPA

> https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/vertical-pod-autoscaler.html

사전 요구 사항

- openssl 1.1.1 이상
- metrics-server

```bash
git clone https://github.com/kubernetes/autoscaler.git
```

```bash
cd autoscaler/vertical-pod-autoscaler/
```

```bash
/hack/vpa-up.sh
```

```bash
kubectl get pods -n kube-system
```

#### VPA 예제

```bash
kubectl apply -f examples/hamster.yaml
```

## 클러스터 삭제

```bash
eksctl delete cluster -f .\myeks.yaml --force --disable-nodegroup-eviction
```
