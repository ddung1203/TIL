# Vagrant
Vagrant란?

운영체제 시스템에 대하여 쉬운 Provisioning을 할 수 있다. 주로 가상머신을 생성하고 관리할 때 사용할 수 있다.
가상머신을 사용자의 요구에 맞게 Host name, IP, Service Install 등 다양한 환경을 미리 설정하고 사용자가 원할 시 해당 시스템을 즉시 사용할 수 있게 해주는 Provisioning 도구이다.
Vagrantfile을 통하여 해당 파일에 가상머신에 대한 설정과 해야할 작업을 미리 정의한 후 virtual box를 통해 Provisioning 할 수 있다. 이렇게 Vagrant를 통해 가상머신을 Provisioning 할 경우 가상머신을 간편하게 생성/삭제/수정할 수 있다.
하이퍼바이저로 VMWare, Hyper-V 등을 사용할 수도 있다.

---

### Vagrantfile 생성

``` bash
vagrant init <IMAGE>
```

### VM 생성 및 부팅
``` bash
vagrant up [VM_NAME]
```

### VM 종료
``` bash
vagrant halt [VM_NAME]
```

### VM 삭제
``` bash
vagrant destroy [VM_NAME]
```

### VM SSH 접속
``` bash
vagrant ssh [VM_NAME]
```

### Vagrantfile 예제
``` YAML
Vagrant.configure("2") do |config|
	# Define VM
	config.vm.define "controller" do |ubuntu|
		ubuntu.vm.box = "ubuntu/focal64"
		ubuntu.vm.hostname = "controller"
		ubuntu.vm.network "private_network", ip: "192.168.100.10"
		ubuntu.vm.provider "virtualbox" do |vb|
			vb.name = "controller"
			vb.cpus = 2
			vb.memory = 2000
		end
	end

	# Define VM
	config.vm.define "node1" do |ubuntu|
		ubuntu.vm.box = "ubuntu/focal64"
		ubuntu.vm.hostname = "node1"
		ubuntu.vm.network "private_network", ip: "192.168.100.11"
		ubuntu.vm.provider "virtualbox" do |vb|
			vb.name = "node1"
			vb.cpus = 2
			vb.memory = 2000
		end
	end

	# Define VM
	config.vm.define "node2" do |ubuntu|
		ubuntu.vm.box = "ubuntu/focal64"
		ubuntu.vm.hostname = "node2"
		ubuntu.vm.network "private_network", ip: "192.168.100.12"
		ubuntu.vm.provider "virtualbox" do |vb|
			vb.name = "node2"
			vb.cpus = 2
			vb.memory = 2000
		end
	end


	config.vm.provision "shell", inline: <<-SHELL
	  sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
	  sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
	  sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
	  systemctl restart ssh
	SHELL
end
```