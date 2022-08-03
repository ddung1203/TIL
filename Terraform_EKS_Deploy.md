# Terraform EKS 배포

작업환경

- Terraform
- Kubectl
- AWS-IAM-AUTHENTICATOR
- Helm
- AWS Configuration

Terraform Registry

```bash
git clone https://github.com/ddung1203/StudyRoom.git
cd StudyRoom/terraform_eks/terraform/dev
```

Terraform Initialization

```bash
terraform init
```

Terraform Apply

```bash
terraform apply -var-file fixture.tc1.tfvars
```

.kube/config 생성

```bash
aws eks update-kubeconfig --region ap-northeast-2 --name eks-autoscaling-tc1
```

Elasticsearch - 3개, Kibana, Fluentd 노드그룹 생성 완료

EKS Cluster AutoScaler 생성 완료
