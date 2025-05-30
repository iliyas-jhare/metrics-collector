from anyio import open_file

from logging_wrapper import LoggingWrapper


log = LoggingWrapper().get_logger(__name__)


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

    async def read_async(self, encoding="utf-8") -> str:
        """
        Reads the entire content of the text file.
        :return: The content of the text file as a string.
        """
        try:
            async with await open_file(self._path, "r", encoding=encoding) as file:
                return await file.read()
        except Exception as e:
            log.exception(e)
            return None
