# Docker 관리

docker ps (= docker container ls)
docker images (= docker image ls)

## 최신 docker 명령 구조

``` bash
docker container <sub-command>
```

``` bash
docker image <sub-command>
```

``` bash
docker network <sub-command>
```

``` bash
docker volume <sub-command>
```

## 이미지

로컬 이미지 확인

``` bash
docker images
```

Docker Hub 이미지 검색
``` bash
docker search <TERM>
```

이미지 풀링
``` bash
docker pull <IMAGE>:<TAG>
```

> latest 태그는 가능하면 사용하지 않도록 한다.

이미지 삭제
``` bash
docker rmi <IMAGE>
```

이미지 상세정보 확인
``` bash
docker inspect <IMAGE>
```

`ContainerConfig` vs. `Config`

- `ContainerConfig` : 이미지 최초 생성할 때 사용했던 설정
- `Config` : 가장 최근에 이미지 생성시 사용했던 설정
- `Config`
	- `ENV`
	- `Cmd`
	- `ExposedPorts`
	- `WorkingDir`
	- `Volumes`
	- `Entrypoint`

``` bash
docker inspect centos:7 --format '{{ .Config.Cmd }}'
```

이미지 저장/아카이브
``` bash
docker save <IMAGE> -o <FILE>
```

이미지 가져오기
``` bash
docker load -i <FILE>
```

## 컨테이너
create -> start -> (pause) -> (unpause) -> (kill) -> (restart) -> stop -> rm run ---------->

컨테이너 목록
현재 실행중인 컨테이너 목록
``` bash
docker ps
```

모든 컨테이너 목록
``` bash
docker ps -a
```

컨테이너 실행
``` bash
docker run <IMAGE>
docker run --name <NAME> <IMAGE>
```

> 동일한 이름의 컨테이너 생성을 불가하다.

- 옵션 없음: Docker Daemon --stdout/stderr-> Docker Clinet
	- --name 옵션 X
- -it: Attach 모드(stdin/stdout/stderr 연결) -> Foreground
	- -i: stdin 유지
	- -t: Terminal 할당
	- ctrl-p-q
		- docker attach 명령으로 연결 가능
- -d: Detach 모드(stdin/stdout/stderr 연결 해제) -> Background 실행
- -itd

> 하나의 컨테이너에는 하나의 Application만 실행 원칙

재시작 정책

> https://docs.docker.com/config/containers/start-containers-automatically/

``` bash
docker run --restart <no|always|on-failure|unless-stopped> <IMAGE>
```

이미지 풀 정책
``` bash
docker run --pull <missing|always|never> <IMAGE>
```

컨테이너의 프로세스 목록 확인
``` bash
docker top <CONTAINER>
```

> 실행중인 컨테이너만 확인

컨테이너에서 (추가)애플리케이션 실행

```
docker exec <CONTAINER> <COMMAND>
```

```
docker exec -it a8 bash
```

```
docker exec a8 cat /etc/httpd/conf/httpd.conf
```


컨테이너 리소스 사용량 확인

```
docker stats
docker stats --no-stream
```

컨테이너 (cpu/memory) 리소스 제한
```
docker run --cpus 0.1 --memory 100m ubuntu sha256sum /dev/zero
```

컨테이너 리소스 제한 변경
```
docker update --cpus 0.2 da
docker update --memory 200m da
```

컨테이너 로그(stdout/stderr) 확인
```
/var/lib/docker/container/<ID>/<ID>-json.log
```
```
docker logs <CONTAINER>
```

> 컨테이너를 삭제하면 로그도 삭제됨

환경변수
```
docker run -e A=100 ubuntu
docker run -d -e MYSQL_ROOT_PASSWORD=P@ssw0rd -e MYSQL_DATABASE=wordpress mysql:5.7
```

> 일부 이미지는 실행시 환경 변수가 필요함

컨테이너 정보 확인
```
docker inspect <CONTAINER>
```

컨테이너 IP 확인
```
docker inspect 16a -f '{{ .NetworkSettings.IPAddress }}'
```

컨테이너 Discovery
```
docker run --name mysqldb -d -e MYSQL_ROOT_PASSWORD=P@ssw0rd mysql:5.7 
```
```
docker run -it --link mysqldb ubuntu bash

> cat /etc/hosts
>> 172.17.X.X mysqldb
```
```
docker run -it --link mysqldb:xyz ubuntu bash

> cat /etc/hosts
>> 172.17.X.X mysqldb xyz
```
```
docker run -it --link mysqldb:xyz mysql:5.7 mysql -h xyz -u root -p
```

컨테이너의 포트를 호스트의 포트로 포워딩 (포트 포워딩)
```
docker run -p <HOST>:<CONTAINER> <IMAGE>
```
```
docker run -d -p 80:80 httpd
```

## Wordpress + MySQL

``` bash
docker run --name wp-db -d -e MYSQL_ROOT_PASSWORD=P@ssw0rd -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wpadm -e MYSQL_PASSWORD=P@ssw0rd --restart always --cpus 0.5 --memory 1000m mysql:5.7
```

``` bash
docker run --name wp-web -d --link wp-db:mysql -e WORDPRESS_DB_HOST=mysql -e WORDPRESS_DB_USER=wpadm -e WORDPRESS_DB_PASSWORD=P@ssw0rd -e WORDPRESS_DB_NAME=wordpress --restart always --cpus 0.5 --memory 500m -p 80:80 wordpress:5-apache
```