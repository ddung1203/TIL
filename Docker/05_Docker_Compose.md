# Docker Compose

Docker IaC

`docker-compose` -> `docker compose`
`docker-compose.yaml` 또는 `docker-compose.yml`

## 예제 - 1
`docker-compose.yaml`

``` yaml
version: '3'

services:
	web:
		image: httpd
```

실행
``` bash
docker compose up -d
```

프로젝트 목록 확인
``` bash
docker compose ls
```

서비스 목록(컨테이너)
``` bash
docker compose ps
```

삭제
``` bash
docker compose down
```

## 예제 - 2
`docker-compose.yaml`
``` yaml
version: '3'

services:
  web:
    image: httpd
    restart: always
    ports:
      - 80:80
    environment:
      MSG: Joongseok's World
    volumes:
      - web-contents:/var/www/html
    networks:
      - web-net
  web2:
    image: nginx
    networks:
      - web-net

volumes:
  web-contents:

networks:
  web-net:
```

``` bash
docker compose up -d
```

``` bash
docker compose exec web bash

> apt update; apt install curl
> curl web2
```

> Docker compose로 배포한 컨테이너는 서로 이름으로 통신가능

## 예제 - 3

`docker-compose.yaml`
``` yaml
version: '3'

services:
	myflask:
		build: ./hello-flask
	mydjango:
		build: ./hello-django
```

``` bash
cp -r ~/python/hello-django .
cp -r ~/python/hello-flask .
```