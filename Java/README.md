# Java

1. [객체지향](#객체지향)

2. [클래스](#클래스)

3. [Call by value](#call-by-value)

4. [상속](#상속)

5. [생성자](#생성자)

6. [인터페이스](#인터페이스)

7. [다형성](#다형성)

8. [추상클래스](#추상클래스)

## 객체지향

Sample 클래스에서 여러 대의 계산기가 필요한 상황이 발생하면, 각 계산기는 각각의 결괏값을 유지해야 하기 때문에 하기와 같이 객체를 사용하여 해결할 수 있다.

```java
package ch01;

public class Calculator {
  int result = 0;

  int add(int num) {
    result += num;
    return result;
  }

  int sub(int num) {
    result -= num;
    return result;
  }
}
```

```java
package ch01;

public class Sample {
  public static void main(String[] args) {
    Calculator cal1 = new Calculator();
    Calculator cal2 = new Calculator();

    System.out.println(cal1.add(3));
    System.out.println(cal1.sub(4));

    System.out.println(cal2.add(1));
    System.out.println(cal2.add(2));
  }
}
```

## 클래스

하기 Animal 클래스는 선언만 있고 내용은 없다. 하지만 `Sample.java`와 같이 객체를 만들 수 있다.

```java
package ch02;

public class Animal {
}
```

```java
package ch02;

public class Sample {
  public static void main(String[] args) {
    Animal cat = new Animal();
  }
}
```

### 객체 변수

Animal 클래스에 name이라는 String 변수를 추가했다. 이를 객체 변수라 한다.

객체 변수는 변수이므로 값을 대입할 수 있다. 객체 변수는 `.`을 이용하여 접근할 수 있다.

```java
cat.name
```

```java
package ch02;

public class Animal {
  String name;
}
```

### 메서드

객체 변수를 메서드를 이용하여 대입

메서드는 클래스 내에 구현된 함수를 의미하는데 보통 함수라고 말하지 않고 메서드라고 말한다.

```java
package ch02;

public class Animal {
  String name;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }
}
```

객체 변수에 접근하기 위해서 `객체.변수`와 같이 `.`로 접근할 수 있었던 것과 마찬가지로 객체가 메서드를 호출하기 위해서는 `객체.메소드`로 호출해야 한다.

```java
cat.setName("body");
```

main 메서드에서 `cat.setName("body")`와 같이 "body"라는 입력값으로 setName 메서드를 호출했기 때문에 setName함수의 입력 항목 name에는 "body"라는 문자열이 전달될 것이다.

따라서 setName의 메서드의 `this.name = name` 문장은 다음과 같이 해석되어 질 것이다.

```java
this.name = "body";
```

setName 메서드 내부에 사용된 `this`는 Animal 클래스에 의해서 생성된 객체를 지칭한다. 만약 `Animal cat = new Animal()`과 같이 cat이라는 객체를 만들고 `cat.setName("body")`와 같이 cat 객체에 의해 setName 메서드를 호출하면 setName 메서드 내부에 선언된 this는 cat 객체를 지칭한다.

## Call by value

메서드에 객체를 전달할 경우 메서드에서 객체의 객체변수 값을 변경할 수 있다.

```java
package ch04;

public class Updater {
  void update(Counter counter) {
    counter.count++;
  }
}
```

```java
package ch04;

public class Counter {
  int count = 0;
}
```

```java
package ch04;

public class Sample {
  public static void main(String[] args) {
    Counter myCounter = new Counter();
    System.out.println("before update: " + myCounter.count);

    Updater myUpdater = new Updater();
    myUpdater.update(myCounter);
    System.out.println("after update: " + myCounter.count);
  }
}
```

## 상속

```java
package ch05;

public class Animal {
  String name;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }
}
```

```java
package ch05;

public class Dog extends Animal {
  void sleep() {
    System.out.println(this.name + " zzz");
  }
}
```

```java
package ch05;

public class Sample {
  public static void main(String[] args) {
    Dog dog = new Dog();
    dog.setName("poppy");
    System.out.println(dog.getName());

    dog.sleep();
  }
}
```

Dog는 Animal을 상속했다. 즉, Dog는 Animal의 하위 개념이다.

자바는 이러한 관계를 `IS-A` 관계라고 표현한다. IS-A 관계에 있을 때 자식 클래스의 객체는 부모 클래스의 자료형인 것처럼 사용할 수 있다.

하지만 부모 클래스로 만들어진 객체를 자식 클래스의 자료형으로는 사용할 수 없다.

```java
Animal dog = new Dog();
```

> Dog 객체를 Animal 자료형으로 사용할 경우에는 Dog 클래스에만 존재하는 sleep 메서드를 사용할 수 없다. 이런 경우에는 Animal 클래스에 구현된 setName 메서드만 사용이 가능하다.

### 메서드 오버라이딩

부모클래스의 메서드를 자식클래스가 동일한 형태로 또다시 구현하는 행위를 메서드 오버라이딩이라 한다.

```java
package ch05;

public class HouseDog extends Dog {
  void sleep() {
    System.out.println(this.name + " zzz in house");
  }
}
```

### 메서드 오버로딩

이미 sleep이라는 메서드가 있지만 동일한 이름의 sleep 메서드를 또 생성할 수 있다. 단, 메서드의 입력항목이 다를 경우만 가능하다.

```java
package ch05;

public class HouseDog extends Dog {
  void sleep() {
    System.out.println(this.name + " zzz in house");
  }

  void sleep(int hour) {
    System.out.println(this.name + " zzz in house for " + hour + "hours");
  }
}
```

### 다중 상속

자바는 다중 상속을 지원하지 않는다. 다중 상속을 지원하게 되면 모호한 부분이 생기게 되며, 자바는 이러한 불명확한 부분을 없앤 언어이다.

## 생성자

dog 객체의 name 변수에 아무런 값도 성정하지 않았기 때문에 null이 출력될 것이다.

생성자를 이용하면, name이라는 객체변수에 값을 무조건 설정해야만 객체가 생성될 수 있도록 할 수 있다.

```java
package ch06;

public class Sample {
  public static void main(String[] args) {
    HouseDog dog = new HouseDog();
    System.out.println(dog.getName());
  }
}
```

```java
HouseDog dog = new HouseDog("puppy");
```

**생성자의 규칙**

1. 클래스명과 매서드명이 동일하다.
2. 리턴타입을 정의하지 않는다.

### Default 생성자

```java
package ch06;

public class Dog extends Animal {
  Dog() {

  }
  void sleep() {
    System.out.println(this.name + " zzz");
  }
}
```

생성자의 입력 항목이 없고 생성자 내부에 아무 내용이 없는 상기와 같은 생성자를 디폴트 생성자라고 부른다.

상기와 같이 디폴트 생성자를 구현하면 `new Dog()`로 Dog 클래스의 객체가 만들어질 때 위에 구현한 디폴트 생성자가 실행될 것이다. 만약 클래스에 생성자가 하나도 없다면 컴파일러는 자동으로 상기와 같은 디폴트 생성자를 추가한다. 하지만 사용자가 작성한 생성자가 하나라도 구현되어 있다면 컴파일러는 디폴트 새엇ㅇ자를 추가하지 않는다.

### 생성자 오버로딩

```java
package ch06;

public class HouseDog extends Dog {

  public HouseDog(String name) {
    this.setName(name);
  }

  public HouseDog(int type) {
    if (type == 1) {
      this.setName("yorkshire");
    } else if (type == 2) {
      this.setName("bulldog");
    }
  }

  void sleep() {
    System.out.println(this.name + " zzz in house");
  }

  void sleep(int hour) {
    System.out.println(this.name + " zzz in house for " + hour + " hours");
  }
}
```

```java
package ch06;

public class Sample {
  public static void main(String[] args) {
    HouseDog dog1 = new HouseDog("puppy");
    HouseDog dog2 = new HouseDog(1);

    System.out.println(dog1.getName());
    System.out.println(dog2.getName());
  }
}
```

상기의 HouseDog 클래스는 두 개의 생성자가 있다. 이렇게 입력 항목이 다른 생성자를 여러 개 만들 수 있는데 이런 것을 생성자 오버로딩이라 한다.

## 인터페이스

예제

```java
package ch07;

public class Animal {
  String name;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }
}
```

```java
package ch07;

public class Tiger extends Animal {
}
```

```java
package ch07;

public class Lion extends Animal {
}
```

```java
package ch07;

public class Zookeeper {
  void feed(Tiger tiger) {
    System.out.println("feed apple");
  }

  void feed(Lion lion) {
    System.out.println("feed banana");
  }
}
```

```java
package ch07;

public class Sample {
  public static void main(String[] args) {
    Zookeeper zooKeeper = new Zookeeper();
    Tiger tiger = new Tiger();
    Lion lion = new Lion();

    zooKeeper.feed(tiger);
    zooKeeper.feed(lion);
  }
}
```

여타 다른 동물들이 추가된다면 ZooKeeper는 육식동물이 추가될 때마다 하기와 같이 매번 feed 메서드를 추가해야 한다.

```java
public void feed(Crocodile crocodile) {
  System.out.println("feed strawberry");
}

public void feed(Leopard leopard) {
  System.out.println("feed orange");
}
```

```java
package ch07;

public class Tiger extends Animal implements Predator {
  @Override
  public String getFood() {
    return "apple";
  }
}
```

```java
package ch07;

public class Lion extends Animal implements Predator {
  @Override
  public String getFood() {
    return "banana";
  }
}
```

```java
package ch07;

public class Zookeeper {
  void feed(Predator predator) {
    System.out.println("feed " + predator.getFood());
  }

}
```

```java
package ch07;

public interface Predator {
  String getFood();
}
```

```java
package ch07;

public class Sample {
  public static void main(String[] args) {
    Zookeeper zooKeeper = new Zookeeper();
    Tiger tiger = new Tiger();
    Lion lion = new Lion();

    zooKeeper.feed(tiger);
    zooKeeper.feed(lion);
  }
}
```

인터페이스 구현은 `implements` 키워드를 사용한다.

또한 feed 메서드의 입력으로 Tiger, Lion을 각각 필요로 했지만 이제 Predator라는 인터페이스로 대체할 수 있다. **tiger, lion은 각각 Tiger, Lion의 객체이기도 하지만 Predator 인터페이스의 객체이기도 하기 때문에 상기와 같이 Predator를 자료형의 타입으로 사용할 수 있다.**

인터페이스의 메서드는 메서드의 이름과 입출력에 대한 정의만 있고 내용을 없다. 위에서 설정한 getFood라는 메서드는 인터페이스를 implements한 클래스들이 구현해야만 하는 것이다.

육식 동물들의 종류만큼의 feed 메서드가 필요했던 Zookeeper 클래스를 Predator 인터페이스를 이용하여 구현했더니 단 한개의 feed 메서드로 구현이 가능해졌다. 여기서, 메서드의 갯수가 줄어들었다는 점이 아니라 ZooKeeper 클래스가 동물들의 종류에 의존적인 클래스에서 동물들의 종류와 상관없는 독립적인 클래스가 되었다는 점이다.

```java
package ch07;

public interface Predator {
  String getFood();

  default void printFood() {
    System.out.printf("my food is %s\n", getFood());
  }

  int LEG_COUNT = 4;

  static int speed() {
    return LEG_COUNT * 30;
  }
}
```

### 디폴트 메서드

디폴드 메서드는 메서드명 가장 앞에 `default`라고 표기해야 한다. 이렇게 Predator 인터페이스에 printFood 디폴트 메서드를 구현하면 Predator 인터페이스를 구현한 Tiger, Lion 등의 실제 클래스는 printFood 메서드를 구현하지 않아도 사용할 수 있다. 그리고 디폴트 메서드는 오버라이딩이 가능하다. 즉, printFood 메서드를 실제 클래스에서 다르게 구현하여 사용할 수 있다.

### 스태틱 메서드

인터페이스에 스태틱 메서드를 구현하면 `인터페이스명.스태틱메서드명`과 같이 사용하여 일반 클래스의 스태틱 메서드를 사용하는 것과 동일하게 사용할 수 있다.

## 다형성

```java
package ch07;

public class Bouncer {
  void barkAnimal(Animal animal) {
    if (animal instanceof Tiger) {
      System.out.println("어흥");
    } else if (animal instanceof Lion) {
      System.out.println("으르렁");
    }
  }
}
```

```java
package ch07;

public class Sample {
  public static void main(String[] args) {
    Tiger tiger = new Tiger();
    Lion lion = new Lion();

    Bouncer bouncer = new Bouncer();
    bouncer.barkAnimal(tiger);
    bouncer.barkAnimal(lion);
  }
}
```

barkAnimal 메서드는 입력으로 받은 animal 객체가 Tiger의 객체인 경우 각각을 출력한다. 하지만, 이 경우 다른 클래스가 추가되면 `else if`로 분기문이 추가되어야 한다. 따라서 하기와 같이 변경하도록 한다.

```java
package ch07;

public interface Barkable {
  void bark();
}
```

barkAnimal 메서드의 입력 자료형이 Animal에서 Barkbale로 변경하였다. 그리고 animal의 객체 타입을 체크하여 bark 메서드를 호출하도록 변경하였다.

```java
package ch07;

public class Bouncer {
  void barkAnimal(Barkable animal) {
    animal.bark();
  }
}
```

Tiger, Lion 클래스는 Predator 인터페이스와 Barkable 인터페이스를 implements하였다.

```java
package ch07;

public class Lion extends Animal implements Predator,Barkable {
  @Override
  public String getFood() {
    return "banana";
  }

  @Override
  public void bark() {
    System.out.println("으르렁");
  }
}
```

상기 예제에서 사용한 tiger, lion 객체는 각각 Tiger, Lion 클래스의 객체이면서 Animal 클래스의 객체이기도 하고 Barkable, Predator 인터페이스의 객체이기도 하다. 이러한 이유로 barkAnimal 메서드의 입력 자료형을 Animal에서 Barkable로 바꾸어 사용할 수 있는 것이다.

이렇게 하나의 객체가 여러개의 자료형 타입을 가질 수 있는 것을 다형성이라 한다.

## 추상클래스

추상클래스는 인터페이스의 역할도 하면서 클래스의 기능도 가지고 있는 클래스이다.

```java
package ch08;

public abstract class Predator extends Animal {
  abstract String getFood();

  void printFood() {
    System.out.printf("my food is %s\n", getFood());
  }

  static int LEG_COUNT = 4;

  static int speed() {
    return LEG_COUNT * 30;
  }
}
```

class 앞에 abstract를 표기해야 한다. 또한 인터페이스의 메서드와 같은 역할을 하는 메서드에도 abstract를 붙여야 한다. 인터페이스의 메서드와 마찬가지로 몸통이 없이, abstract 클래스를 상속하는 클래스에서 해당 abstract 메서드를 구현해야만 한다.

> 인터페이스와 추상 클래스의 차이
>
> 추상 클래스는 인터페이스와 달리 일반 클래스터럼 객체변수, 생성자, private 메서드 등을 가질 수 있다.
