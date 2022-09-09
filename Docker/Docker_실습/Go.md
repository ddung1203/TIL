# Go

```
mkdir -p ~/golang/hello
cd ~/golang/hello
```

```
sudo apt install golang
```

```
go mod init hello
```

`hello.go`
``` go
package main

import "fmt"

func main() {
        fmt.Println("hello go world")
}
```

```
go run .
-OR-
go run hello.go
```

```
go build .
-OR-
go build -o hello hello.go
```

`Dockerfile`
```
FROM golang:1.18-buster AS gobuilder
COPY . /app
WORKDIR /app
RUN go build .

FROM scratch
COPY --from=gobuilder /app/hello /
CMD ["/hello"]
```

```
docker build -t gohello .
```

```
docker run gohello
```

## HTTP Web
```
mkdir ~/golang/goweb
cd ~/golang/goweb
```

```
go mod init goweb
```

`goweb.go`
``` go
package main

import (
        "fmt"
        "log"
        "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hi there, I love %s!", r.URL.Path[1:])
}

func main() {
        http.HandleFunc("/", handler)
        log.Fatal(http.ListenAndServe(":8080", nil))
}
```

```
go run .
```

```
go build .
```

`.dockerignore`
```
goweb
Dockerfile
.dockerignore
```

`Dockerfile`
```
FROM golang:1.18-buster AS gobuilder
ENV CGO_ENABLED 0
COPY . /app
WORKDIR /app
RUN go build -o goweb .

FROM scratch
COPY --from=gobuilder /app/goweb /
CMD ["/goweb"]
EXPOSE 8080
```

```
docker build -t goweb .
```

```
docker run -d -p 80:8080 goweb
```

## Gin
```
mkdir ~/golang/gogin
cd ~/golang/gogin
```

```
go mod init gogin
```

`gogin.go`
``` go
package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
```

```
go mod tidy
```

```
cat go.sum
```

`Dockerfile`
```
FROM golang:1.18-buster AS gobuilder
ENV CGO_ENABLED 0
COPY . /app
WORKDIR /app
RUN go build -o gogin .

FROM scratch
COPY --from=gobuilder /app/gogin /
CMD ["/gogin"]
EXPOSE 8080
```

```
docker build -t gogin .
```
```
docker run -d -p 80:8080 gogin
```

```
curl 192.168.100.100/ping
```