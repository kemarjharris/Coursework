package factory;

public class OnCostEstimator extends CostEstimator 
{

    @Override
    public TaxEstimator getTaxEstimator() {
        return new OnTaxEstimator();
    }
    
}
