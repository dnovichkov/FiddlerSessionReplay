"""
Script for extraction requests from Fiddler's session.
"""

import requests
import logging
from zipfile import ZipFile
import os


def get_method(data: str):
    poss_methods = ['GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in poss_methods:
        if method in data:
            return method
    logging.error('Cannot extract method')
    return None


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
