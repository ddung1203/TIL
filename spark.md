# 전중석

### 스칼라 설치

```java
sudo apt install scala
```

환경변수 설정

```bash
export SCALA_HOME=/usr/bin
```

Apache Spark 설치 & 세팅

```bash
wget https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3-scala2.13.tgz
tar xvfz spark-3.3.0-bin-hadoop3-scala2.13.tgz
mv spark-3.3.0-bin-hadoop3-scala2.13 spark
```

.zshrc(slave1, slave2에 동일하게 설정)

```bash
export SPARK_HOME=$HOME/spark
export PYSPARK_PYTHON=python3
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```

spark/conf/workers

```bash
slave1
slave2
```

spark/conf/spark-env.sh

```bash
export SCALA_HOME=/usr/bin
export SPARK_HOME=$HOME/spark

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

slave1, slave2 복사

```bash
scp -r /home/vagrant/spark slave1:/home/vagrant/
scp -r /home/vagrant/spark slave2:/home/vagrant/
```

HDFS 실행

```bash
start-dfs.sh
```

스파크 서버 실행

```bash
start-master.sh
start-slaves.sh 
```

---

hdfs 파일복사

```bash
hdfs dfs -mkdir -p /user/ubuntu
hdfs dfs -put $SPARK_HOME/README.md /user/ubuntu/
hdfs dfs -ls /user/ubuntu
```

Wordcount(scala)

```bash
val textFile = sc.textFile("hdfs://master:9000/user/ubuntu/README.md")
val counts = textFile.flatMap(line => line.split(" ")).map(word => (word,1)).reduceByKey(_ + _)
counts.saveAsTextFile("hdfs://master:9000/user/ubuntu/mapreduce_result")
```

결과 확인

```bash
hdfs dfs -cat /user/ubuntu/mapreduce_result/part-00000
hdfs dfs -cat /user/ubuntu/mapreduce_result/part-00001
```

- Worker 노드의 개수 ⇒ 입력 파일의 크기를 128MB로 나눈 값

→ 하둡의 MapReduce와 달리 정렬이 안됨. 원할 경우 정렬이 가능하다.

READMD.txt에서 rdd.split()함수에서 제거할 글자를 구분자를 포함해 결과 정제

```bash
val counts = textFile.flatMap(line => line.split(" ")).flatMap(line => line.split("~")).flatMap(line => line.split("!")).flatMap(line => line.split("@")).flatMap(line => line.split("#")).flatMap(line => line.split("$")).flatMap(line => line.split("%")).flatMap(line => line.split("\\^")).flatMap(line => line.split("&")).flatMap(line => line.split("\\*")).flatMap(line => line.split("\\(")).flatMap(line => line.split("\\)")).flatMap(line => line.split("=")).flatMap(line => line.split("\\+")).flatMap(line => line.split("\\[")).flatMap(line => line.split("]")).flatMap(line => line.split("\\{")).flatMap(line => line.split("}")).flatMap(line => line.split("\"")).flatMap(line => line.split("\\|")).flatMap(line => line.split(";")).flatMap(line => line.split(":")).flatMap(line => line.split("\\.")).flatMap(line => line.split("\\,")).flatMap(line => line.split("<")).flatMap(line => line.split(">")).flatMap(line => line.split("\\?")).flatMap(line => line.split("/")).flatMap(line => line.split("\"")).flatMap(line => line.split("‘")).flatMap(line => line.split("'")).flatMap(line => line.split("`")).flatMap(line => line.split("_")).flatMap(line => line.split("-")).flatMap(line => line.split("\\\\")).flatMap(line => line.split("”")).flatMap(line => line.split("–")).map(_.toLowerCase).map(word => (word, 1)).reduceByKey(_ + _)
```