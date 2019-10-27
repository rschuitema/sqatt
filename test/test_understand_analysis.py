"""Unit test for the commandline parser of the understand analysis."""
from unittest.mock import patch

import pytest

from src.understand.understand_analysis import parse_arguments


class AnalysisMocks:
    def __init__(self):
        self.code_size_patch = patch('src.understand.understand_analysis.analyze_code_size')
        self.complexity_patch = patch('src.understand.understand_analysis.analyze_complexity')
        self.fan_in_patch = patch('src.understand.understand_analysis.analyze_fan_in')
        self.fan_out_patch = patch('src.understand.understand_analysis.analyze_fan_out')
        self.function_size_patch = patch('src.understand.understand_analysis.analyze_function_size')
        self.file_size_patch = patch('src.understand.understand_analysis.analyze_file_size')
        self.interface_patch = patch('src.understand.understand_analysis.analyze_interface')
        self.code_size_mock = None
        self.complexity_mock = None
        self.fan_in_mock = None
        self.fan_out_mock = None
        self.function_size_mock = None
        self.file_size_mock = None
        self.interface_mock = None

    def start(self):
        print("start patching")
        self.code_size_mock = self.code_size_patch.start()
        self.complexity_mock = self.complexity_patch.start()
        self.fan_in_mock = self.fan_in_patch.start()
        self.fan_out_mock = self.fan_out_patch.start()
        self.function_size_mock = self.function_size_patch.start()
        self.file_size_mock = self.file_size_patch.start()
        self.interface_mock = self.interface_patch.start()

    def stop(self):
        print("stop patching")
        self.code_size_mock.stop()
        self.complexity_patch.stop()
        self.fan_in_patch.stop()
        self.fan_out_patch.stop()
        self.function_size_patch.stop()
        self.file_size_patch.stop()
        self.interface_patch.stop()


@pytest.fixture
def analysis_mocks():
    am = AnalysisMocks()
    am.start()
    yield am
    am.stop()


class MetricsMocks:
    def __init__(self):
        self.file_patch = patch('src.understand.understand_analysis.collect_file_metrics')
        self.function_patch = patch('src.understand.understand_analysis.collect_function_metrics')
        self.file_mock = None
        self.function_mock = None

    def start(self):
        self.file_mock = self.file_patch.start()
        self.function_mock = self.function_patch.start()

    def stop(self):
        self.file_patch.stop()
        self.function_patch.stop()


@pytest.fixture
def metrics_mocks():
    mm = MetricsMocks()
    mm.start()
    yield mm
    mm.stop()


def test_option_code_size_performs_only_code_size_analysis(analysis_mocks):
    # arrange
    args = parse_arguments(['analysis', '--code-size', 'db'])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_called_once()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_complexity_performs_only_complexity_analysis(analysis_mocks):
    # arrange
    args = parse_arguments(['analysis', '--complexity', 'db'])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_called_once()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_fan_in_performs_only_fan_in_analysis(analysis_mocks):
    # arrange
    args = parse_arguments(['analysis', '--fan-in', 'db'])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_called_once()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_fan_out_performs_only_fan_out_analysis(analysis_mocks):
    # arrange
    args = parse_arguments(['analysis', '--fan-out', 'db'])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_called_once()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_function_size_performs_only_function_size_analysis(analysis_mocks):
    # arrange
    args = parse_arguments(['analysis', '--function-size', 'db'])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_called_once()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_file_size_performs_only_file_size_analysis(analysis_mocks):
    # arrange
    args = parse_arguments(['analysis', '--file-size', 'db'])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_called_once()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_interface_performs_only_interface_analysis(analysis_mocks):
    # arrange
    args = parse_arguments(['analysis', '--interface', 'db'])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_called_once()


def test_option_all_performs_all_analysis(analysis_mocks):
    # arrange
    args = parse_arguments(['analysis', '--all', 'db'])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_called_once()
    analysis_mocks.complexity_mock.assert_called_once()
    analysis_mocks.fan_in_mock.assert_called_once()
    analysis_mocks.fan_out_mock.assert_called_once()
    analysis_mocks.function_size_mock.assert_called_once()
    analysis_mocks.file_size_mock.assert_called_once()
    analysis_mocks.interface_mock.assert_called_once()


def test_option_file_collects_only_file_metrics(metrics_mocks):
    # arrange
    args = parse_arguments(['metrics', '--file', 'db'])

    # act
    args.func(args)

    # assert
    metrics_mocks.file_mock.assert_called_once()
    metrics_mocks.function_mock.assert_not_called()


def test_option_module_should_have_correct_default_value(metrics_mocks):
    # arrange
    args = parse_arguments(['metrics', '--file', 'db'])

    # act
    args.func(args)

    # assert
    metrics_mocks.file_mock.assert_called_with('db', './reports', None, None)


def test_options_file_should_have_correct_values(metrics_mocks):
    # arrange
    args = parse_arguments(['metrics', '--file', '--output=/tmp/reports', '--module=foo', '--sort=CountLine', 'db'])

    # act
    args.func(args)

    # assert
    metrics_mocks.file_mock.assert_called_with('db', '/tmp/reports', 'foo', 'CountLine')


def test_option_function_collects_only_function_metrics(metrics_mocks):
    # arrange
    args = parse_arguments(['metrics', '--function', 'db'])

    # act
    args.func(args)

    # assert
    metrics_mocks.file_mock.assert_not_called()
    metrics_mocks.function_mock.assert_called_once()