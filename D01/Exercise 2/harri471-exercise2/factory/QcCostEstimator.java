package factory;

public class QcCostEstimator  extends CostEstimator
{

    @Override
    public TaxEstimator getTaxEstimator() {
        return new QcTaxEstimator();
    }
    
}
