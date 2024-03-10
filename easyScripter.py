import os
import string
import json

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import (
    QWidget,
    QDockWidget,
    QTreeView,
    QStyle,
    QFileDialog,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QAbstractItemView,
    QTextEdit,
)

script_folder = os.path.dirname(os.path.realpath(__file__))
cfg_file = os.path.join(script_folder, "cfg.json")

# default connection config
default_config = {"path": r""}


def read_cfg(data_file):
    if not os.path.isfile(data_file):
        with open(data_file, "w", encoding="utf-8") as d:
            json.dump(default_config, d, indent=4, ensure_ascii=False)
            data = default_config
    else:
        with open(data_file, "r") as fp:
            data = json.load(fp)

    path = data["path"]
    descriptions_path = os.path.join(path, "descriptions.json")
    if os.path.isfile(descriptions_path):
        with open(descriptions_path, "r") as fp:
            data_desc = json.load(fp)
    else:
        data_desc = {}

    return path, data_desc


class Scripter(QDockWidget):
    closingPlugin = pyqtSignal()

    def __init__(self, wrapper):
        QDockWidget.__init__(self)
        self.wrapper = wrapper
        self.setWindowTitle("Scripter")
        self.ispnippets = Scripter_widget(self)
        self.setWidget(self.ispnippets)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()


class Scripter_widget(QWidget):
    # Main widget tab tool

    def __init__(self, parent):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.wpath, self.descriptions = read_cfg(cfg_file)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.upd_table = QPushButton()
        self.upd_table.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.upd_table.setToolTip("Update script list")
        self.upd_table.setMaximumWidth(35)

        self.path_line = QLineEdit()
        self.path_line.setPlaceholderText("Path to scripts...")
        self.path_line.setText(self.wpath)

        self.settings = QPushButton()
        self.settings.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.settings.setToolTip("Path to scripts")
        self.settings.setMaximumWidth(35)

        self.dataView = QTreeView()
        self.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataView.setRootIsDecorated(False)
        self.dataView.doubleClicked.connect(self.on_double_click)

        self.model = QStandardItemModel(0, 1, self.dataView)
        self.model.setColumnCount(1)
        self.model.setHeaderData(0, Qt.Horizontal, "Script")

        self.description_area = QTextEdit()
        self.description_area.setReadOnly(True)

        self.dataView.setModel(self.model)

        self.btn_run = QPushButton()
        self.btn_run.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        h_layout = QVBoxLayout(self)
        buttons_layout = QHBoxLayout(self)
        content_layout = QHBoxLayout(self)

        h_layout.addLayout(buttons_layout)
        h_layout.addLayout(content_layout)

        buttons_layout.addWidget(self.upd_table, 1)
        buttons_layout.addWidget(self.path_line, 1)
        buttons_layout.addWidget(self.settings, 1)
        buttons_layout.addStretch()

        content_layout.addWidget(self.dataView, 1)
        content_layout.addWidget(self.description_area, 1)
        self.description_area.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        h_layout.addWidget(self.btn_run)

        self.upd_table.clicked.connect(lambda: self.get_actions(self.model))
        self.btn_run.clicked.connect(self.run_action)
        self.settings.clicked.connect(self.load_folder)
        self.dataView.clicked.connect(self.get_description)
        self.get_actions(self.model)

    def on_double_click(self, index):
        self.run_action()

    def get_description(self):
        selected_data = self.dataView.selectedIndexes()
        script_name = selected_data[0].data()
        self.description_area.setHtml(
            "<b>{}</b>".format(self.descriptions.get(script_name, ""))
        )

    def load_folder(self):
        result = QFileDialog.getExistingDirectoryUrl(self, "Select scripts folder")
        if result:
            selected_path = result.path().strip(string.punctuation)
            if selected_path:
                self.wpath = selected_path
            else:
                return

            with open(cfg_file, "w", encoding="utf-8") as d:
                json.dump({"path": self.wpath}, d, indent=4, ensure_ascii=False)
            self.path_line.setText(self.wpath)
            self.get_actions(self.model)
            self.description_area.setHtml("<b></b>")

    def get_actions(self, model):
        current_path = self.path_line.text()
        if not current_path:
            return
        if not os.path.isdir(current_path):
            self.warning_message("Wrong path")
            return
        self.wpath = current_path
        model.setRowCount(0)
        for afile in os.listdir(self.wpath):
            if os.path.isfile(os.path.join(self.wpath, afile)):
                if "." not in afile:
                    continue
                action_name, action_type = os.path.splitext(afile)
                if action_type == ".py":
                    model.insertRow(0)
                    model.setData(model.index(0, 0), action_name)
        self.description_area.setHtml("<b></b>")
        print("-->", current_path)
        file_descriptions = os.path.join(current_path, "descriptions.json")
        if os.path.isfile(file_descriptions):
            with open(file_descriptions, "r") as fp:
                self.descriptions = json.load(fp)
        else:
            self.descriptions = {}

        with open(cfg_file, "w", encoding="utf-8") as d:
            json.dump({"path": self.wpath}, d, indent=4, ensure_ascii=False)

    def run_action(self):
        selected_data = self.dataView.selectedIndexes()
        if selected_data:
            script_name = selected_data[0].data()
            self.run_script(script_name)
        else:
            self.warning_message("Select script then press ▶︎ button")

    def run_script(self, script):
        script_path = os.path.join(self.wpath, "{}.py".format(script))
        try:
            self.result = exec(
                open("{}".format(script_path).encode("utf-8")).read(),
                {"wrapper": self, "project_folder": self.wpath, "script_name": script},
            )
        except Exception as e:
            print(e)
            self.warning_message("Error in script\nSee Python console for details")

    def warning_message(self, err_text):
        msg = QMessageBox()
        msg.warning(self, "Warning", err_text)
