# 반복

> https://www.terraform.io/language/meta-arguments/count

```
resource "aws_instance" "server" {
  count = 4 # create four similar EC2 instances

  ami           = "ami-a1b2c3d4"
  instance_type = "t2.micro"

  tags = {
    Name = "Server ${count.index}"
  }
}
```

## count.index

```
resource "aws_eip" "app_server_eip" {
  count = var.instance_count

  instance = aws_instance.app_server[count.index].id
  vpc      = true

  tags = local.common_tags
}
```

> output 블록에서는 count argument를 사용할 수 없음

## modulo / modular

`%`

M % N = R(Remain: 나머지) M mod N = R

0 % 4 = 0
1 % 4 = 1
2 % 4 = 2
3 % 4 = 3
4 % 4 = 0
5 % 4 = 1
6 % 4 = 2
7 % 4 = 3

```
  subnet_id              = module.app_vpc.public_subnets[count.index % length(module.app_vpc.public_subnets)]
```