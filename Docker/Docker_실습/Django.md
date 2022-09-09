# Django
> https://docs.djangoproject.com/en/4.0/intro/tutorial01/

``` bash
mkdir ~/python/hello-django
cd ~/python/hello-django
```

``` bash
sudo apt install python3.8-venv
```

``` bash
python3 -m venv venv
```

``` bash
. venv/bin/activate
```

``` bash
pip3 install Django
```

``` bash
django-admin startproject mysite
```

``` bash
cd mysite
```

`mysite/settings.py`
```
...
ALLOWED_HOSTS = ['*']
...
```

``` bash
python3 manage.py runserver 0.0.0.0:8000
```

``` bash
python3 manage.py startapp polls
```

`polls/views.py`

``` py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

`polls/urls.py`
``` py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

`mysite/urls.py`
``` py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

``` bash
python3 manage.py runserver 0.0.0.0:8000
```

``` bash
curl 192.168.100.100:8080/polls
```

``` bash
pip3 freeze > requirments.txt
```

`.dockerignore`
```
venv/
Dockerfile
.dockerignore
```

`Dockerfile`
```
# For Normal Buster
FROM python:3.9-buster

# For Slim Buster
#FROM python:3.9-slim-buster
#RUN apt update && apt install -y gcc libc6-dev

# For Alpine Linux
#FROM python:3.9-alpine
#RUN apk add gcc musl-dev

COPY . /app


WORKDIR /app/mysite
RUN pip3 install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
```

생성한 Dockerfile을 Image로 빌드
``` bash
docker build -t ddung1203:1 .
```

Image Run
``` bash
docker run -p 8000:8000 -d ddung1203:1
```