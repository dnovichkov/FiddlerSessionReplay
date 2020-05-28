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


def get_headers(data: str) -> dict:
    """
    Exctract headers from data, which are located in 'AdditionalParams'.
    :param data:
    :return:
    """
    splitted_lines = data.splitlines()
    result = {}
    try:
        params_index = splitted_lines.index('AdditionalParams:')
        # Empty string means, that request's body is located after this string.
        empty_string_index = splitted_lines.index('', params_index)
    except ValueError as ex:
        logging.error(ex)
        return {}
    for i in range(params_index + 1, empty_string_index):
        line = splitted_lines[i]
        try:
            splitter_index = line.index(':')
            param = line[:splitter_index]
            # Data format is 'Param_name: param_value', we return it as dict: {'param_name': 'param_value'}.
            value = line[splitter_index + 2:]
            result[param] = value
        except ValueError as ex:
            logging.error(ex)

    return result


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
