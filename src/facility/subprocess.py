"""Subprocess wrapper."""

from logging import getLogger
from os.path import join
from shutil import which
from time import strftime
from subprocess import CalledProcessError, DEVNULL, PIPE, STDOUT, Popen, TimeoutExpired, check_call, run  # nosec

LOG = getLogger(__name__)


class ProcessError(Exception):
    """
    Process error.

    Something went wrong executing the Python subprocess call
    """


class SubprocessRuntimeError(Exception):
    """
    Runtime error.

    Something went wrong before or after the Python subprocess call
    """


# pylint: disable=too-few-public-methods
class Subprocess:
    """
    Class to handle the execution of all command line tooling.

    User friendly subprocess wrapper, providing useful and informative
    error messages to the user in case of failures.
    """

    def __init__(self, command, stdout=DEVNULL, stderr=DEVNULL, verbose=0, timeout=None):  # pylint: disable=R0913
        """
        Class initializer.

        Creates a command object that can be executed.

        :param command: Command to execute on operating system in tuple format
        :param stdout: Optional location to redirect standard output stream
        :param stderr: Optional location to redirect error output stream
        :param verbose: Optional verbosity level of the processes output
        :param timeout: Optional variable providing command timeout
        """
        if not isinstance(command, (list, tuple)):
            raise SubprocessRuntimeError("Command (%s) is not of type list or tuple." % command)

        self.base_command = command[0]
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.timeout = timeout
        self.verbose = verbose

        command[0] = self.__which()

    def __which(self):
        """
        Check if tool is available.

        Check if the tool that is to be executed is installed on the system.

        :return: tool location (Full path)
        """
        abspath = which(self.base_command)

        if not abspath:
            raise SubprocessRuntimeError(
                "%s is not installed on the system.\n"
                "Please make sure it is installed and added to the `PATH`." % self.base_command
            )

        LOG.debug("Located `%s` in `%s`", self.base_command, abspath)
        return abspath

    def execute(self):
        """
        Execute the command.

        Execute the command as defined in the object. Raising informative exceptions
        in case of an `execution error` or `command timeout`.
        """
        stdout = self.stdout
        stderr = self.stderr

        if self.verbose == 2:
            stderr = None
        elif self.verbose >= 3:
            stdout = None
            stderr = None

        try:
            LOG.debug("Starting call: %s", self.command)
            check_call(
                self.command,
                stdout=stdout,
                stderr=stderr,
                shell=False,
                timeout=self.timeout,
            )  # nosec
        except CalledProcessError as error:
            raise ProcessError(
                "%s returned a non-zero exit status %s" % (self.base_command, error.returncode)
            ) from error
        except TimeoutExpired as error:
            raise ProcessError("%s timed out after %s seconds" % (self.base_command, error.timeout)) from error

    def execute_async(self):
        """
        Execute the command asynchronously.

        Execute the command asynchronously as defined in the object and don't wait on or check any return value.
        Raising informative exceptions in case of an `Operating System error` or `Value error`.
        """
        try:
            LOG.debug("Starting asynchronous call: %s", self.command)
            Popen(self.command)  # nosec
        except ValueError as error:
            raise ProcessError("%s has an invalid argument: %s" % (self.base_command, error.args)) from error
        except OSError as error:
            raise ProcessError(
                "%s returned an OS error: %s '%s' %s" % (self.base_command, error.errno, error.strerror, error.filename)
            ) from error

    def execute_pipe(self, output_directory, filename, check_return_code=True):
        """
        Execute command returning stdout as string.

        Execute the command as defined in the object returning process
        information. This command will always produce a log file with the
        output of the executed command. With the possibility to raise an
        informative exception in case of a non-zero return code.

        :param output_directory: log file output directory
        :param filename log file filename
        :param check_return_code: Optional raise exception with non-zero return code
        :return: Subprocess CompletedProcess object
        """
        LOG.debug("Starting call: %s", self.command)

        command_output = run(
            self.command,
            stdout=PIPE,
            stderr=STDOUT,
            shell=False,
            check=False,
            timeout=self.timeout,
        )  # nosec

        self.__write_log_file(output_directory, filename, command_output)

        if self.verbose >= 3:
            print(command_output.stdout.decode("utf-8"))

        if command_output.returncode != 0 and check_return_code:
            raise ProcessError("%s returned a non-zero exit status %s" % (self.base_command, command_output.returncode))

        return command_output

    @staticmethod
    def __write_log_file(output_directory, filename, command_output):
        """
        Write process data to log file.

        Write command output to unique (timestamped) log file based on the
        provided `output_directory` and `filename`.

        :param output_directory: log file output directory
        :param filename log file filename
        :param command_output: Optional raise exception with non-zero return code
        """
        try:
            with open(join(output_directory, "{}_{}.log".format(filename, strftime("%Y%m%d-%H%M%S"))), "wb") as file:
                file.write(command_output.stdout)
        except FileNotFoundError as exception:
            raise SubprocessRuntimeError(
                "Unable to open ('%s') and write results.\nPlease use preconditions to enforce: "
                "['OutputDirectoryExists', 'OutputDirectoryIsEmpty']." % exception.filename
            ) from exception


# pylint: enable=too-few-public-methods
