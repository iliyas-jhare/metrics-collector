import os
import re

import logging_wrapper


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
        latest = self.get_latest_hsp_config()
        numbers = re.findall(r"(\d+)", latest)
        if not numbers:
            log.error("No version numbers found in the directory name.")
            return None

        # Remove first number as it is not part of the HSP version
        numbers = numbers[1:]
        version = ".".join(numbers)
        return f"HSP{version}"

    def get_latest_hsp_config(self):
        """
        Finds the latest HSP configuration directory based on the naming convention.

        :return: The name of the latest HSP configuration directory or None if not found.
        """

        directories = [
            d
            for d in os.listdir(self._configs_path)
            if os.path.isdir(os.path.join(self._configs_path, d))
        ]
        if not directories:
            log.error("No directories found in the specified path.")
            return None
        directories.sort(reverse=True)
        return directories[0]
