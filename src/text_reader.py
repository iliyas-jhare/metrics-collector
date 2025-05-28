import logging_wrapper

log = logging_wrapper.LoggingWrapper().get_logger(__name__)


class TextReader:
    """
    A simple text file reader class that provides methods to read the entire content
    of a text file or read it line by line.
    """

    def __init__(self, path):
        """
        Initializes the TextReader with the specified file path.
        :param path: The path to the text file to be read.
        """

        self._path = path

    def read(self, encoding="utf-8"):
        """
        Reads the entire content of the text file.
        :return: The content of the text file as a string.
        """
        try:
            with open(self._path, "r", encoding=encoding) as file:
                return file.read()
        except Exception as e:
            log.exception(e)
            return ""

    def read_lines(self, encoding="utf-8"):
        """
        Reads the text file line by line.
        :return: A list of lines from the text file.
        """
        try:
            with open(self._path, "r", encoding=encoding) as file:
                return file.readlines()
        except Exception as e:
            log.exception(e)
            return []
