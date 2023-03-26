# Addons
## Metallb
`~/kubespray/inventory/mycluster/group_vars/k8s-cluster/addons.yml`
```
...
139 metallb_enabled: true
140 metallb_speaker_enabled: true
141 metallb_ip_range:
142   - "192.168.100.240-192.168.100.249"
...
168 metallb_protocol: "layer2"
...
```

`~/kubespray/inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml`
```
129 kube_proxy_strict_arp: true
```

## Niginx Ingress Controller
`~/kubespray/inventory/mycluster/group_vars/k8s-cluster/addons.yml`
```
 93 ingress_nginx_enabled: true
```

## metrics-server
`~/kubespray/inventory/mycluster/group_vars/k8s-cluster/addons.yml`
```
 16 metrics_server_enabled: true
```

적용
```
ansible-playbook -i inventory/mycluster/inventory.ini cluster.yml -b
```
