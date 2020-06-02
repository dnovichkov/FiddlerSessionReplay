import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from session_replay import Ui_MainWindow

from fiddler_session_replay.session_extracters import extract_session
from fiddler_session_replay.session_senders import send_request_files


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.settings.triggered.connect(self.show_settings_dialog)
        self.ui.exit.triggered.connect(QtWidgets.QApplication.quit)
        self.ui.about.triggered.connect(self.show_about_dialog)

        self.ui.load_source_button.clicked.connect(self.load_source_file)
        self.ui.load_file_action.triggered.connect(self.load_source_file)
        self.ui.run_button.clicked.connect(self.run_planning)
        self.filename = None

    def run_planning(self):
        if not self.filename:
            logging.error('File is not loaded')
            return

        foldername = extract_session(self.filename)
        logging.debug(f'Session was extracted to {foldername}')

        logging.info('Session was started')
        self.statusBar().showMessage(f'Session is playing')

        send_request_files(foldername)

        self.statusBar().showMessage(f'Session was stopped')

    def load_source_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Choose session file", "",
                                                  "Fiddler Session Files (*.saz);;All Files (*)", options=options)
        if not filename:
            return
        logging.debug(f'Choosed file {filename}')
        self.filename = filename

        self.ui.run_button.setDisabled(False)

        self.statusBar().showMessage(f'Loaded file {filename}')

    def show_settings_dialog(self):
        text = 'There are no settings now'
        QMessageBox.about(self, "Settings", text)

    def show_about_dialog(self):
        text = 'Simplest replaying for Fiddler session'
        QMessageBox.about(self, "About", text)
