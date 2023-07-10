package ch08;

public class Tiger extends Predator implements Barkable {
  @Override
  public String getFood() {
    return "apple";
  }

  @Override
  public void bark() {
    System.out.println("어흥");
  }
}
