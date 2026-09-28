"""The Strategy contract is independent of Account and execution."""
from typing import Protocol, Sequence
from dataclasses import dataclass

class Strategy(Protocol):
    def target(self, history: Sequence[float]) -> float: ...

@dataclass(frozen=True)
class ToyTrend:
    """Unrelated teaching rule; its window is not a production parameter."""
    window: int

    def __post_init__(self):
        if type(self.window) is not int or self.window < 2:
            raise ValueError("window must be an integer of at least two")

    def target(self, history):
        if len(history) < self.window:
            return 0.0
        recent = history[-self.window:]
        return float(recent[-1] > sum(recent) / self.window)
