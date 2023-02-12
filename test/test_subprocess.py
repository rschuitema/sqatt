"""Unit tests for SubProcess."""

from subprocess import CalledProcessError, DEVNULL, TimeoutExpired  # nosec
from os.path import join
from types import SimpleNamespace
from unittest import TestCase

from mock import call, patch
from pytest import raises

from src.facility.subprocess import ProcessError, Subprocess, SubprocessRuntimeError


class TestSubprocess(TestCase):
    """Test the Subprocess class."""

    def setUp(self):
        """Prepare the test cases."""

        self.which_mock = patch("src.facility.subprocess.which").start()
        self.check_call_mock = patch("src.facility.subprocess.check_call").start()

        # Arrange
        self.which_mock.return_value = "/test_path/test_command"
        self.check_call_mock.return_value.returncode = 0

    def tearDown(self):
        """Teardown the test cases."""

        patch.stopall()

    @staticmethod
    def test_subprocess_throws_exception_when_providing_command_as_plain_string():
        """Test that subprocess throws an exception when a command is provided as plain string."""

        # Arrange
        command = "test_command test_arguments"

        # Act
        # Assert
        with raises(SubprocessRuntimeError):
            Subprocess(command)

    def test_which_is_successful_with_correct_parameters(self):
        """Test that which is successful with correct parameters."""

        # Arrange
        command = ["test_command", "test_arguments"]
        self.which_mock.return_value = "/long/test/path/test_command"

        # Act
        process = Subprocess(command)

        # Assert
        self.which_mock.assert_called_with("test_command")
        assert process.base_command == "test_command"
        assert process.command[0] == "/long/test/path/test_command"

    def test_which_raises_exception_with_shutil_which_returning_none(self):
        """Test that which raises an exception with shutil."""

        # Arrange
        command = ["unexisting_test_command", "test_arguments"]
        self.which_mock.return_value = None

        # Act
        with raises(SubprocessRuntimeError):
            Subprocess(command)

        # Assert
        self.which_mock.assert_called_once_with("unexisting_test_command")

    def test_execute_is_successful_with_correct_command_parameters(self):
        """Test that execute is successful with correct command parameters."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command)

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout=DEVNULL,
            stderr=DEVNULL,
            shell=False,
            timeout=None,
        )

    def test_standard_streams_are_modified_when_overridden(self):
        """Test that standard streams are modified when overridden."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream")

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout="stdout_stream",
            stderr="stderr_stream",
            shell=False,
            timeout=None,
        )

    def test_execute_runs_subprocess_with_stderr_output_with_verbose_is_2(self):
        """Test that execute run subprocess with stderr output with verbose level 2."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=2)

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout="stdout_stream",
            stderr=None,
            shell=False,
            timeout=None,
        )

    def test_execute_runs_subprocess_with_stdout_and_stderr_output_with_verbose_is_3(self):
        """Test that execute run subprocess with stdout and stderr output with verbose level 3."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=3)

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout=None,
            stderr=None,
            shell=False,
            timeout=None,
        )

    def test_execute_runs_subprocess_with_stdout_and_stderr_default_constructor_output_with_verbose_is_3(self):
        """Test that execute runs subprocess with default constructor with stdout and stderr output with verbose
        level 2."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command, verbose=3)

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout=None,
            stderr=None,
            shell=False,
            timeout=None,
        )

    def test_execute_runs_subprocess_with_stdout_and_stderr_output_with_verbose_is_greater_than_3(self):
        """Test that execute runs subprocess with stdout and stderr output with verbose level > 3."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=8)

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout=None,
            stderr=None,
            shell=False,
            timeout=None,
        )

    def test_execute_runs_subprocess_with_stdout_redirect_with_defined_stdout_stream_and_verbose_smaller_than_3(self):
        """Test that execute run subprocess with stdout redirected to stream output with verbose level < 3."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=1)

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout="stdout_stream",
            stderr="stderr_stream",
            shell=False,
            timeout=None,
        )

    def test_execute_runs_subprocess_with_stdout_redirect_with_defined_stdout_stream_and_verbose_greater_than_3(self):
        """Test that execute run subprocess with stdout redirected to stream output with verbose level > 3."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command, stdout="stdout_stream", stderr="stderr_stream", verbose=8)

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout=None,
            stderr=None,
            shell=False,
            timeout=None,
        )

    def test_execute_runs_subprocess_with_correct_timeout_value_with_timeout_set(self):
        """Test that execute runs subprocess times out at specified moment."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command, timeout=180)

        # Act
        process.execute()

        # Assert
        self.check_call_mock.assert_called_once_with(
            ["/test_path/test_command", "test_arguments"],
            stdout=DEVNULL,
            stderr=DEVNULL,
            shell=False,
            timeout=180,
        )

    def test_execute_raises_exception_with_subprocess_called_process_error_exception(self):
        """Test that execute raises an process error exception."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command)

        self.check_call_mock.side_effect = CalledProcessError("Error", "process_name")

        # Act
        # Assert
        with raises(ProcessError):
            process.execute()

    def test_execute_raises_exception_with_subprocess_timeout_expired_exception(self):
        """Test that execute raises and process timeout expired exception."""

        # Arrange
        command = ["test_command", "test_arguments"]
        process = Subprocess(command)

        self.check_call_mock.side_effect = TimeoutExpired("Error", "timout_value")

        # Act
        # Assert
        with raises(ProcessError):
            process.execute()


class TestSubprocessPipe(TestCase):
    """Test the SubprocessPipe class."""

    def setUp(self):
        """Prepare of the test cases."""

        self.which_mock = patch("src.facility.subprocess.which").start()
        self.open_mock = patch("src.facility.subprocess.open").start()
        self.print_mock = patch("src.facility.subprocess.print").start()
        self.run_mock = patch("src.facility.subprocess.run").start()
        self.strftime_mock = patch("src.facility.subprocess.strftime").start()

        # Arrange
        self.which_mock.return_value = "/test_path/test_command"
        self.run_mock.return_value = SimpleNamespace(stdout=b"standard_output", returncode=0)
        self.strftime_mock.return_value = "yyyymmdd-hhmmss"

    def tearDown(self):
        """Tear down of test cases."""

        patch.stopall()

    @staticmethod
    def test_execute_pipe_when_command_is_executed_successful_then_stdout_is_returned():
        """Test that execute pipe returns stdout when successful."""

        # Arrange
        command = ["test_command", "test_arguments"]

        # Act
        process = Subprocess(command)
        output = process.execute_pipe("test_directory", "filename")

        # Assert
        assert output.stdout == b"standard_output"

    def test_execute_pipe_when_command_is_executed_then_stdout_is_saved_to_file(self):
        """Test that execute pipe saves sdtout to file."""

        # Arrange
        command = ["test_command", "test_arguments"]

        # Act
        process = Subprocess(command)
        process.execute_pipe("test_directory", "filename")

        # Assert
        self.open_mock.assert_called_once_with(join("test_directory", "filename_yyyymmdd-hhmmss.log"), "wb")
        self.open_mock.assert_has_calls([call().__enter__().write(b"standard_output")])

    def test_execute_pipe_when_unable_to_open_logfile_then_subprocess_runtime_error_is_raised(self):
        """Test that execute pipe raises runtime error when unable to open logfile."""

        # Arrange
        command = ["test_command", "test_arguments"]
        self.open_mock.side_effect = FileNotFoundError(None, None, "filename")

        # Act
        process = Subprocess(command)
        with raises(SubprocessRuntimeError) as exception:
            process.execute_pipe("test_directory", "filename")

        # Assert
        assert (
            str(exception.value) == "Unable to open ('filename') and write results.\n"
            "Please use preconditions to enforce: ['OutputDirectoryExists', 'OutputDirectoryIsEmpty']."
        )

    def test_execute_pipe_when_non_zero_return_code_then_stdout_is_saved_to_file(self):
        """Test that stdout is saved to file when non zero is returned."""

        # Arrange
        command = ["test_command", "test_arguments"]
        self.run_mock.return_value = SimpleNamespace(stdout=b"standard_output", returncode=1)

        # Act
        process = Subprocess(command)
        with raises(ProcessError):
            process.execute_pipe("test_directory", "filename")

        # Assert
        self.open_mock.assert_called_once_with(join("test_directory", "filename_yyyymmdd-hhmmss.log"), "wb")
        self.open_mock.assert_has_calls([call().__enter__().write(b"standard_output")])

    def test_execute_pipe_when_verbose_is_less_than_3_then_stdout_is_not_printed_to_terminal(self):
        """Test that stdout is not printed to terminal when verbose level < 3."""

        # Arrange
        command = ["test_command", "test_arguments"]

        # Act
        process = Subprocess(command, verbose=2)
        process.execute_pipe("test_directory", "filename")

        # Assert
        self.print_mock.assert_not_called()

    def test_execute_pipe_when_verbose_equals_3_then_stdout_printed_to_terminal(self):
        """Test that stdout is printed to terminal when verbose level = 3."""

        # Arrange
        command = ["test_command", "test_arguments"]

        # Act
        process = Subprocess(command, verbose=3)
        process.execute_pipe("test_directory", "filename")

        # Assert
        self.print_mock.assert_called_once_with("standard_output")

    def test_execute_pipe_when_verbose_is_greater_than_3_then_stdout_is_printed_to_terminal(self):
        """Test that stdout is printed to terminal when verbose level > 3."""

        # Arrange
        command = ["test_command", "test_arguments"]

        # Act
        process = Subprocess(command, verbose=8)
        process.execute_pipe("test_directory", "filename")

        # Assert
        self.print_mock.assert_called_once_with("standard_output")
