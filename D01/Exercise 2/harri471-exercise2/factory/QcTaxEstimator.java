package factory;

public class QcTaxEstimator implements TaxEstimator {

  private final double gst = 0.05;
  private final double pst = 0.09975;

  @Override
  public double getSalesTax() {
    return gst + pst;
  }
}
