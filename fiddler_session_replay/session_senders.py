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
    return send_data(body, headers, method, url)


def send_data(body, headers, method, url):
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


def get_full_requests_filenames(folder_name):
    full_folder_name = folder_name + '/raw/'
    files = [full_folder_name + f for f in os.listdir(full_folder_name) if f.endswith('_c.txt')]
    logging.debug(files)
    return files


def send_request_files(folder_name):
    """
    Send files from unpacked Fiddler file
    :param folder_name:
    :return:
    """
    files = get_full_requests_filenames(folder_name)
    for file in files:
        send_request(file)
