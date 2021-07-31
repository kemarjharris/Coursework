package factory;

public class OnTaxEstimator implements TaxEstimator {

  private final double hst = 0.14;

  @Override
  public double getSalesTax() {
    return hst;
  }

}
