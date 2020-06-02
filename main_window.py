import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem

from fiddler_session_replay.data_extracters import get_request
from fiddler_session_replay.session_extracters import extract_session
from fiddler_session_replay.session_senders import get_full_requests_filenames, send_data
from session_replay import Ui_MainWindow
from threading_utils import Worker


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.settings.triggered.connect(self.show_settings_dialog)
        self.ui.exit.triggered.connect(QtWidgets.QApplication.quit)
        self.ui.about.triggered.connect(self.show_about_dialog)

        self.ui.requests_table_widget.setColumnCount(2)
        self.ui.requests_table_widget.setHorizontalHeaderLabels(["Method", "URL"])
        self.ui.requests_table_widget.resizeColumnsToContents()
        header = self.ui.requests_table_widget.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.ui.load_source_button.clicked.connect(self.load_source_file)
        self.ui.load_file_action.triggered.connect(self.load_source_file)
        self.ui.run_button.clicked.connect(self.run_playing)
        self.requests = None
        self.thread_pool = QThreadPool()

    def progress_fn(self, n):
        self.ui.requests_table_widget.item(n, 0).setBackground(QtGui.QColor(125, 125, 125))
        self.ui.requests_table_widget.item(n, 1).setBackground(QtGui.QColor(125, 125, 125))

        self.statusBar().showMessage(f'Send {self.requests[n][0]}-request to {self.requests[n][1]}')

    def execute_this_fn(self, progress_callback):
        if not self.requests:
            return
        try:
            for i, request_data in enumerate(self.requests):
                url, method, headers, body = request_data
                if not method or not url:
                    continue
                logging.debug(url)

                send_data(body, headers, method, url)
                progress_callback.emit(i)
        except Exception as ex:
            logging.error(ex)
            self.statusBar().showMessage(str(ex))

    def print_output(self, s):
        pass

    def thread_complete(self):
        self.statusBar().showMessage(f'Session was stopped')

    def run_playing(self):
        if not self.requests:
            logging.error('File is not loaded')
            return

        self.statusBar().showMessage(f'Session was started')

        worker = Worker(self.execute_this_fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        self.thread_pool.start(worker)
        return

    def load_source_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Choose session file", "",
                                                  "Fiddler Session Files (*.saz);;All Files (*)", options=options)
        if not filename:
            return
        logging.debug(f'Choosed file {filename}')

        foldername = extract_session(filename)
        logging.debug(f'Session was extracted to {foldername}')
        self.statusBar().showMessage(f'Session was extracted to {foldername}')

        filenames = get_full_requests_filenames(foldername)
        self.requests = [get_request(filename) for filename in filenames]
        self.requests = [req for req in self.requests if req[0] and req[1]]
        self.ui.requests_table_widget.setRowCount(len(self.requests))
        for i, request_data in enumerate(self.requests):
            url, method, _, _ = request_data
            if not method or not url:
                continue
            logging.debug(url)
            self.ui.requests_table_widget.setItem(i, 0, QTableWidgetItem(method))
            self.ui.requests_table_widget.setItem(i, 1, QTableWidgetItem(url))

        self.ui.run_button.setDisabled(False)

    def show_settings_dialog(self):
        text = 'There are no settings now'
        QMessageBox.about(self, "Settings", text)

    def show_about_dialog(self):
        text = 'Simplest replaying for Fiddler session'
        QMessageBox.about(self, "About", text)
