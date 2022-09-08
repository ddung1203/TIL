# 백엔드

현재 사용하고 있는 백엔드: Local Backend

> s3, dynamo DB를 이용한 원격 백엔드
> https://www.terraform.io/language/settings/backends/s3

## 테라폼 클라우드 백엔드

```
terraform {
  backend "remote" {
    organization = "example_corp"

    workspaces {
      name = "my-app-prod"
    }
  }
}
```