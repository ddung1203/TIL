# Monitoring & Logging

## Prometheus Monitoring

CPU, Memory, Network IO, Disk IO

- Heapster + InfluxDB : X
  - metrics-server : DB 없음, 실시간
    - CPU, Memory
  - Prometheus
![Prometheus](./img/17_1.png)

> https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

``` bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm update
```

`prom-value.yaml`
``` yaml
grafana:
  service:
    type: LoadBalancer
```

``` bash
kubectl create ns monirot
```

``` bash
helm install prom prometheus-community/kube-prometheus-stack -f prom-values.yaml -n monitor
```

웹브라우저 http://192.168.100.24X
ID: admin
PWD: prom-operator

## EFK Logging

ELK Stack: Elasticsearch + Logstash + Kibana
EFK Stack: Elasticsearch + Fluentd + Kibana 
(Elasticsearch + Fluent Bit + Kibana)
Elastic Stack: Elasticsearch + Beat + Kibana

### Elasticsearch

``` bash
helm repo add elastic https://helm.elastic.co
helm repo update
```

``` bash
helm show values elastic/elasticsearch > es-value.yaml
```

`es-value.yaml`
``` yaml
 18 replicas: 1
 19 minimumMasterNodes: 1
 
 80 resources:
 81   requests:
 82     cpu: "500m"
 83     memory: "1Gi"
 84   limits:
 85     cpu: "500m"
 86     memory: "1Gi"
```

``` bash
kubectl create ns logging
```

``` bash
helm install elastic elastic/elasticsearch -f es-value.yaml -n logging
```

### Fluent Bit

> https://github.com/fluent/fluent-bit-kubernetes-logging

``` bash
git clone https://github.com/fluent/fluent-bit-kubernetes-logging.git
```

``` bash
cd fluent-bit-kubernetes-logging
```

``` bash
kubectl create -f fluent-bit-service-account.yaml
kubectl create -f fluent-bit-role-1.22.yaml
kubectl create -f fluent-bit-role-binding-1.22.yaml
```

``` bash
kubectl create -f output/elasticsearch/fluent-bit-configmap.yaml
```

`output/elasticsearch/fluent-bit-ds.yaml`
``` yaml
 32         - name: FLUENT_ELASTICSEARCH_HOST
 33           value: "elasticsearch-master"
```

``` bash
kubectl create -f output/elasticsearch/fluent-bit-ds.yaml
```

### Kibana

``` bash
helm show values elastic/kibana > kibana-value.yaml
```

`kibana-value.yaml`
``` yaml
 49 resources:
 50   requests:
 51     cpu: "500m"
 52     memory: "1Gi"
 53   limits:
 54     cpu: "500m"
 55     memory: "1Gi"
 
 119 service:
 120   type: LoadBalancer
```

``` bash
helm install kibana elastic/kibana -f kibana-value.yaml -n logging
```

http://192.168.100.X:5601

- 햄버거 -> Management -> Stack Management
  - Kibana -> Index Pattern
    - Create Index Pattern 우상
        - Name: logstash-*
        - Timestamp: @timestamp
- 햄버거 -> Analystics -> Discover