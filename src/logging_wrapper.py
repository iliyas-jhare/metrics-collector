import logging


class LoggingWrapper:
    """
    A wrapper class for logging functionality.
    This class provides methods to get a logger with a specified name and level.
    """

    def get_stream_handler(self, level=logging.INFO) -> logging.StreamHandler:
        """
        Returns a stream handler with the specified logging level.

        :param level: The logging level for the stream handler (default is logging.INFO).
        :return: A stream handler instance.
        """

        format = "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"
        formatter = logging.Formatter(format)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return handler

    def get_logger(self, name: str, level=logging.INFO) -> logging.Logger:
        """
        Returns a logger with the specified name.

        :param name: The name of the logger.
        :param level: The logging level for the logger (default is logging.INFO).
        :return: A logger instance.
        """

        stream_handler = self.get_stream_handler(level)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(stream_handler)
        return logger
