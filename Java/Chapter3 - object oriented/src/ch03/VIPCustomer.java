package ch03;

public class VIPCustomer extends Customer {
  private String agentID;
  double salesRatio;

//  public VIPCustomer() {
//    bonusRatio = 0.05;
//    salesRatio = 0.1;
//    customerGrade = "VIP";
//
//    System.out.println("VIPCustomer() 호출");
//  }

  public VIPCustomer(int customerID, String customerName) {
    super(customerID, customerName);

    customerGrade = "VIP";
    bonusRatio = 0.05;
    salesRatio = 0.1;

    System.out.println("VIPCustomer() 호출");
  }

  public String getAgentID() {
    return agentID;
  }

  public void setAgentID(String agentID) {
    this.agentID = agentID;
  }
}
