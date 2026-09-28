# Validation methods

The toy rule compares the most recently observed price with its short moving average. Its arbitrary example windows are chosen for a short artificial series; none are derived from deployed settings. It is a teaching mechanism, not an alpha claim.

## Backtest assumptions

At return index t, Strategy receives prices strictly before t. The chosen weight applies to the close-to-close return ending at t. This assumes execution at the prior close without information or execution delay; real fill timing needs a separate model. Turnover cost is proportional to absolute weight change. The initial position is cash. Terminal positions are marked, without a forced final liquidation. Drawdown includes initial capital as a peak.

## Walk-forward analysis

An expanding training prefix selects the highest terminal-equity candidate, with deterministic smallest-window tie-breaking. The next disjoint test block is evaluated using only already observed prices, with warm-up history available. Each fold starts in cash and charges initial turnover; fold returns should not be interpreted as one continuously held portfolio. The final partial test block is included. Tests mutate future prices to verify that an earlier selection cannot change.

A serious strategy study would predeclare objectives, costs, data contracts and acceptance gates; report every out-of-sample fold; and compare fold-count sensitivity, including N and N±1. This repository demonstrates the mechanics, not completed production WFA certification.

## Monte Carlo and plateau analysis

Seeded IID bootstrap resamples returns with replacement and reports path objects. It destroys serial dependence; block bootstrap and regime-aware stress scenarios would be extensions. Parameter plateau analysis reports contiguous regions on the supplied ordered candidate grid whose synthetic total return is within an explicit absolute tolerance of the best score. This is descriptive, not an out-of-sample acceptance test.

## Tests and CI

Tests use synthetic inputs and a socket guard. No credentials, IB software or data downloads are needed. CI installs pytest and runs the same test, demo and publication-scan commands. Dependency installation and GitHub Actions provisioning require network access; evaluation itself does not. The initial published implementation passed hosted CI on Python 3.11–3.13; see [Actions](https://github.com/TaylorYam/QuantCore-Public/actions) for current results.
