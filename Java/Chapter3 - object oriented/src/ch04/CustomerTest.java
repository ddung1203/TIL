package ch04;

public class CustomerTest {
  public static void main(String[] args) {
    Customer customerLee = new Customer(1001, "전중석");
    customerLee.bonusPoint = 1000;
    int price = customerLee.calcPrice(1000);
    System.out.println(customerLee.showCustomerInfo() + price);

    VIPCustomer customerKim = new VIPCustomer(1002, "김혜수");
    customerKim.bonusPoint = 10000;
    price = customerKim.calcPrice(1000);
    System.out.println(customerKim.showCustomerInfo() + price);

    Customer vc = new VIPCustomer(1234, "noname");


  }
}
