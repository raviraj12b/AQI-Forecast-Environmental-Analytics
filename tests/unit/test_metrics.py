import pytest
from src.evaluation.metrics import RegressionMetrics, calculate_regression_metrics

def test_perfect_predictions_give_zero_error_and_r2_one():
    m = calculate_regression_metrics([100,200,300],[100,200,300])
    assert m.mae==0 and m.mse==0 and m.rmse==0 and m.r2==pytest.approx(1.0)

def test_known_mae_value():
    m = calculate_regression_metrics([100,200,300],[110,190,310])
    assert m.mae==pytest.approx(10.0)

def test_known_rmse_is_sqrt_of_mse():
    m = calculate_regression_metrics([100,200,300],[110,190,310])
    assert m.rmse==pytest.approx(m.mse**0.5)

def test_returns_regression_metrics_dataclass():
    assert isinstance(calculate_regression_metrics([1,2,3],[1,2,3]), RegressionMetrics)

def test_to_dict_has_all_four_mandatory_metrics():
    d = calculate_regression_metrics([1,2,3],[1,2,4]).to_dict()
    assert set(d.keys())=={"MAE","MSE","RMSE","R2"}

def test_summary_is_readable_string():
    s = calculate_regression_metrics([1,2,3],[1,2,4]).summary()
    assert "MAE" in s and "R2" in s

def test_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        calculate_regression_metrics([1,2,3],[1,2])

def test_rejects_empty_input():
    with pytest.raises(ValueError):
        calculate_regression_metrics([],[])
