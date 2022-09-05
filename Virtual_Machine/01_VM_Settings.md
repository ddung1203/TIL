# 터미널 환경 구성
### ZSH이란?
많은 새로운 기능과 플러그인 및 테마를 지원한다. BSH과 동일한 Shell을 기반으로하기 때문에 ZSH은 동일한 기능을 많이 가지고 있으며 전환이 쉽다.

``` bash
sudo apt update
```

``` bash
sudo apt install zsh
```

``` bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

`~/.zshrc`
```
...
ZSH_THEME="agnoster"
...

plugins=(
	git
	zsh-autosuggestions
	zsh-completions
	zsh-syntax-highlighting
)
```

``` bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

``` bash
git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions
```

``` bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-syntax-highlighting
```


```
source ~/.zshrc
```

### VIM이란?
Linux의 대표적인 텍스트 편집기 vi와 호환되는 텍스트 편집기

`.vimrc`
```
if has("syntax")
	syntax on
endif

set hlsearch
set nu
set autoindent
set ts=2
set sts=2
set cindent
set laststatus=2
set shiftwidth=2
set showmatch
set smartcase
set smarttab
set smartindent
set ruler
set fileencodings=utf8,euc-kr
```