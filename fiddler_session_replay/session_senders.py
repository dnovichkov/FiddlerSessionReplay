import json
import logging
import os

import requests

from fiddler_session_replay.data_extracters import get_request


def send_request(filename: str):
    """
    Send request from file
    :param filename:
    :return:
    """
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


def send_request_files(folder_name):
    """
    Send files from unpacked Fiddler file
    :param folder_name:
    :return:
    """
    full_folder_name = folder_name + '/raw/'
    files = [f for f in os.listdir(full_folder_name) if f.endswith('_c.txt')]
    logging.debug(files)
    for file in files:
        full_filename = full_folder_name + file
        send_request(full_filename)
