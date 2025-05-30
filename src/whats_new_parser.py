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

    async def get_service_pack_and_configurator_version(self) -> tuple:
        """
        Extracts both the service pack and configurator versions from the "What's New" text file.

        :return: A tuple containing the service pack version and configurator version as strings.
        """

        sp_version = self._sp_version
        cfg_version = None
        contents = await self._reader.read_async(encoding="utf-16")
        if contents is None:
            log.error("Failed to read the contents of the 'What's New' file.")
            return sp_version, cfg_version

        map = self.__create_version_map(contents)
        if not map:
            log.error("No service pack or configurator version found in the contents.")
            return sp_version, cfg_version

        if self._sp_version in map:
            sp_version = self._sp_version
            cfg_version = map[self._sp_version]
        else:
            sp_version = list(map)[0]
            cfg_version = list(map.values())[0]

        return sp_version, cfg_version

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
            if "ServicePack:" in tag:
                key = f"SP{re.search(SP_VERSION_REGEX, tag).group(0)}"
            elif "Configurator:" in tag:
                value = f"CFG{re.search(CFG_VERSION_REGEX, tag).group(0)}"
            if key and value:
                map[key] = value
                key = None
                value = None
        return map
