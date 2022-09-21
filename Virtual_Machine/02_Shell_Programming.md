# Shell Programming 기초

## 변수

쉘에서는 변수를 선언할 때 그냥 변수명을 적어준다. 변수를 선언할 때 변수의 타입이나 형을 명시하지 않는다.
이렇게 선언된 변수는 문자열을 입력하여 문자열 변수로 활용해도되고 정수형 데이터를 입력하여 계산 및 연산을 위한 변수로 활용해도 된다.

``` bash
name=Joongseok
full_name="Joongseok Jeon"
```

``` bash
echo $name
echo $full_name
```

`name.sh`
``` bash
#!/bin/sh

name="Joongseok Jeon"
echo $name

echo First: $1, Second: $2
```

스크립트를 보면 1번째 라인에서 어떤 쉘을 이용하여 이 프로그램을 실행시킬 것인지를 지정하고 있는데 이는 스크립트가 실행되면 /bin/sh 프로그램 하에서 실행됨을 의미한다.
또한 /bin/sh 프로그램이 종료됨과 동시에 쉘스크립트의 실행도 끝나며 이 속에서 사용된 변수들도 모두 해제된다.

``` bash
vagrant@jeonj:~$ sh ./name.sh Joongseok Jeon
Joongseok Jeon
First: Joongseok, Second: Jeon
```

변수를 이용하여 스트링의 일부를 변경할 수도 있다.
예를 들어 option이라는 변수에 '1'을 입력한 후 ls -"$option"을 사용하면 ls -l과 동일한 문장이 된다.
이 기능을 이용하면 명령어로 사용할 문장을 완성한 후 이를 실행하는 프로그램을 작성할 수 있다.

`option.sh`
``` bash
#!/bin/sh

option=
First=$1
option=$First
ls -"$option"
```

``` bash
vagrant@jeonj:~$ sh option.sh l
total 16
-rw-rw-r-- 1 vagrant vagrant  462 Sep 20 05:33 connections_port.sh
-rw-rw-r-- 1 vagrant vagrant   72 Sep 21 07:58 name.sh
-rw-rw-r-- 1 vagrant vagrant 1773 Sep 20 05:26 netmon.sh
-rw-rw-r-- 1 vagrant vagrant   56 Sep 21 08:01 option.sh

vagrant@jeonj:~$ sh option.sh al
total 60
drwxr-xr-x 5 vagrant vagrant 4096 Sep 21 08:01 .
drwxr-xr-x 4 root    root    4096 Sep  4 07:12 ..
-rw------- 1 vagrant vagrant 1981 Sep 21 03:31 .bash_history
-rw-r--r-- 1 vagrant vagrant  220 Sep  2 21:54 .bash_logout
-rw-r--r-- 1 vagrant vagrant 3771 Sep  2 21:54 .bashrc
drwx------ 2 vagrant vagrant 4096 Sep  4 07:12 .cache
drwx------ 3 vagrant vagrant 4096 Sep 20 01:21 .config
-rw-r--r-- 1 vagrant vagrant  807 Sep  2 21:54 .profile
drwx------ 2 vagrant vagrant 4096 Sep  4 07:12 .ssh
-rw------- 1 vagrant vagrant 4821 Sep 21 08:01 .viminfo
-rw-rw-r-- 1 vagrant vagrant  462 Sep 20 05:33 connections_port.sh
-rw-rw-r-- 1 vagrant vagrant   72 Sep 21 07:58 name.sh
-rw-rw-r-- 1 vagrant vagrant 1773 Sep 20 05:26 netmon.sh
-rw-rw-r-- 1 vagrant vagrant   56 Sep 21 08:01 option.sh
```

쉘에서도 상수를 만들 수 있다. 즉, 값을 임의로 바꿀 수 있는 변수와는 달리 한번 값을 할당한 후 변경없이 사용하는 상수를 선언할 수 있다는 것이다. 이때 사용되는 키워드는 'readonly'인데 readonly로 선언된 변수는 이후로는 값을 변경할 수 없는 상수가 된다.


``` bash
name="Joongseok Jeon"
readonly name
```

``` bash
vagrant@jeonj:~$ echo $name
Joongseok Jeon

vagrant@jeonj:~$ name='foo'
-bash: name: readonly variable
```

## 제어문

### 조건문


명령어의 실행이 실패했을 때 이 내용을 로그로 남기는 작업

``` bash
Run Command1 || echo 첫번째 명령 실행 실패 >> log.txt
Run Command2 || echo 두번째 명령 실행 실패 >> log.txt
```

실패가 예상되는 명령에 대한 보완 명령 실행
ShellTest5.sh을 실행하면서 명령이 실패했을 경우 이를 해결하는 문장이다. 실패가 예상되는 경우 중 하나인 실행 권한을 부여하지 않은 문제를 해결하기 위한 명령이 `||` 연산자 뒤에 위치한다.

``` bash
ShellTest5.sh || chmod 755 ShellTest5.sh && ShellTest5.sh
```

`if_0.sh`
``` bash
#!/bin/sh

if [ $# -eq 2 ]
then
    echo "인수는 두개이며 내용은 <$1>, <$2> 입니다."
elif [ $# -eq 1 ]
then
    echo "인수는 한개이며 내용은 <$1>입니다."
else
    echo "인수는 하나도 없거나 너무 많습니다."
fi
```
`-eq` 는 `==` 와 동일한 의미를 가진다.
조건문에서 사용되는 연산들은 다음과 같다.

- 문자열 체크
  - [ stringName ] - 문자열이 널(Null) 인지 체크, Null이 아니면 참
  - [ -n stringName ] - 문자열의 사이즈가 0 이상인지 체크, 0 이상이면 참
  - [ -z stringName ] - 문자열의 사이즈가 0인지 체크, 0이면 참
  - [ stringNameA = stringNameB ] - A 문자열과 B 문자열이 같은지 체크, 같으면 참
  - [ stringNameA != stringNameB ] - A 문자열과 B 문자열이 다른지 체크, 다르면 참
- 숫자 대소 관계 체크
  - [ intA -ge 100 ] - 숫자 A가 100보다 크거나 같은지 체크, 100 이상이면 참
  - [ intA -gt 100 ] - 숫자 A가 100보다 큰지 체크, 100이 넘으면 참
  - [ intA -le 100 ] - 숫자 A가 100보다 작거나 같은지 체크, 100 이하이면 참
  - [ intA -lt 100 ] - 숫자 A가 100보다 작은지 체크, 100 미만이면 참
- 파일체크
  - [ -r filename ] - 해당 파일이 읽기 가능한지 체크
  - [ -w filename ] - 해당 파일이 쓰기 가능한지 체크
  - [ -x filename ] - 해당 파일이 실행 가능한지 체크
  - [ -s filename ] - 해당 파일의 사이즈가 제로 이상인지 체크
  - [ -d filename ] - 해당 파일이 디렉토리 파일인지 체크
  - [ -f filename ] - 해당 파일이 보통 파일인지 체크
  - [ -h filename ] - 해당 파일이 링크 파일인지 체크
- 조건문의 결합
  - [ 조건문A -a 조건문B ] - 조건문 A와 조건문 B가 모두 참인지 체크, -a는 AND와 동일
  - [ 조건문A -o 조건문B ] - 조건문 A와 B 중 참이 하나라도 있는지 체크, OR과 동일

``` bash

`if_1.sh`
#!/bin/sh
if [ $# -eq 1 ]
then
    if [ -r $1 ]
    then
        cat $1
    else
        echo "존재하지 않는 파일."
        echo "$1 파일 생성."
        echo "데이터를 입력한 후 Ctrl-C를 누르세요..."
        cat > $1
    fi
else
    echo "파일이름을 넣지 않았습니다. 다시 실행해 주세요."
fi
```
인수로 입력한 파일이 없을 때 파일을 직접 만드는 것을 볼 수 있다. 그리고 파일을 만들면서 사용자가 입력한 내용이 새로 생성된 파일 속에 입력되는 것을 확인할 수 있다.


`case.sh`
``` bash
#!/bin/sh

case $1 in
ls)
    ls ;;
ps)
    ps ;;
pwd)
    pwd ;;
*)
    echo "인수를 넣지 않았거나 존재하지 않는 명령어입니다.";
esac
```
case문을 끝내기 위해 사용한 `esac`은 case를 거꾸로 적은 글자이다.
인수로 ls를 입력하면 ls, ps를 입력하면 ps, pwd를 입력하면 pwd가 각각 실행된다.
만일 그 외의 인수를 넣거나 또는 인수를 넣지 않으면 echo에 입력한 문장이 화면에 나타나게 된다.


### 반복문

아래 예제는 쉘을 실행하면서 같이 입력한 인수들을 하나씩 실행하는 프로그램이다.

`loop_0.sh`
``` bash
#!/bin/sh
while [ $# -gt 0 ]
do
    echo "< $1 명령 실행 >"
    $1
    shift
done
```

``` bash
vagrant@jeonj:~$ vi loop_0.sh

vagrant@jeonj:~$ sh loop_0.sh ls pwd ps
< ls 명령 실행 >
case.sh  connections_port.sh  if_0.sh  if_1.sh  loop_0.sh  name.sh  netmon.sh  option.sh  qwe

< pwd 명령 실행 >
/home/vagrant

< ps 명령 실행 >
    PID TTY          TIME CMD
   1661 pts/0    00:00:00 bash
   3956 pts/0    00:00:00 sh
   3958 pts/0    00:00:00 ps
```

`shift` 명령어는 인수로 들어온 내용을 하나씩 옮겨가는 기능을 한다. `shift`가 실행되면 `$1`은 `$0`이 되고, `$2`는 `$1`이 된다.
따라서 인수만큼 `shift`가 실행된 후에는 `while` 속의 조건문의 거짓이 되고 `do~done` 사이의 구문은 반복실행을 멈추게 된다.

`loop_1.sh`
``` bash
#!/bin/sh

for variable in $*
do
    if [ $variable = java ]
    then
        echo "이번 에디션에서 자바 언어는 다루지 않습니다."
        continue
    elif [ $variable = quit ]
    then
        echo "Quit을 만나 for문을 종료합니다."
        break
    else
        echo "$variable 언어는 이번 에디션에서 다루는 언어입니다."
    fi
    echo "다음 언어를 체크합니다..."
done
```

``` bash
vagrant@jeonj:~$ sh loop_1.sh c python bash java quit foo
c 언어는 이번 에디션에서 다루는 언어입니다.
다음 언어를 체크합니다...
python 언어는 이번 에디션에서 다루는 언어입니다.
다음 언어를 체크합니다...
bash 언어는 이번 에디션에서 다루는 언어입니다.
다음 언어를 체크합니다...
이번 에디션에서 자바 언어는 다루지 않습니다.
Quit을 만나 for문을 종료합니다.
```

각각의 인수에 대해 `java`와 `quit` 이라는 단어가 있는지 체크를 하고 만일 `java`와 `quit` 이 아니면 `else` 문으로 분기하여 출력하게 된다.
만일 `java` 로 분기하면 `continue` 가 되어 바로 다음 반복문이 실행된다.

## 함수 작성


`func.sh`
``` bash
#!/bin/sh
withoutArg()
{
    echo "Run withoutArg() Function"
}
withArg()
{
    echo "Run withArg() Function"
    while [ $# -gt 0 ]
    do
        echo "Func with $1"
        shift
    done
}

withoutArg
withArg Joongseok Jeon
```

## AWK

`awk.sh`
``` bash
#!/bin/sh

usage=`df -k $1 | /bin/awk '{ rem = 0 } { n += 1 } { a = $3 } { b = $4 } \
n == 2 { rem = int(a/(a+b) * 100); print rem} \
END { }'`

if [ $usage -ge 90 ]
then
    echo "DISK($usage) - 심각한 상태"
elif [ $usage -ge 70 ]
then
    echo "DISK($usage) - 주의요망 상태"
else
    echo "DISK($usage) - 양호한 상태"
fi
```

WIP..