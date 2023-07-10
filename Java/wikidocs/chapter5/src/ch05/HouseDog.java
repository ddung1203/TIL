package ch05;

public class HouseDog extends Dog {
  void sleep() {
    System.out.println(this.name + " zzz in house");
  }

  void sleep(int hour) {
    System.out.println(this.name + " zzz in house for " + hour + " hours");
  }
}
