package factory;

public abstract class CostEstimator 
{
    /**
     * Returns the tax estimator.
     */
    public abstract TaxEstimator getTaxEstimator();

    /**
     * 
     * @param quanity The quantity of the item.
     * @param price The price of the item.
     * @return The total value.
     */
    public double estimateSupplyCost(int quanity, double price) {
        return (quanity * price) * (1 + getTaxEstimator().getSalesTax());
    }
}
