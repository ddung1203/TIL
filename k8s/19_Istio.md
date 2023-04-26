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

## Visualizing Metrics with Grafana

서비스 mesh traffic을 확인하기 위해 Istio Dashboard를 활용한다. Grafana, Prometheus의 Addon을 설치하고, Bookinfo의 예제를 통해 확인해보겠다.

### 샘플 Prometheus 설치
``` bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.17/samples/addons/prometheus.yaml

kubectl patch svc prometheus -n istio-system -p '{"spec": {"type": "NodePort"}}'
```

상기 설정 및 기존 Grafana 대시보드 내 Data Source 추가

하기와 같이 성공적으로 배포 확인 가능

![Istio](./img/19_1.png)

> 일반적으로 하나의 Kubernetes 클러스터 내에서 여러 개의 Prometheus를 사용하는 것은 좋지 않다. 클러스터 리소스를 낭비하고 복잡성을 증가시킬 수 있다.

### Bookinfo

Bookinfo Application은 4개의 Micro Service로 나뉜다.

- productpage: Micro Service를 호출
- details: book info
- reviews: book reviews
- ratings: book ranking

아키텍처는 하기와 같다.

![Istio](./img/19_4.svg)

### Deploy Bookinfo

기본 Istio 설치는 automatic sidecar injection을 사용한다. label은 하기와 같이 `istio-injection=enabled`로 설정한다.

``` bash
kubectl label namespace default istio-injection=enabled
```

``` bash
kubectl apply -f ./istio-1.17.2/samples/bookinfo/platform/kube/bookinfo.yaml
```

``` bash
kubectl patch svc productpage -p '{"spec": {"type": "NodePort"}}'
```

### Traffic 전송

Bookinfo에 요청을 보내 트래픽을 확인한다.


``` bash
while true;do curl http://192.168.100.100:30241/productpage; done
```

![Istio](./img/19_2.png)

상기와 같이 Service Mesh를 확인할 수 있다. 