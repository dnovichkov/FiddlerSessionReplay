"""
Script for extraction requests from Fiddler's session.
"""

import logging
from zipfile import ZipFile
import os


def extract_session(filename: str) -> str:
    with ZipFile(filename, 'r') as zip_archive:
        archive_name, _ = os.path.splitext(filename)
        logging.debug(f'Unpacking session {filename} to folder {archive_name}')
        zip_archive.extractall(archive_name)
        return archive_name


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    default_filename = 'FiddlerSession2.saz'
    result = extract_session(default_filename)
    logging.debug(result)
