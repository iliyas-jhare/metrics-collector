import subprocess

from logging_wrapper import LoggingWrapper


log = LoggingWrapper().get_logger(__name__)


class SvnCommands:
    """
    Class to handle SVN commands.
    This class provides methods to execute SVN commands such as add, commit, and propset.
    """

    @staticmethod
    def add(path: str):
        """Adds the path to SVN repo."""
        try:
            return subprocess.run(["svn", "add", path], check=True)
        except subprocess.CalledProcessError as e:
            log.exception(e)

    @staticmethod
    def propset1(path: str, key: str, value: str):
        """Sets a property on the path in SVN repo."""
        try:
            return subprocess.run(["svn", "propset", key, value, path], check=True)
        except subprocess.CalledProcessError as e:
            log.exception(e)

    @staticmethod
    def propset2(path: str, props: dict):
        """Sets multiple properties on the path in SVN repo."""
        for key, value in props.items():
            SvnCommands.propset1(path, key, value)

    @staticmethod
    def commit(path: str, msg: str):
        """Commits changes to SVN repo."""
        try:
            return subprocess.run(["svn", "commit", path, "-m", msg], check=True)
        except subprocess.CalledProcessError as e:
            log.exception(e)
