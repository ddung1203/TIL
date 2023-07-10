package ch06;

public class Sample {
  public static void main(String[] args) {
    HouseDog dog1 = new HouseDog("puppy");
    HouseDog dog2 = new HouseDog(1);

    System.out.println(dog1.getName());
    System.out.println(dog2.getName());
  }
}
