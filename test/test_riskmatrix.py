"""This module tests the functionality of the RiskMatrix class."""

from src.riskmatrix.risk_matrix import RiskMatrix


def test_read_metric_thresholds():
    """Test that the metric thresholds can be read form a csv file."""

    matrix = RiskMatrix()
    matrix.add_metric_thresholds(r'../src/riskmatrix/quadrant_metric_thresholds.csv')

    q1_thresholds = matrix.metric_thresholds['Q1']
    assert q1_thresholds['Complexity'] == '< 5'


def test_read_component_risk_level():
    """Test that the component risk level can be read from csv file."""
    matrix = RiskMatrix()

    matrix.add_component_risk_level('component_risk_level.csv')

    assert matrix.component_risk_level['ComponentA'] == 'Q1'


def test_all_component_comply_verify_metric_returns_true():
    """Test that verify metric returns true if all component comply to the metric."""

    matrix = RiskMatrix()
    matrix.add_metric_thresholds(r'../src/riskmatrix/quadrant_metric_thresholds.csv')
    matrix.add_component_risk_level('component_risk_level.csv')

    result = matrix.verify_metric('component_coverage.csv')

    assert result is True
