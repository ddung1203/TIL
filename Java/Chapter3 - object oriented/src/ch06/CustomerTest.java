package ch06;

import java.util.ArrayList;

public class CustomerTest {
  public static void main(String[] args) {
    ArrayList<Customer> customerList = new ArrayList<>();

    Customer customerT = new Customer(10010, "Tomas");
    Customer customerJ = new Customer(10011, "John");
    Customer customerE = new GoldCustomer(10012, "Edward");
    Customer customerP = new GoldCustomer(10013, "Potter");
    Customer customerK = new VIPCustomer(10014, "Kim");

    customerList.add(customerT);
    customerList.add(customerJ);
    customerList.add(customerE);
    customerList.add(customerP);
    customerList.add(customerK);

    for (Customer customer : customerList) {
      System.out.println(customer.showCustomerInfo());
    }

    int price = 10000;

    for(Customer customer : customerList) {
      int cost = customer.calcPrice(price);
      System.out.println(cost);
      System.out.println(customer.bonusPoint);
    }


  }
}
