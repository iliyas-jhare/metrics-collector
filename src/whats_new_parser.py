import re

from logging_wrapper import LoggingWrapper
import text_reader

# TODO - Fetch from a config file for better user experience instead of hardcoding
HTML_TAGS_VERSION_REGEX = (
    r"(<b>ServicePack:</b> \d+.\d+.\d+.\d+.\d+|<b>Configurator:</b> \d+.\d+.\d+.\d+)"
)
SP_VERSION_REGEX = r"\d+.\d+.\d+.\d+.\d+"
CFG_VERSION_REGEX = r"\d+.\d+.\d+.\d+"


log = LoggingWrapper().get_logger(__name__)


class WhatsNewParser:
    """
    A class to read the "What's New" text file for the Drive Recorder tool.
    This class provides methods to read the entire content of the file or read it line by line.
    """

    def __init__(self, path=str, sp_version=str):
        """
        Initializes the DriveRecorderWhatsNewReader with the specified file path.

        :param path: The path to the "What's New" text file.
        :param sp_version: The service pack version to be used if not found in the file.
        """

        self._path = path
        self._sp_version = sp_version
        self._reader = text_reader.TextReader(path)

    def get_service_pack_and_configurator_version(self) -> tuple:
        """
        Extracts both the service pack and configurator versions from the "What's New" text file.

        :return: A tuple containing the service pack version and configurator version as strings.
        """

        contents = self._reader.read(encoding="utf-16")
        if contents is None:
            log.error("Failed to read the contents of the 'What's New' file.")
            return None, None

        map = self.__create_version_map(contents)
        if not map:
            log.error("No service pack or configurator version found in the contents.")
            return None, None

        if value := map.get(self._sp_version):
            return self._sp_version, value
        else:
            key = list(map)[0]
            value = list(map.values())[0]
            return key, value

        return None, None

    def __create_version_map(self, contents=str) -> dict:
        """
        Creates a dictionary mapping service pack and configurator versions to their respective values.

        :param contents: The contents of the "What's New" text file as a string.
        :return: A dictionary with service pack and configurator versions.
        """

        map = {}
        html_tags = re.findall(HTML_TAGS_VERSION_REGEX, contents)
        if not html_tags:
            log.error("No service pack or configurator version found in the contents.")
            return map

        key = None
        value = None
        for tag in html_tags:
            key = self.__get_version(tag)
            value = self.__get_version(tag)
            if key and value:
                map[key] = value
                key = None
                value = None
        return map

    def __get_version(self, tag=str) -> str:
        """
        Extracts the version from the given HTML tag.

        :param tag: The HTML tag containing the version information.
        :return: The extracted version as a string.
        """
        if "ServicePack:" in tag:
            return f"SP{re.search(SP_VERSION_REGEX, tag).group(0)}"
        elif "Configurator:" in tag:
            return f"CFG{re.search(CFG_VERSION_REGEX, tag).group(0)}"
        return None
