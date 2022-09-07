# 로컬값

```
locals {
  service_name = "forum"
  owner        = "Community Team"
}
```

```
resource "aws_instance" "example" {
  # ...

  tags = local.service_name
}
```