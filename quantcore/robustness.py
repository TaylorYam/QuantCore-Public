"""Small reproducible research tools, without production baselines."""
import math
import random
from dataclasses import dataclass
from .backtest import run, metrics
from .data import validate
from .strategy import ToyTrend

@dataclass(frozen=True)
class Fold:
    train_end: int
    test_end: int
    selected_window: int
    returns: tuple[float, ...]

def walk_forward(prices, windows, train_size, test_size, cost_bps=0.0):
    prices = validate(prices)
    windows = tuple(sorted(set(windows)))
    if not windows:
        raise ValueError("Empty candidate grid")
    for w in windows:
        ToyTrend(w)
    if (type(train_size) is not int or type(test_size) is not int
            or train_size <= max(windows) or test_size < 1
            or train_size >= len(prices)):
        raise ValueError("Invalid fold sizes")
    folds = []
    for end in range(train_size, len(prices), test_size):
        selected = max(windows, key=lambda w: run(
            prices[:end], ToyTrend(w), cost_bps).equity[-1])
        stop = min(end + test_size, len(prices))
        # Each independent fold starts in cash and charges initial turnover.
        result = run(prices[:stop], ToyTrend(selected), cost_bps, start=end)
        folds.append(Fold(end, stop, selected, result.returns))
    return tuple(folds)

def bootstrap(returns, simulations=100, seed=17):
    values = tuple(returns)
    metrics(values)
    if not values or type(simulations) is not int or simulations < 1:
        raise ValueError("Need returns and a positive simulation count")
    rng = random.Random(seed)
    return tuple(metrics(rng.choices(values, k=len(values))) for _ in range(simulations))

def plateau(prices, windows, tolerance, cost_bps=0.0):
    """Contiguous near-best runs on the supplied ordered candidate grid."""
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("Invalid absolute score tolerance")
    scores = {w: run(prices, ToyTrend(w), cost_bps).equity[-1] - 1
              for w in sorted(set(windows))}
    if not scores:
        raise ValueError("Empty grid")
    cutoff = max(scores.values()) - tolerance
    regions, current = [], []
    for window, score in scores.items():
        if score >= cutoff:
            current.append(window)
        elif current:
            regions.append(tuple(current)); current = []
    if current:
        regions.append(tuple(current))
    return scores, tuple(regions)
