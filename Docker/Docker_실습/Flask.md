# Flask

- python3
- python3-pip
- python3-venv

``` bash
sudo apt install python3-pip python3-venv
```

``` bash
mkdir ~/python/hello-flask
cd ~/python/hello-flask
```

가상환경/프로젝트 생성
``` bash
python3 -m venv venv
```

가상환경 활성화
``` bash
. venv/bin/activate
```
> 가상환경 비활성화 deactivate

``` bash
pip3 install Flask
```

`hello.py`
``` py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

``` bash
export FLASK_APP=hello
flask run --host='0.0.0.0'
```

``` bash
pip3 freeze > requirements.txt
```

``` bash
pip3 install -r requirements.txt
```

Dockerfile 및 Image Build의 경우 Django.md와 같다.
[Django](https://github.com/ddung1203/TIL/blob/main/Docker/Docker_%EC%8B%A4%EC%8A%B5/Django.md)