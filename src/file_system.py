import os
import shutil

from logging_wrapper import LoggingWrapper


log = LoggingWrapper().get_logger(__name__)


class FileSystem:
    """
    Class to handle file system operations.
    """

    @staticmethod
    def get_recent_directory(path) -> str:
        """
        Returns the most recent directory in the specified path.

        :param path: The path to search for directories.
        """
        if not os.path.exists(path):
            log.error(f"Path does not exist: {path}")
            return None

        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        if not dirs:
            log.error(f"No directories found in the specified path: {path}")
            return None

        return sorted(
            dirs,
            reverse=True,
            key=lambda x: os.path.getctime(os.path.join(path, x)),
        )[0]

    @staticmethod
    def get_directory(path, search) -> str:
        """
        Returns the directory that matches the search pattern.

        :param path: The path to search for directories.
        :param search: The search pattern to match against directory names.
        """
        if not os.path.exists(path):
            log.error(f"Path does not exist: {path}")
            return None

        for d in os.listdir(path):
            if os.path.isdir(os.path.join(path, d)) and search and d.endswith(search):
                return os.path.join(path, d)

        log.error(f"No directory found matching: {search}")
        return None

    @staticmethod
    def copytree(src, dst, dirs_exist_ok=False) -> str:
        """
        Copies a directory tree from source to destination.

        :param src: The source directory path.
        :param dst: The destination directory path.
        :param dirs_exist_ok: If True, allows the destination directory to exist.
        """
        try:
            ret = shutil.copytree(src, dst, dirs_exist_ok=dirs_exist_ok)
            if ret:
                log.info(f"Copied directory tree. From={src}, To={dst}")
            return ret
        except shutil.Error as e:
            log.exception(f"Failed to copy directory tree: {e}")
            raise
