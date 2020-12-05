from subprocess import DEVNULL  # nosec
from subprocess import CalledProcessError  # nosec
from subprocess import TimeoutExpired  # nosec

from unittest import mock

import pytest

from src.facility.subprocess import ProcessError
from src.facility.subprocess import Subprocess


def test_subprocess_throws_exception_when_providing_command_as_plain_string():
    # Arrange
    command = "test_command test_arguments"

    # Act
    # Assert
    with pytest.raises(ProcessError):
        Subprocess(command)


@mock.patch("shutil.which")
def test_which_is_successful_with_correct_parameters(which_mock,):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "/test_path/test_command"

    # Act
    process = Subprocess(command)
    return_value = process._which()

    # Assert
    which_mock.assert_called_with("test_command")
    assert return_value == "/test_path/test_command"


@mock.patch("shutil.which")
def test_which_raises_exception_with_shutil_which_returning_none(which_mock,):
    # Arrange
    command = ["unexisting_test_command", "test_arguments"]
    which_mock.return_value = None

    # Act
    # Assert
    with pytest.raises(ProcessError):
        Subprocess(command)

    which_mock.assert_called_once_with("unexisting_test_command")


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_is_successful_with_correct_command_parameters(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command)
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"], stdout=DEVNULL, stderr=DEVNULL, shell=False, timeout=None,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_standard_streams_are_modified_when_overridden(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream")
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"],
        stdout="stdout_stream",
        stderr="stderr_stream",
        shell=False,
        timeout=None,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_runs_subprocess_with_stderr_output_with_verbose_is_2(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=2)
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"], stdout="stdout_stream", stderr=None, shell=False, timeout=None,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_runs_subprocess_with_stdout_and_stderr_output_with_verbose_is_3(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=3)
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"], stdout=None, stderr=None, shell=False, timeout=None,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_runs_subprocess_with_stdout_and_stderr_default_constructor_output_with_verbose_is_3(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command, verbose=3)
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"], stdout=None, stderr=None, shell=False, timeout=None,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_runs_subprocess_with_stdout_and_stderr_output_with_verbose_is_greater_than_3(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=8)
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"], stdout=None, stderr=None, shell=False, timeout=None,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_runs_subprocess_with_stdout_redirect_with_defined_stdout_stream_and_verbose_smaller_than_3(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=1)
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"],
        stdout="stdout_stream",
        stderr="stderr_stream",
        shell=False,
        timeout=None,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_runs_subprocess_with_stdout_redirect_with_defined_stdout_stream_and_verbose_greater_than_3(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=8)
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"], stdout=None, stderr=None, shell=False, timeout=None,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_runs_subprocess_with_correct_timeout_value_with_timeout_set(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command, timeout=180)
    subprocess_mock.return_value.returncode = 0

    # Act
    process.execute()

    # Assert
    subprocess_mock.assert_called_once_with(
        ["test_path/test_command", "test_arguments"], stdout=DEVNULL, stderr=DEVNULL, shell=False, timeout=180,
    )


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_raises_exception_with_subprocess_called_process_error_exception(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command)
    subprocess_mock.side_effect = CalledProcessError("Error", "process_name")

    # Act
    # Assert
    with pytest.raises(ProcessError):
        process.execute()


@mock.patch("src.facility.subprocess.check_call")
@mock.patch("shutil.which")
def test_execute_raises_exception_with_subprocess_timeout_expired_exception(
    which_mock, subprocess_mock,
):
    # Arrange
    command = ["test_command", "test_arguments"]
    which_mock.return_value = "test_path/test_command"

    process = Subprocess(command)
    subprocess_mock.side_effect = TimeoutExpired("Error", "timout_value")

    # Act
    # Assert
    with pytest.raises(ProcessError):
        process.execute()
