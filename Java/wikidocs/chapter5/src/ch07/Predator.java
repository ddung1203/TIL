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
