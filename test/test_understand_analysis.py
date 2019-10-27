"""Unit test for the commandline parser of the understand analysis."""
from unittest.mock import patch

from src.understand.understand_analysis import parse_arguments


@patch('src.understand.understand_analysis.analyze_code_size')
def test_option_code_size_performs_code_size_analysis(acs_mock):
    # arrange

    # act
    args = parse_arguments(['analysis', '--code-size', 'db'])
    args.func(args)

    # assert
    acs_mock.assert_called_once()
