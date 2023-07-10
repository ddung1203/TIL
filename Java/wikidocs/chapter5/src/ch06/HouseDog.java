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
