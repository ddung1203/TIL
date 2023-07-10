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
