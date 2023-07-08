package ch03;

public class CustomerTest {
  public static void main(String[] args) {
    Customer customerLee = new Customer(1001, "전중석");
    customerLee.bonusPoint = 100;
    System.out.println(customerLee.showCustomerInfo());

    VIPCustomer customerKim = new VIPCustomer(1002, "김혜수");
    customerKim.bonusPoint = 1000;
    System.out.println(customerKim.showCustomerInfo());

    Customer vc = new VIPCustomer(1234, "noname");


  }
}
