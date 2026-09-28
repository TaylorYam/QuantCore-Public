# Domain vocabulary

- **Strategy**: a producer of normalized target exposure, independent of Account and execution. Cash is a valid output.
- **Account**: a broker portfolio context; no concrete Account is modeled in this demonstration.
- **Allocation**: an Account-level multiplier assigned to a Strategy; deployed values and composition are excluded.
- **Constituents**: instruments eligible at a particular observation date.
- **Universe**: the historical union of Constituents. The sample has only one fictional instrument.
- **Rebalance Plan**: plain-data orders derived from targets, prices, holdings and synthetic NAV.
- **Reference Close**: an already observed close, available before the next simulated return.

The public demonstration deliberately implements only a small subset of these concepts.
