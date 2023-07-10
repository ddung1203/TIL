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
