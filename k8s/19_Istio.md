# Istio

> https://www.istioworkshop.io/
> https://github.com/rafik8/istio-workshop-labs

Istio는 Kubernetes 환경에서 서비스 메시를 관리하기 위한 오프소스 플랫폼이다. Envoy를 기반으로 하며, 서비스 간 트래픽 관리, 인증 및 권한 부여, 서비스 모니터링, 로깅 등 다양한 기능을 제공한다.

1. 서비스 메시 구성

Istio는 Kubernetes 상에서 Envoy 프록시를 이용하여 서비스 간의 통신을 관리한다. 서비스 메시 구성은 Istio의 제어 평면에서 이루어지며, 다양한 라우팅 규칙, 트래픽 분산 방식, 롤릴 업데이트 등을 설정할 수 있다.

2. 인증 및 권한 부여

Istio는 서비스 간 통신에 대한 보안을 제공한다. mTLS 기반의 보안 통신을 지원하며, 인증 및 권한 부여를 위한 다양한 기능을 제공한다.

3. 서비스 모니터링

Istio는 서비스 메시에서 발생하는 트래픽을 모니터링하고, Prometheus와 Grafana를 이용하여 대시보드를 제공한다. 이를 통해 소비스 메시의 상태를 실시간으로 확인할 수 있다.

4. 로깅

Istio는 서비스 메시에서 발생하는 로그를 수집하고, Fluntd 또는 Fluent Bit와 같은 로그 수집 도구와 연동하여 로그 분석을 가능하게 한다.

5. 서비스 메시 확장

Istio는 Kubernetes 환경에서 서비스 메시를 확장하는 다양한 기능을 제공한다. 예를 들어, 서비스 메시 확장을 위한 Auto Scaling, Traffic Splitting 등을 지원한다.

## Install

``` bash
mkdir ~/istio && cd ~/istio
```

최신 버전 설정

> https://github.com/istio/istio

``` bash
export ISTIO_VERSION=1.17.2
```

``` bash
curl -L https://git.io/getLatestIstio | sh -
```

PATH에 istioctl 추가
``` bash
export PATH="$PATH:~/istio-$ISTIO_VERSION/bin"
```

``` bash
 vagrant@k8s-node1  ~/istio  istioctl version --remote=false
1.17.2
```


하기 설치의 경우 demo를 사용한다.
``` bash
 vagrant@k8s-node1  ~/istio  istioctl install --set profile=demo -y
✔ Istio core installed                                                        
✔ Istiod installed                                                            
✔ Egress gateways installed                                                   
✔ Ingress gateways installed                                                  
✔ Installation complete                                                       
```

namespace label을 추가하여 Istio에 Envoy를 자동으로 삽입
``` bash
kubectl label namespace default istio-injection=enabled
```

