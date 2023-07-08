package ch10;

public class CarTest {
  public static void main(String[] args) {
    Car AICar = new AICar();
    AICar.run();

    Car ManualCar = new ManualCar();
    ManualCar.run();
  }
}
