"""Pure, illustrative long-only sizing and Rebalance Plan."""
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class PlannedOrder:
    symbol: str
    quantity: int

def risk_weights(volatility, gross_limit):
    if (not volatility or not math.isfinite(gross_limit)
            or not 0 <= gross_limit <= 1
            or any(not math.isfinite(v) or v <= 0 for v in volatility.values())):
        raise ValueError("Invalid volatility or gross limit")
    inverse = {s: 1/v for s, v in volatility.items()}
    total = sum(inverse.values())
    if not math.isfinite(total):
        raise ValueError("Volatility is too small")
    return {s: gross_limit * v/total for s, v in inverse.items()}

def plan(weights, prices, holdings, nav):
    if not math.isfinite(nav) or nav <= 0:
        raise ValueError("Invalid synthetic NAV")
    if any(not math.isfinite(w) or w < 0 for w in weights.values()) or sum(weights.values()) > 1 + 1e-12:
        raise ValueError("Invalid normalized target")
    if any(type(q) is not int or q < 0 for q in holdings.values()):
        raise ValueError("Only nonnegative integer holdings are supported")
    orders = []
    for symbol in sorted(weights.keys() | holdings.keys()):
        price = prices.get(symbol, 0)
        if not symbol or not math.isfinite(price) or price <= 0:
            raise ValueError("Missing or invalid price")
        quantity = math.floor(nav * weights.get(symbol, 0) / price) - holdings.get(symbol, 0)
        if quantity:
            orders.append(PlannedOrder(symbol, quantity))
    return tuple(orders)
