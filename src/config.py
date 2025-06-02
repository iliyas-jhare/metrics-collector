import json

from logging_wrapper import LoggingWrapper
from text_reader import TextReader

log = LoggingWrapper().get_logger(__name__)


class Dict(dict):
    """Make dictionary items accessible using dot notation"""

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config(object):
    """
    A class to handle configuration data, allowing for loading from dictionaries, lists, or JSON files.
    This class provides methods to load data and access it using dot notation.
    """

    @staticmethod
    def load_data(data):
        """
        Loads data from a dictionary or list and returns a Config object or a Dict object.
        :param data: A dictionary or list of data items to be loaded.
        :return: A Config object or a Dict object containing the data.
        """

        if type(data) is dict:
            return Config.load_dict(data)
        elif type(data) is list:
            return Config.load_list(data)
        else:
            return data

    @staticmethod
    def load_dict(data):
        """
        Loads a dictionary of data and returns a Dict object with dot notation access.

        :param data: A dictionary of data items to be loaded.
        :return: A Dict object containing the data, allowing dot notation access.
        """

        ret = Dict()
        for key, value in data.items():
            ret[key] = Config.load_data(value)
        return ret

    @staticmethod
    def load_list(data):
        """
        Loads a list of data and returns a list of Config objects.

        :param data: A list of data items to be loaded.
        :return: A list of Config objects.
        """

        ret = [Config.load_data(item) for item in data]
        return ret

    @staticmethod
    async def load_json(path):
        """
        Loads a JSON file from the specified path and returns a Config object.

        :param path: The path to the JSON file.
        :return: A Config object containing the data from the JSON file, or None if an error occurs.
        """
        try:
            reader = TextReader(path)
            contents = await reader.read_async()
            data = json.loads(contents)
            return Config.load_data(data)
        except Exception as e:
            log.exception(e)
            return None

    @staticmethod
    def get_svn_file_properties(config: dict) -> dict:
        """
        Returns a dictionary of SVN file properties from the given configuration.
        :param config: A dictionary containing SVN file properties.
        :return: A dictionary of SVN file properties with keys as property names and values as property values.
        """
        props = {}
        for d in config.SvnFileProperties:
            key = d["name"]
            value = d["value"]
            props[key] = value
        return props
