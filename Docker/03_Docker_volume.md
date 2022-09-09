# Docker 볼륨

방식
- Bind : 볼륨은 도커 데몬이 관리하지 않음
- Volume : 볼륨은 도커 데몬이 관리함

이미지의 `Config.Volumes` 선언되어 있으면, 자동으로 Docker 볼륨이 생성되고 마운트된다.

## 볼륨 방식 마운트

볼륨 : 읽기 - 쓰기가 가능한 빈 저장소를 생성

빈 볼륨 생성

``` bash
docker volume create <NAME>
```

볼륨 목록

``` bash
docker volume ls
```

볼륨 삭제

``` bash
docker volume rm <NAME>
```

사용하지 않는 볼륨 삭제
``` bash
docker volume prune
```

> 사용하지 않는 이란
> 컨테이너에 마운트되지 않은 볼륨

볼륨을 사용한 컨테이너

``` bash
docker run -v <VOL-NAME>:<MOUNTPOINT>[:ro] <IMAGE>
```

> 지정한 볼륨 이름이 없으면 생성

``` bash
docker run --name wp-db -d -e MYSQL_ROOT_PASSWORD=P@ssw0rd -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wpadm -e MYSQL_PASSWORD=P@ssw0rd --restart always --cpus 0.5 --memory 1000m -v wp-db-vol:/var/lib/mysql mysql:5.7
```

## 바인드 방식 마운트
바인드 방식은 컨테이너에게 제공할 볼륨을 호스트의 특정 디렉토리를 지정하는 방식
호스트의 디렉토리를 컨테이너에게 제공 : 미리 데이터를 채워서 제공이 가능

``` bash
docker run -v <ABSOLUTE_PATH>:<MOUNTPOINT>[:ro] <IMAGE>
```

디렉토리 전체 마운트
``` bash
docker run -d -v /home/vagrant/contents:/usr/local/apache2/htdocs httpd
```

**파일 마운트**
``` bash
docker run -d -v /home/vagrant/contents/hello.html:/usr/local/apache2/htdocs/hello.html httpd
```

## 사용 용도
- 바인드 : 설정파일, 기타 파일을 제공하기 위한 목적
- 볼륨 : 데이터를 저장하기 위한 빈 디렉토리 제공하기 위한 목적