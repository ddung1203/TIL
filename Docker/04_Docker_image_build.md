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