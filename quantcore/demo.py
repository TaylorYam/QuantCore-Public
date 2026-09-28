"""Run with python -m quantcore.demo; all output is synthetic."""
import json
from .data import synthetic_prices
from .strategy import ToyTrend
from .backtest import run
from .robustness import walk_forward, bootstrap, plateau
from .portfolio import risk_weights, plan
from .execution import MockBroker

def main():
    prices = synthetic_prices()
    result = run(prices, ToyTrend(7), cost_bps=2)
    folds = walk_forward(prices, (3, 7, 11), 32, 16, cost_bps=2)
    samples = bootstrap(result.returns)
    _, regions = plateau(prices, (3, 7, 11), .03, cost_bps=2)
    weights = risk_weights({"SYNTH": .23}, .61)
    orders = plan(weights, {"SYNTH": prices[-1]}, {}, 10000)
    broker = MockBroker()
    previews = [broker.preview(str(i), o, prices[-1]) for i, o in enumerate(orders)]
    print(json.dumps({"data": "ARTIFICIAL; not investment performance",
                      "observations": len(prices), "walk_forward_folds": len(folds),
                      "bootstrap_paths": len(samples), "plateau_regions": regions,
                      "previews": previews, "monitoring": broker.events}, indent=2))

if __name__ == "__main__":
    main()
