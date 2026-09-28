"""Close-to-close toy evaluation with prior-close information only."""
import math
from dataclasses import dataclass
from .data import validate
from .strategy import Strategy

@dataclass(frozen=True)
class Result:
    returns: tuple[float, ...]
    equity: tuple[float, ...]
    max_drawdown: float

def metrics(returns):
    returns = tuple(returns)
    if any(not math.isfinite(r) or r <= -1 for r in returns):
        raise ValueError("Returns must be finite and greater than minus one")
    equity = [1.0]
    peak = 1.0
    drawdown = 0.0
    for r in returns:
        equity.append(equity[-1] * (1 + r))
        peak = max(peak, equity[-1])
        drawdown = min(drawdown, equity[-1] / peak - 1)
    return Result(returns, tuple(equity), drawdown)

def run(prices, strategy: Strategy, cost_bps=0.0, start=1):
    prices = validate(prices)
    if not math.isfinite(cost_bps) or not 0 <= cost_bps < 10000:
        raise ValueError("Invalid transaction cost")
    if type(start) is not int or not 1 <= start < len(prices):
        raise ValueError("Invalid evaluation start")
    previous = 0.0
    returns = []
    for t in range(start, len(prices)):
        weight = strategy.target(prices[:t])
        if not math.isfinite(weight) or not 0 <= weight <= 1:
            raise ValueError("Toy backtest requires a long-only normalized target")
        returns.append(weight * (prices[t] / prices[t-1] - 1)
                       - abs(weight - previous) * cost_bps / 10000)
        previous = weight
    return metrics(returns)
