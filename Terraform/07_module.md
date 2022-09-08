# 모듈

```
module "myvpc" {
	source = 

	...입력 변수...
}
```

```
resource "aws_instance" "web" {

  subnet_id = module.myvpc.<출력값>
}
```

모듈 초기화

``` bash
terraform init
```