import re

import logging_wrapper
import file_system


log = logging_wrapper.LoggingWrapper().get_logger(__name__)


class HspConfigs:
    """
    Class to handle HSP configurations by reading.
    """

    def __init__(self, configs_path):
        self._configs_path = configs_path

    def get_hsp_version(self):
        """
        Extracts the HSP version from the fwut log file.

        :return: The HSP version as a string.
        """
        latest = file_system.FileSystem.get_recent_directory(self._configs_path)
        numbers = re.findall(r"(\d+)", latest)
        if not numbers:
            log.error("No version numbers found in the directory name.")
            return None

        # Remove first number as it is not part of the HSP version
        numbers = numbers[1:]
        version = ".".join(numbers)
        return f"HSP{version}"
