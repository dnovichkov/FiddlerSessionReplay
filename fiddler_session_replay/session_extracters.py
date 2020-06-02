import logging
import os
from zipfile import ZipFile


def extract_session(filename: str) -> str:
    """
    Unpack Fiddler-file to folder
    :param filename:
    :return:
    """
    with ZipFile(filename, 'r') as zip_archive:
        archive_name, _ = os.path.splitext(filename)
        logging.debug(f'Unpacking session {filename} to folder {archive_name}')
        zip_archive.extractall(archive_name)
        return archive_name
