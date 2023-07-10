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
