from pathlib import Path
import math
import pytest
from quantcore.data import synthetic_prices, validate, load_csv
from quantcore.strategy import ToyTrend
from quantcore.backtest import run, metrics
from quantcore.robustness import walk_forward, bootstrap, plateau
from quantcore.portfolio import risk_weights, plan, PlannedOrder
from quantcore.execution import MockBroker, ib_preview

def test_fixture_provenance():
    path = Path(__file__).resolve().parents[1] / "data/sample/synthetic.csv"
    assert load_csv(path) == pytest.approx(synthetic_prices(), abs=1e-8)

@pytest.mark.parametrize("prices", [[], [1], [1, 0], [1, -1], [1, math.nan], [1, math.inf]])
def test_reject_bad_data(prices):
    with pytest.raises(ValueError): validate(prices)

def test_no_lookahead_and_turnover_cost():
    result = run([10, 20, 10], ToyTrend(2), cost_bps=100)
    assert result.returns == pytest.approx((0, -.51))
    assert result.max_drawdown == pytest.approx(-.51)

def test_strategy_receives_only_observed_prefix():
    class Spy:
        def __init__(self): self.seen = []
        def target(self, history): self.seen.append(tuple(history)); return 0
    spy = Spy(); run([11, 12, 13], spy)
    assert spy.seen == [(11,), (11, 12)]

def test_drawdown_includes_initial_capital():
    assert metrics([-.2, .1]).max_drawdown == pytest.approx(-.2)

def test_wfa_selection_ignores_future_and_covers_oos_once():
    prices = synthetic_prices()
    original = walk_forward(prices, (3, 7, 11), 32, 16)
    changed = walk_forward(prices[:32] + tuple(x * 2 for x in prices[32:]), (3, 7, 11), 32, 16)
    assert original[0].selected_window == changed[0].selected_window
    assert sum(len(f.returns) for f in original) == len(prices) - 32
    assert all(a.test_end == b.train_end for a,b in zip(original, original[1:]))

def test_bootstrap_reproducible_and_seed_sensitive():
    values = (.02, -.04, .01, .03)
    assert bootstrap(values, 8, 19) == bootstrap(values, 8, 19)
    assert bootstrap(values, 8, 19) != bootstrap(values, 8, 20)
    assert all(len(r.returns) == 4 for r in bootstrap(values, 8))

def test_plateau_flat_grid():
    scores, regions = plateau([10] * 20, (3, 7, 11), 0)
    assert regions == ((3, 7, 11),)
    assert set(scores.values()) == {0}

def test_inverse_risk_and_cash_residual():
    weights = risk_weights({"A": .1, "B": .2}, .6)
    assert weights == pytest.approx({"A": .4, "B": .2})
    assert plan(weights, {"A": 30, "B": 20}, {}, 100) == (PlannedOrder("A", 1), PlannedOrder("B", 1))

def test_liquidation_is_part_of_rebalance_plan():
    assert plan({}, {"OLD": 50}, {"OLD": 3}, 100) == (PlannedOrder("OLD", -3),)

@pytest.mark.parametrize("weights,prices,holdings,nav", [({"A": 1.1},{"A":1},{},100), ({"A":.5},{},{},100), ({},{"A":1},{"A":-1},100), ({},{},{},math.nan)])
def test_plan_fails_closed(weights, prices, holdings, nav):
    with pytest.raises(ValueError): plan(weights, prices, holdings, nav)

@pytest.mark.parametrize("qty,action", [(2,"BUY"),(-2,"SELL")])
def test_ib_mapping(qty, action):
    payload = ib_preview(PlannedOrder("SYNTH",qty), 12)
    assert payload["order"]["action"] == action
    assert payload["order"]["totalQuantity"] == 2
    assert payload["order"]["transmit"] is False
    assert payload["contract"]["secType"] == "STK"

def test_mock_idempotency_and_no_submission():
    broker = MockBroker(); order = PlannedOrder("SYNTH", 2)
    broker.preview("demo", order, 12); broker.preview("demo", order, 12)
    assert len(broker.events) == 1
    with pytest.raises(ValueError): broker.preview("demo", order, 13)
    with pytest.raises(RuntimeError): broker.submit(order)

def test_caller_cannot_mutate_stored_preview():
    broker = MockBroker()
    order = PlannedOrder("SYNTH", 2)
    payload = broker.preview("demo", order, 12)
    payload["order"]["totalQuantity"] = 999
    assert broker.preview("demo", order, 12)["order"]["totalQuantity"] == 2

def test_csv_rejects_duplicate_dates(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("date,symbol,close\n2000-01-01,SYNTH,10\n2000-01-01,SYNTH,11\n")
    with pytest.raises(ValueError): load_csv(path)

@pytest.mark.parametrize("train,test", [(2, 3), (20, 0), (100, 5)])
def test_invalid_walk_forward_sizes(train, test):
    with pytest.raises(ValueError):
        walk_forward(synthetic_prices(), (3, 7), train, test)

def test_invalid_bootstrap_and_plateau():
    with pytest.raises(ValueError): bootstrap([])
    with pytest.raises(ValueError): bootstrap([-.1], 0)
    with pytest.raises(ValueError): plateau(synthetic_prices(), [], .1)
    with pytest.raises(ValueError): plateau(synthetic_prices(), [3], -.1)

@pytest.mark.parametrize("window", [0, 1, -1, 2.5, True])
def test_bad_window(window):
    with pytest.raises(ValueError): ToyTrend(window)

def test_end_to_end(capsys):
    from quantcore.demo import main
    main()
    assert "ARTIFICIAL" in capsys.readouterr().out
