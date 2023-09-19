# Kubectl CLI

Kubectl CLI 꿀팁

### Kubectl 자동 완성

`/.zshrc`
```bash
# 추가
source <(kubectl completion zsh)
```

### Krew

krew는 kubectl 플러그인 매니저이다.

```bash
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)
```

`~/.zshrc`
```bash
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
```

krew를 사용하여 `kube-ctx`, `kube-ns` 등의 플러그인을 사용할 수 있다.

```bash
kubectl krew install ns
kubectl krew install ctx
```

### kube-ps1

kubernetes context(클러스터, 네임스페이스)를 zsh에 표시한다.

`~/.zshrc`
```
plugins=(
  kube-ps1
)

PROMPT='$(kube_ps1)'$PROMPT # or RPROMPT='$(kube_ps1)'
```

하기와 같다. 

![img](../img/03_kubectl_01.png)

> 혹은 zsh의 `powerlevel10k/powerlevel10k` 테마 사용

### kube-neat

`-o yaml`로 파일을 export 할 때, `krew`로 `neat` 플러그인을 사용하면 가독성이 향상된다.

```bash
kubectl krew install neat
kubectl get deployments.apps/youtube-deployment -o yaml | kubectl neat
```

