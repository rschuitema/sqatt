"""Unit tests for the dotcover functions."""
from unittest.mock import patch, Mock, call, mock_open

import pytest
import xmltodict

from src.dotcover.dotcover import get_namespaces, determine_namespaces, determine_coverage_of_namespace, \
    save_coverage_per_namespace


def test_get_namespaces_empty_input_returns_empty_set():
    """Test that an empty set is return when the input is empty."""

    # arrange
    line = ''

    # act
    namespaces = get_namespaces(line, '.')

    # assert
    assert namespaces == set()


def test_get_namespace_one_namespace_input_returns_one_item_in_set():
    """Test that one item is returned when the input contains one namespace."""

    # arrange
    line = 'root'
    expected_namespaces = {'root'}

    # act
    namespaces = get_namespaces(line, '.')

    # assert
    assert namespaces == expected_namespaces


def test_get_names_several_namespaces_input_return_correct_items_in_set():
    """Test that a set is returned when the input contains several namespaces."""

    # arrange
    line = 'root.directory.subdirectory.file'
    expected_namespaces = {'root.directory.subdirectory.file', 'root.directory.subdirectory', 'root.directory', 'root'}
    # act
    namespaces = get_namespaces(line, '.')

    # assert
    assert namespaces == expected_namespaces


def test_get_namespaces_wrong_separator_returns_one_item_in_set():
    """Test that one namespace is returned when the separator is incorrect."""

    # arrange
    line = 'root.directory.subdirectory.file'
    expected_namespaces = {'root.directory.subdirectory.file'}
    # act
    namespaces = get_namespaces(line, ':')

    # assert
    assert namespaces == expected_namespaces


def test_get_namespaces_different_separator_returns_correct_items_in_set():
    """Test that namespaces can be found with a different separator."""

    # arrange
    line = 'root:directory:subdirectory:file'
    expected_namespaces = {'root:directory:subdirectory:file', 'root:directory:subdirectory', 'root:directory', 'root'}
    # act
    namespaces = get_namespaces(line, ':')

    # assert
    assert namespaces == expected_namespaces


def test_get_namespaces_two_separator_input_returns_correct_items_in_set():
    """Test that the correct namespaces are returned when the input contains two separators."""

    # arrange
    line = 'root:directory:subdirectory,file'
    expected_namespaces = {'root:directory:subdirectory,file', 'root:directory', 'root'}
    # act
    namespaces = get_namespaces(line, ':')

    # assert
    assert namespaces == expected_namespaces


def test_determine_namespaces_returns_correct_namespaces():
    """Test that the correct namespaces are returned when the input contains several assemblies."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Root CoveredStatements="7198" TotalStatements="24118" CoveragePercent="30" ReportType="Xml" ' \
                  r'DotCoverVersion="2019.1.1">' \
                  r'<Assembly Name="A.B.C.C" CoveredStatements="107" TotalStatements="116" ' \
                  r'CoveragePercent="92"></Assembly>' \
                  r'<Assembly Name="A.B.C.E" CoveredStatements="0" TotalStatements="102" ' \
                  r'CoveragePercent="0"></Assembly>' \
                  r'<Assembly Name="A.B.D.F" CoveredStatements="70" TotalStatements="143" ' \
                  r'CoveragePercent="49"></Assembly>' \
                  r'</Root>'

    expected_namespaces = {'A.B.C.C', 'A.B.C', 'A.B', 'A',
                           'A.B.C.E', 'A.B.D.F', 'A.B.D'}

    doc = xmltodict.parse(xml_to_read)

    # act
    namespaces = determine_namespaces(doc)

    # assert
    assert namespaces == expected_namespaces


def test_determine_namespaces_one_assembly_returns_correct_namespaces():
    """Test that the  correct namespaces are returned when the input contains one assembly."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Root CoveredStatements="7198" TotalStatements="24118" CoveragePercent="30" ReportType="Xml" ' \
                  r'DotCoverVersion="2019.1.1">' \
                  r'<Assembly Name="A.B.C.C" CoveredStatements="107" TotalStatements="116" ' \
                  r'CoveragePercent="92"></Assembly>' \
                  r'</Root>'

    expected_namespaces = {'A.B.C.C', 'A.B.C', 'A.B', 'A'}

    doc = xmltodict.parse(xml_to_read)

    # act
    namespaces = determine_namespaces(doc)

    # assert
    assert namespaces == expected_namespaces


def test_determine_coverage_for_namespace_one_assembly_correct_coverage():
    """Test that the coverage is determined correctly when the input contains one assembly."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Root CoveredStatements="7198" TotalStatements="24118" CoveragePercent="30" ReportType="Xml" ' \
                  r'DotCoverVersion="2019.1.1">' \
                  r'<Assembly Name="A.B.C.C" CoveredStatements="107" TotalStatements="116" ' \
                  r'CoveragePercent="92"></Assembly>' \
                  r'</Root>'

    doc = xmltodict.parse(xml_to_read)

    # act
    coverage = determine_coverage_of_namespace(doc, 'A.B.C.C')

    # assert
    assert coverage == pytest.approx(92.2, 0.1)


def test_determine_coverage_for_namespace_several_assemblies_correct_coverage():
    """Test that the coverage is determined correctly when the input contains several assemblies."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Root CoveredStatements="7198" TotalStatements="24118" CoveragePercent="30" ReportType="Xml" ' \
                  r'DotCoverVersion="2019.1.1">' \
                  r'<Assembly Name="A.B.C.C" CoveredStatements="100" TotalStatements="200" ' \
                  r'CoveragePercent="92"></Assembly>' \
                  r'<Assembly Name="A.B.C.E" CoveredStatements="80" TotalStatements="200" ' \
                  r'CoveragePercent="92"></Assembly>' \
                  r'<Assembly Name="A.B.C.Control" CoveredStatements="10" TotalStatements="100" ' \
                  r'CoveragePercent="92"></Assembly>' \
                  r'</Root>'

    doc = xmltodict.parse(xml_to_read)

    # act
    coverage = determine_coverage_of_namespace(doc, 'A.B.C')

    # assert
    assert coverage == pytest.approx(38.0, 0.1)


@patch('src.dotcover.dotcover.csv')
def test_save_coverage_per_namespace(csv_mock):
    """Test that the resulting issues can be saved."""

    items = {'A': 15, 'b': 8}
    csv_mock.writer = Mock(writerow=Mock())
    report_dir = r'/tmp/'
    calls = [call.writerow(['Namespace', 'Coverage']), call.writerow(['A', 15]), call.writerow(['b', 8])]
    with patch('src.dotcover.dotcover.open', mock_open()) as mocked_file:
        save_coverage_per_namespace(items, report_dir)

        mocked_file.assert_called_once_with(report_dir + r'coverage_per_namespace.csv', 'w')

        csv_mock.writer().assert_has_calls(calls)
