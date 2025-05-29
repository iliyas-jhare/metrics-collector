import re

from logging_wrapper import LoggingWrapper
import text_reader

# TODO - Fetch from a config file for better user experience instead of hardcoding
SERVICE_PACK_VERSION_REGEX = r"<b>ServicePack:</b> \d+.\d+.\d+.\d+.\d+"
CONFIGURATOR_VERSION_REGEX = r"<b>Configurator:</b> \d+.\d+.\d+.\d+"


log = LoggingWrapper().get_logger(__name__)


class WhatsNewParser:
    """
    A class to read the "What's New" text file for the Drive Recorder tool.
    This class provides methods to read the entire content of the file or read it line by line.
    """

    def __init__(self, path):
        """
        Initializes the DriveRecorderWhatsNewReader with the specified file path.

        :param path: The path to the "What's New" text file.
        """

        self._path = path
        self._reader = text_reader.TextReader(path)

    def get_service_pack_and_configurator_version(self) -> tuple:
        """
        Extracts both the service pack and configurator versions from the "What's New" text file.

        :return: A tuple containing the service pack version and configurator version as strings.
        """

        contents = self._reader.read(encoding="utf-16")
        sp_version = self.__get_service_pack_version(contents)
        cfg_version = self.__get_configurator_version(contents)

        return sp_version, cfg_version

    def __get_service_pack_version(self, contents=str) -> str:
        """
        Extracts the service pack version from the contents

        :param contents: The contents of the "What's New" text file as a string.
        :return: The service pack version as a string.
        """

        match = re.search(SERVICE_PACK_VERSION_REGEX, contents)
        if match:
            # TODO expose naming convesion into a config file
            return f"SP{match.group(0).split(' ')[1]}"
        else:
            log.error("Service Pack version not found.")
            return None

    def __get_configurator_version(self, contents=str) -> str:
        """
        Extracts the configurator version from the contents

        :param contents: The contents of the "What's New" text file as a string.
        :return: The configurator version as a string.
        """

        match = re.search(CONFIGURATOR_VERSION_REGEX, contents)
        if match:
            # TODO expose naming convesion into a config file
            return f"CFG{match.group(0).split(' ')[1]}"
        else:
            log.error("Configurator version not found.")
            return None
