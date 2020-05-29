"""
Script for extraction requests from Fiddler's session.
"""

import requests
import logging
from zipfile import ZipFile
import os
import json


def get_url(data: str):
    splitted_lines = data.splitlines()
    if not splitted_lines:
        logging.error('Wrong data format')
        return None
    first_line = splitted_lines[0]
    strings = first_line.split(' ')
    if len(strings) != 3:
        logging.error(f'Wrong 1st string: {first_line}')
        return None
    return strings[1]


def get_method(data: str):
    splitted_lines = data.splitlines()
    if not splitted_lines:
        logging.error('Wrong data format')
        return None

    first_line = splitted_lines[0]
    strings = first_line.split(' ')
    if len(strings) != 3:
        logging.error(f'Wrong 1st string: {first_line}')
        return None

    method_string = strings[0]

    poss_methods = ['GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE']
    if method_string in poss_methods:
        return method_string

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
        params_index = splitted_lines.index('AdditionalParams: ')
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


def get_json_body(data: str):
    splitted_lines = data.splitlines()
    try:
        empty_string_index = splitted_lines.index('')
    except ValueError as ex:
        logging.error(ex)
        return None
    for i in range(empty_string_index + 1, len(splitted_lines)):
        line = splitted_lines[i]
        if not line:
            continue
        try:
            res = json.loads(line)
            return res
        except Exception as ex:
            logging.error(ex)
            return None


def get_request(filename: str):
    with open(filename, 'r') as content_file:
        content = content_file.read()
        url = get_url(content)
        method = get_method(content)
        headers = get_headers(content)
        body = get_json_body(content)
        return url, method, headers, body


def send_request(filename: str):
    logging.debug(f'Send request from {filename}')
    url, method, headers, body = get_request(filename)
    if not url or not method:
        return
    if body:
        logging.debug(f'Send {method}-request to {url} with data')
        response = requests.request(method, url, headers=headers, data=json.dumps(body)).content
        logging.debug(response)
        return

    logging.debug(f'Send {method}-request to {url} without data')
    response = requests.request(method, url, headers=headers)
    logging.debug(response)
    return


def extract_session(filename: str) -> str:
    with ZipFile(filename, 'r') as zip_archive:
        archive_name, _ = os.path.splitext(filename)
        logging.debug(f'Unpacking session {filename} to folder {archive_name}')
        zip_archive.extractall(archive_name)
        return archive_name


def send_request_files(folder_name):
    full_folder_name = folder_name + '/raw/'
    files = [f for f in os.listdir(full_folder_name) if f.endswith('_c.txt')]
    logging.debug(files)
    for file in files:
        full_filename = full_folder_name + file
        send_request(full_filename)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    default_filename = 'FiddlerSession2.saz'
    result = extract_session(default_filename)
    logging.debug(result)
    send_request_files(result)
