package ch02;

public class CustomerTest {
  public static void main(String[] args) {
    Customer customerLee = new Customer();
    customerLee.setCustomerName("전중석");
    customerLee.setCustomerID(1001);
    customerLee.bonusPoint = 100;
    System.out.println(customerLee.showCustomerInfo());

    VIPCustomer customerKim = new VIPCustomer();
    customerKim.setCustomerName("김혜수");
    customerKim.setCustomerID(1002);
    customerKim.bonusPoint = 1000;
    System.out.println(customerKim.showCustomerInfo());
  }
}
