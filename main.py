"""
Script for extraction requests from Fiddler's session.
"""

import logging
import sys
from PyQt5 import QtWidgets

from main_window import MainWindow


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # default_filename = 'FiddlerSession2.saz'
    # result = extract_session(default_filename)
    # logging.debug(result)
    # send_request_files(result)

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()

    app.exec_()
