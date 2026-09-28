"""Preview-only IB API boundary. No broker transport exists in this package."""
from copy import deepcopy
import math
from .portfolio import PlannedOrder

def ib_preview(order: PlannedOrder, limit_price):
    """Map plain data to common IB Contract/Order field names."""
    if (not order.symbol or type(order.quantity) is not int or not order.quantity
            or not math.isfinite(limit_price) or limit_price <= 0):
        raise ValueError("Invalid order preview")
    return {
        "contract": {"symbol": order.symbol, "secType": "STK", "exchange": "SMART", "currency": "USD"},
        "order": {"action": "BUY" if order.quantity > 0 else "SELL",
                  "totalQuantity": abs(order.quantity), "orderType": "LMT",
                  "lmtPrice": limit_price, "transmit": False},
    }

class MockBroker:
    def __init__(self):
        self.previews = {}
        self.events = []

    def preview(self, request_key, order, limit_price):
        if not request_key:
            raise ValueError("Request key is required")
        payload = ib_preview(order, limit_price)
        if request_key in self.previews and self.previews[request_key] != payload:
            raise ValueError("Request key reused for a different order")
        if request_key not in self.previews:
            self.previews[request_key] = deepcopy(payload)
            self.events.append({"event": "preview_created", "request_key": request_key})
        return payload

    def submit(self, *args, **kwargs):
        raise RuntimeError("Order submission is unavailable in this public demo")
