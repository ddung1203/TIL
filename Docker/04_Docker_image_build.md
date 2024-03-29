# Docker 이미지 빌드

방법
- `docker commit` 명령
- Dockerfile

## 명령으로 이미지 생성
### `docker diff`

``` bash
docker diff <CONTAINER>
```

기준 이미지 <-> 컨테이너 차이
- A : ADD
- C : CHANGE
- D : DELETE

### `docker commit`

``` bash
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
```

CMD 변경
``` bash
docker commit -c "CMD XXX" CONTAINER [REPOSITORY[:TAG]]
```

ExposedPort 변경
``` bash
docker commit -c "EXPOSE PORT/PROTOCOL" CONTAINER [REPOSITORY[:TAG]]
```

> ExposedPort는 실제 작동여부와 상관 없다.

> CMD /usr/sbin/apache2ctl -D FORECROUND
> /bin/sh -c /usr/sbin/apache2ctl -D FOREGROUND

### `docker cp`
컨테이너 -> 도커 호스트

``` bash
docker cp CONTAINER:SRC_PATH DEST_PATH
```

도커 호스트 -> 컨테이너

``` bash
docker cp SRC_PATH CONTAINER:DEST_PATH
```

/bin/sh -c /usr/sbin/apache2ctl -DFOREGROUND

### 이미지 레이어
레이어의 이유?
저장소 및 네트워크 전송 효율성을 높임

httpd:latest
```
sha256:9c1b6dd6c1e6be9fdd2b1987783824670d3b0dd7ae8ad6f57dc3cea5739ac71e
sha256:1d1a2486e901871ad1257512d588eebb30ae0605d8353abb6635e2d313b2187c
sha256:ec02eb7f3cf4dd78bc518d3a8ccf57f57336ceacb9638303891787ff2ec2e96f
sha256:67bb571b5bd2b65cbdf2c93c6f9dc8e89414055dd7444df617b23466996f3be7
sha256:e83f42350a11889083536c5af330dcf15fd3624f8e956f4086e1f0cfb07ff246
```

myhttpd:latest
```
sha256:9c1b6dd6c1e6be9fdd2b1987783824670d3b0dd7ae8ad6f57dc3cea5739ac71e
sha256:1d1a2486e901871ad1257512d588eebb30ae0605d8353abb6635e2d313b2187c
sha256:ec02eb7f3cf4dd78bc518d3a8ccf57f57336ceacb9638303891787ff2ec2e96f
sha256:67bb571b5bd2b65cbdf2c93c6f9dc8e89414055dd7444df617b23466996f3be7
sha256:e83f42350a11889083536c5af330dcf15fd3624f8e956f4086e1f0cfb07ff246
sha256:4b8c655a2e61d6f017f3a5cc103fe6bbb6f71bba663085fdae697861dd57695a
```

myhttpd:p8080 set
```
sha256:9c1b6dd6c1e6be9fdd2b1987783824670d3b0dd7ae8ad6f57dc3cea5739ac71e
sha256:1d1a2486e901871ad1257512d588eebb30ae0605d8353abb6635e2d313b2187c
sha256:ec02eb7f3cf4dd78bc518d3a8ccf57f57336ceacb9638303891787ff2ec2e96f
sha256:67bb571b5bd2b65cbdf2c93c6f9dc8e89414055dd7444df617b23466996f3be7
sha256:e83f42350a11889083536c5af330dcf15fd3624f8e956f4086e1f0cfb07ff246
sha256:4b8c655a2e61d6f017f3a5cc103fe6bbb6f71bba663085fdae697861dd57695a
sha256:fffe7ea283ae8867d740e17f619c4db845cb0d75fc655809185e582601786521
```

## Dockerfile로 이미지 빌드

### RUN

RUN - execute command, 이미지를 빌드하는 중에 실행할 명령어 지정

``` bash
RUN yum install httpd
```

Exec Form

``` bash
RUN ["yum", "install", "httpd"]
```

exec form에서의 `exec()`는 c언어 함수이자 shell의 기능인데, `exec ls`하면 `ls`가 실행이 된다.

- `/bin/sh -c`

Docker 컨테이너 내부에서 실행할 명령어를 지정하는 옵션
이 옵션을 사용하면 컨테이너 내부에서 쉘을 실행하고, 해당 쉘에서 지정한 명령어를 실행한다.
이 옵션은 새로운 프로세스를 실행하므로, 컨테이너 내부에서 실행 중인 다른 프로세스와는 별개로 실행된다.

- `exec`

Docker 컨테이너 내부에서 실행 중인 프로세스에 명령어를 전달하는 옵션
이 옵션을 사용하면, 이미 실행 중인 프로세스에 명령어를 전달하여 추가적인 작업을 수행할 수 있다.
이 옵션은 이미 실행 중인 프로세스와 연결되므로, 해당 프로세스가 종료되면 명령어도 함께 동료된다.

### CMD

``` bash
CMD /usr/sbin/httpd -DFOREGROUND
```


``` bash
CMD ["/usr/sbin/httpd", "-DFOREGROUND"]
```

CMD 또는 ENTRYPOINT에서는 Shell form을 사용하면 안된다.
작동에는 문제가 없지만, stop 시에는 항상 비정상 종료가 된다.

CMD를 사용할 때는 종료 시그널을 shell이 대신받아 이미지에 전달하지 않기 때문에, Docker가 kill signal을 전송시켜 프로세스가 강제로 죽는 것이다.

### ENTRYPOINT

Docker 컨테이너가 시작될 때 실행할 기본 명령어를 지정하는 지시어이다.

## Docker Cache

이미 한번 빌드한 이미지를 다시 빌드하면 작업이 금방 끝난다. 그리고 작업 내용을 보면 `Using cache`를 확인할 수 있다. 이는 빌드 과정 자체가 로컬에 저장되어 있기 때문에 따로 실행하지 않는다는 것이다.
`index.html`의 파일을 수정하고 빌드 시 cache를 사용하여 빌드가 되지 않는 것이 아닌, 파일의 hash값을 확인하여 기존의 hash값과 다를 때 빌드를 다시 진행한다.
또한 ubuntu는 `apt update`를 할 때만 최신 패키지 목록을 가져온다.
Docker image를 사용할 때 latest 태그를 사용하지 않는 것이 좋다. 이는 Dockerfile에서 패키치 설치 명령을 작성할 때도 마찬가지이다. 따라서 하기의 방법을 고안해보자.

1. ONBUILD 옵션

2. `--no-cache` 옵션 

## Multistage Build

기본 node 이미지를 사용하여 build (1.14GB)
```
FROM node:14

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "start"]
```

node 이미지 중 alpine 이미지를 사용하여 build (343MB)
```
FROM node:14-alpine

WORKDIR /app
COPY package.json .

RUN npm install --only=production

COPY /bin ./bin
COPY /public ./public
COPY /routes ./routes
COPY /views ./views
COPY /app.js ./

EXPOSE 3000
CMD ["npm", "start"]
```

Multi-stage Build를 이용한 build (283MB)
```
FROM node:14 as builder

WORKDIR /app

COPY package.json .
RUN npm install --no-cache && \
    rm -rf /app/node_modules && \
    npm install --only=production --no-cache --prefix /app

COPY . .


FROM node:14-alpine

WORKDIR /app
COPY package.json .
COPY . .
RUN npm install --only=production


EXPOSE 3000
CMD ["npm", "start"]
```

alpine 이미지는 기존 node 이미지보다 최소한의 런타임 라이브러리만 포함하고 있어, 적은 용량으로 이미지를 빌드하고 실행할 수 있다.


Multi-stage Build에서 `FROM node:14-alpine`는 동일한 base image이며, `npm install --only=production` 명령어도 동일하게 실행된다.

동일한 `npm install --only-production`을 수행하지만, 빌드 과정에서 처리되는 파일들이 다르기 때문에 이미지 크기 차이가 발생한다.
두 번째 Dockerfile에서는 `COPY . .` 명령어로 현재 디렉토리의 모든 파일을 복사하는데, 이는 불필요한 파일까지 모두 복사되어 이미지 크기가 커질 가능성이 있다.
세 번째 Dockerfile에서는 builder 이미지에서 필요한 파일들만 복사하고, 그 후에 최종 이미지에서 필요한 파일들만 복사하고 있다.


정리하자면, 첫 번째 `FROM` 명령어에서는 모든 의존성이 설치된 Node.js 이미지를 기반으로 빌드를 진행한다. 그리고 두 번째 `FROM` 명령어에서는 `node:14-alpine` 이미지를 기반으로 빌드하며, `--only=production` 옵션을 통해 개발 의존성을 설치하지 않고 프로독션 의존성만 설치한다. 따라서 최종 이미지의 용량 차이가 발생한다.

> `builder` 이미지를 이용하여 `npm install`을 실행하고 빌드된 파일들만(필요한 파일들만) 복사하여 이미지를 더 가볍게 만든다.