"""Unit tests for the reporting module."""

from unittest.mock import patch

from src.reporting.reporting import create_report_directory, setup_report_directory


@patch("os.path.exists")
def test_create_report_directory_directory_exists(path_exists_mock):
    """Test that the create report directory does not create the directory when it already exists."""

    # arrange
    directory = r"c:\temp\reports"
    path_exists_mock.return_value = True

    # act
    report_dir = create_report_directory(directory)

    # assert
    assert directory == report_dir
    path_exists_mock.assert_called_once()


@patch("os.makedirs")
@patch("os.path.exists")
def test_create_report_directory_directory_created(path_exists_mock, makedirs_mock):
    """Test that the create report directory creates the directory when it does not exist."""

    # arrange

    directory = r"c:\temp\reports"
    path_exists_mock.return_value = False

    # act
    report_dir = create_report_directory(directory)

    # assert
    assert directory == report_dir
    path_exists_mock.assert_called_once()
    makedirs_mock.assert_called_once()


@patch("os.makedirs")
@patch("shutil.rmtree")
@patch("os.path.exists")
def test_setup_directory_cleans_report_directory_if_it_exists(path_exists_mock, rm_tree_mock, makedirs_mock):
    """Test that the report directory is cleaned when it exists."""

    # arrange
    directory = "/data/reports"
    path_exists_mock.return_value = True

    # act
    report_dir = setup_report_directory(directory)

    # assert
    path_exists_mock.assert_called_once()
    rm_tree_mock.assert_called_once()
    makedirs_mock.assert_called_once()
    assert directory == report_dir


@patch("os.makedirs")
@patch("shutil.rmtree")
@patch("os.path.exists")
def test_setup_directory_creates_report_directory_if_it_does_not_exists(path_exists_mock, rm_tree_mock, makedirs_mock):
    """Test that the report directory is cleaned when it exists."""

    # arrange
    directory = "/data/reports"
    path_exists_mock.return_value = False

    # act
    report_dir = setup_report_directory(directory)

    # assert
    path_exists_mock.assert_called_once()
    rm_tree_mock.assert_not_called()
    makedirs_mock.assert_called_once()
    assert directory == report_dir
