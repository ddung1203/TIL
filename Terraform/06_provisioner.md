# 프로비저너

```
resource "aws_instance" "web" {
  # ...

  provisioner "local-exec" {
    command = "echo The server's IP address is ${self.private_ip}"
  }
}
```

프로비저너 종류
- file: 파일 복사

```
resource "aws_instance" "web" {
  # ...

  # Copies the myapp.conf file to /etc/myapp.conf
  provisioner "file" {
    source      = "conf/myapp.conf"
    destination = "/etc/myapp.conf"
  }
}
```

- local_exec: 로컬 머신에서 명령 실행

```
resource "aws_instance" "web" {
  # ...

  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> private_ips.txt"
  }
}
```

- remote_exec: 원격 머신에서 명령 실행

```
resource "aws_instance" "web" {
  # ...

  # Establishes connection to be used by all
  # generic remote provisioners (i.e. file/remote-exec)
  connection {
    type     = "ssh"
    user     = "root"
    password = var.root_password
    host     = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "puppet apply",
      "consul join ${aws_instance.web.private_ip}",
    ]
  }
}
```

## 프로비저너 연결

SSH 연결이 필요함

- file
- remote_exec

```
  provisioner "file" {
	  connection {
	    type     = "ssh"
	    user     = "root"
	    password = "${var.root_password}"
	    host     = "${var.host}"
	  }
  }
```

```
  provisioner "file" {
  }

  provisioner "file" {
  }

  connection {
  }
```

## Taint
Taint? 오염되다, 문제있다, 오류

리소스를 생성/변경하다가 오류가 발생하면, 해당 리소스를 Taint 처리

`terraform taint <RESOURCE>`

`terraform untaint <RESOURCE>`

## Ansible 실행 방법

1. AMI 이미지 내에 ansible을 미리 설치
	- file로 플레이북 및 파일 복사
	- remote-exec로 실행
	- ansible-playbook a.yaml -c local

2. 로컬에서 실행
	- 로컬에 ansible이 설치되어 있어야 함
	- local-exec로 인벤토리 생성
		- self.public_ip
	- local-exec로 ansible-playbook 실행

```
  connection {
    user        = "ec2-user"
    host        = self.public_ip
    private_key = file("/home/vagrant/.ssh/id_rsa")
    timeout     = "1m"
  }

  provisioner "local-exec" {
    command = "echo ${self.public_ip} ansible_user=ec2-user > inven.ini"
  }

  provisioner "local-exec" {
    command = "ansible-playbook -i inven.ini web_install.yaml -b"
  }
```