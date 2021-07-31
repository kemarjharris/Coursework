package factory;

public class Client {

  /**
   * Demo the use of the pattern.
   * @param args the usual
   */
  public static void main(String[] args) {
    CostEstimator once = new OnCostEstimator();
    CostEstimator qcce = new QcCostEstimator();
    System.out.println(String.format("$%.2f", once.estimateSupplyCost(42, 50.67)));
    System.out.println(String.format("$%.2f", qcce.estimateSupplyCost(42, 50.67)));

    // Expected output:
    // $2426.08
    // $2446.83
  }
}
