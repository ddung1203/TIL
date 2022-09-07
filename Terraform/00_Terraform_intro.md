# Terraform

HCL: Hashicorp Configuration Language

DSL: Domain Specific Language

Workflow

- 코드 작성 (Write)
- 계획 (plan)
- 적용 (Apply)

> 프로바이더 : https://registry.terraform.io/browse/providers

## 설치

> Terraform 설치 : https://www.terraform.io/downloads

``` bash
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

> aws-cli 설치 : https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html

``` bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

``` bash
aws configure
aws sts get-caller-identity
```