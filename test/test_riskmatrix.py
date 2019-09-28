"""This module tests the functionality of the RiskMatrix class."""
import csv
from io import StringIO
from unittest.mock import patch, mock_open
from src.riskmatrix.risk_matrix import RiskMatrix


def test_read_metric_thresholds():
    """Test that the metric thresholds can be read form a csv file."""

    thresholds = StringIO("""Quadrant, Complexity, Function size, Coverage
    Q1, < 5,< 15,> 80
    Q2, < 8,< 30,> 95
    Q3, < 16,< 50,> 70
    Q4, < 20,< 100,> 60""")

    threshold_file = r'../src/riskmatrix/quadrant_metric_thresholds.csv'
    matrix = RiskMatrix()

    test_reader = csv.DictReader(thresholds, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    with patch('src.riskmatrix.risk_matrix.open', mock_open()) as mocked_file:
        matrix.add_metric_thresholds(threshold_file, test_reader)

    mocked_file.assert_called_once_with(threshold_file)
    q1_thresholds = matrix.metric_thresholds['Q1']
    assert len(matrix.metric_thresholds) == 4
    assert q1_thresholds['Complexity'] == '< 5'
    assert q1_thresholds['Function size'] == '< 15'
    assert q1_thresholds['Coverage'] == '> 80'


def test_read_component_risk_level():
    """Test that the component risk level can be read from csv file."""

    risk_level = StringIO("""Component, Quadrant
    ComponentA, Q1
    ComponentB, Q3
    ComponentC, Q2
    ComponentD, Q4
    ComponentE, Q2
    ComponentF, Q1""")

    matrix = RiskMatrix()
    risk_level_file = r'component_risk_level.csv'

    test_reader = csv.DictReader(risk_level, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    with patch('src.riskmatrix.risk_matrix.open', mock_open()) as mocked_file:
        matrix.add_component_risk_level(risk_level_file, test_reader)

    mocked_file.assert_called_once_with(risk_level_file)
    assert len(matrix.component_risk_level) == 6
    assert matrix.component_risk_level['ComponentA'] == 'Q1'
    assert matrix.component_risk_level['ComponentB'] == 'Q3'
    assert matrix.component_risk_level['ComponentC'] == 'Q2'
    assert matrix.component_risk_level['ComponentD'] == 'Q4'
    assert matrix.component_risk_level['ComponentE'] == 'Q2'
    assert matrix.component_risk_level['ComponentF'] == 'Q1'


def test_all_component_comply_verify_metric_returns_true():
    """Test that verify metric returns true if all component comply to the metric."""

    # arrange
    coverage = StringIO("""Component, Coverage
    ComponentA, 77
    ComponentB, 99
    ComponentC, 99
    ComponentD, 60
    ComponentE, 99
    ComponentF, 55""")

    matrix = RiskMatrix()
    add_metric_thresholds(matrix)
    add_component_risk_levels(matrix)

    # act
    component_coverage_file = r'component_coverage.csv'
    reader = csv.DictReader(coverage, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    with patch('src.riskmatrix.risk_matrix.open', mock_open()) as mocked_file:
        result = matrix.verify_metric(component_coverage_file, reader)

        # assert
        mocked_file.assert_called_once_with(component_coverage_file)
        assert result is True


def test_one_component_does_not_comply_verify_metric_returns_false():
    """Test that verify metric returns false if one component does not comply to the metric."""

    # arrange
    coverage = StringIO("""Component, Coverage
    ComponentA, 77
    ComponentB, 99
    ComponentC, 66
    ComponentD, 60
    ComponentE, 99
    ComponentF, 59""")

    matrix = RiskMatrix()
    add_metric_thresholds(matrix)
    add_component_risk_levels(matrix)

    # act
    component_coverage_file = r'component_coverage.csv'
    reader = csv.DictReader(coverage, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    with patch('src.riskmatrix.risk_matrix.open', mock_open()) as mocked_file:
        result = matrix.verify_metric(component_coverage_file, reader)

        # assert
        mocked_file.assert_called_once_with(component_coverage_file)
        assert result is False


def add_component_risk_levels(matrix, risk_levels=None):
    """Add risk levels for the components to the matrix."""

    risk_levels = risk_levels or StringIO("""Component, Quadrant
    ComponentA, Q1
    ComponentB, Q3
    ComponentC, Q2
    ComponentD, Q4
    ComponentE, Q2
    ComponentF, Q1""")

    component_risk_file = r'component_risk_level.csv'
    reader = csv.DictReader(risk_levels, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    with patch('src.riskmatrix.risk_matrix.open', mock_open()):
        matrix.add_component_risk_level(component_risk_file, reader)


def add_metric_thresholds(matrix, thresholds=None):
    """Add metric threshold for each quadrant to the matrix."""

    thresholds = thresholds or StringIO("""Quadrant, Complexity, Function size, Coverage
    Q1, < 5,< 15,< 80
    Q2, < 8,< 30,> 95
    Q3, < 16,< 50,>= 70
    Q4, < 20,< 100,<= 60""")

    threshold_file = r'../src/riskmatrix/quadrant_metric_thresholds.csv'
    reader = csv.DictReader(thresholds, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    with patch('src.riskmatrix.risk_matrix.open', mock_open()):
        matrix.add_metric_thresholds(threshold_file, reader)
