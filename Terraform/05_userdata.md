# 사용자 데이터

```
resource "aws_instance" "app_web" {
  ...
  user_data = <<-EOF
    #!/bin/sh
    echo "hello wolrd"
    EOF
  ...
}
```

``` bash
cat <<EOF > a.txt
> a
> b
> c
> d
> EOF
```

```
resource "aws_instance" "app_web" {
  ...
  user_data = file("userdata.sh")
  ...
}
```

`userdata.sh`
```
#!/bin/sh
apt install -y apache2
...
```