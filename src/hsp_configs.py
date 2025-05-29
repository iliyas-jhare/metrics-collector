import re

from logging_wrapper import LoggingWrapper
from file_system import FileSystem


log = LoggingWrapper().get_logger(__name__)


class HspConfigs:
    """
    Class to handle HSP configurations by reading.
    """

    def __init__(self, configs_path):
        self._configs_path = configs_path

    def get_hsp_version(self) -> str:
        """
        Extracts the HSP version from the fwut log file.

        :return: The HSP version as a string.
        """
        recent = FileSystem.get_recent_directory(self._configs_path)
        numbers = re.findall(r"(\d+)", recent)
        if not numbers:
            log.error("No version numbers found in the directory name.")
            return None

        # Remove first number as it is not part of the HSP version
        numbers = numbers[1:]
        version = ".".join(numbers)
        return f"HSP{version}"
