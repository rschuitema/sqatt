"""Subprocess launcher.
"""
import logging
import shutil
from subprocess import DEVNULL  # nosec
from subprocess import CalledProcessError  # nosec
from subprocess import TimeoutExpired  # nosec
from subprocess import check_call  # nosec

LOG = logging.getLogger(__name__)


class ProcessError(Exception):
    """Generic process error."""


# pylint: disable=too-few-public-methods
class Subprocess:
    """Class to handle the execution of all command line tooling.

    User friendly subprocess wrapper, providing useful and informative
    error messages to the user in case of failures.
    """

    def __init__(self, command, stdout=DEVNULL, stderr=DEVNULL, verbose=0, timeout=None):  # pylint: disable=R0913
        """Class initializer.

        Creates a command object that can be executed.

        :param command: Command to execute on operating system in tuple format
        :param stdout: Optional location to redirect standard output stream
        :param stderr: Optional location to redirect error output stream
        :param verbose: Optional verbosity level of the processes output
        :param timeout: Optional variable providing command timeout
        """
        if not isinstance(command, (list, tuple)):
            raise ProcessError("Command (%s) is not of type list or tuple." % command)

        self.base_command = command[0]
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.timeout = timeout
        self.verbose = verbose

        command[0] = self._which()

    def _which(self):
        """Check if tool is available.

        Check if the tool that is to be executed is installed on the system.

        :return: tool location (Full path)
        """
        abspath = shutil.which(self.base_command)

        if not abspath:
            raise ProcessError(
                "%s is not installed on the system.\n"
                "Please make sure it is installed and added to the `PATH`." % self.base_command
            )

        LOG.debug("Located `%s` in `%s`", self.base_command, abspath)
        return abspath

    def execute(self):
        """Execute the command.

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
                self.command, stdout=stdout, stderr=stderr, shell=False, timeout=self.timeout,
            )  # nosec
        except CalledProcessError as error:
            raise ProcessError("%s returned a non-zero exit status %s" % (self.base_command, error.returncode)) \
                from error
        except TimeoutExpired as error:
            raise ProcessError("%s timed out after %s seconds" % (self.base_command, error.timeout)) from error

# pylint: enable=too-few-public-methods
