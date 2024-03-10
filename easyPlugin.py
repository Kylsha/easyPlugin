# -*- coding: utf-8 -*-
"""
/***************************************************************************
Plugin which creates a simple QGIS plugin templates ready for install, editing and testing
                              -------------------
        released             : 2024-02-28
        author               : (C) 2024 by Pavel Pereverzev
        email                : pavelpereverzev93@gmail.com
        made in              : easyPlugin by Pavel Pereverzev
        credits to           : Gary Sherman and Alexandre Neto
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# import system, PyQt and QGIS libraries
from __future__ import absolute_import
import os
from datetime import datetime
import shutil
import zipfile

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *  

from qgis.core import *
from qgis._gui import *
from qgis.utils import iface

import pyplugin_installer
from .easyScripter import *


# variables
# plugin name validator
rx = QRegExp("[A-Za-z_ ]*")
validator = QRegExpValidator(rx)
script_folder = os.path.dirname(os.path.realpath(__file__))

# links to original data
file_mdata = os.path.join(script_folder, "template_data", "metadata.txt")
file_init = os.path.join(script_folder, "template_data", "__init__.txt")
file_action = os.path.join(script_folder, "template_data", "template.txt")
file_tools = os.path.join(script_folder, "template_data", "template_tools.txt")
file_icon = os.path.join(script_folder, "template_data", "icon.png")

ptypes = {
    "Action": ["self.simple_action()", False, "icon_script.png"],
    "Widget": ["self.simple_gui()", False, "icon_widget.png"],
    "Map tool": ["self.simple_map_tool()", True, "icon_maptool.png"],
    "Custom": ["self.custom_tool()", False, "icon_custom.png"],
}

# current date/year
curr_day = datetime.strftime(datetime.now(), "%Y-%m-%d")
curr_year = datetime.now().year


def prepare_data(
    folder_out,
    plugin_name,
    plugin_classname,
    plugin_type,
    plugin_custom_file,
    plugin_desc,
    plugin_author,
    plugin_mail,
    plugin_site,
    icon_path,
):
    global file_icon
    # creating out paths
    folder_out_sub = os.path.join(folder_out, plugin_classname)
    if not os.path.isdir(folder_out_sub):
        os.mkdir(folder_out_sub)
    file_new_mdata = os.path.join(folder_out_sub, r"metadata.txt")
    file_new_init = os.path.join(folder_out_sub, r"__init__.py")
    file_new_action = os.path.join(folder_out_sub, r"{}.py".format(plugin_classname))
    file_new_tools = os.path.join(folder_out_sub, r"template_tools.py")
    file_new_icon = os.path.join(folder_out_sub, r"icon.png")
    file_new_custom = os.path.join(
        os.path.dirname(script_folder),
        plugin_name,
        os.path.basename(plugin_custom_file),
    )
    file_new_custom_local = os.path.join(
        folder_out_sub, os.path.basename(plugin_custom_file)
    )

    cmd_custom = (
        "pass"
        if not plugin_custom_file
        else """self.result = exec(open(r'{}'.encode('utf-8')).read(), {{"wrapper": self}})""".format(
            file_new_custom
        )
    )

    # 1. metadata
    with open(file_mdata, "r", encoding="utf-8") as mdata_obj:
        mdata = mdata_obj.read()
    mdata_edited = mdata.format(
        plugin_name,
        plugin_desc,
        "",  # plugin_about,
        plugin_author,
        plugin_mail,
        plugin_site,
    )
    with open(file_new_mdata, "w", encoding="utf-8") as mdata_obj:
        mdata_obj.write(mdata_edited)

    # 2. init
    with open(file_init, "r", encoding="utf-8") as mdata_obj:
        idata = mdata_obj.read()
    idata_edited = idata.format(
        plugin_name,
        plugin_desc,
        curr_day,
        curr_year,
        plugin_author,
        plugin_mail,
        plugin_classname,
    )
    with open(file_new_init, "w", encoding="utf-8") as mdata_obj:
        mdata_obj.write(idata_edited)

    # 3. class
    with open(file_action, "r", encoding="utf-8") as mdata_obj:
        py_data = mdata_obj.read()
    py_data_edited = py_data.format(
        plugin_desc,
        curr_day,
        curr_year,
        plugin_author,
        plugin_mail,
        plugin_classname,
        plugin_name,
        ptypes[plugin_type][0],
        ptypes[plugin_type][1],
        cmd_custom,
    )
    with open(file_new_action, "w", encoding="utf-8") as mdata_obj:
        mdata_obj.write(py_data_edited)

    # 4. icon
    if icon_path:
        file_icon = icon_path
    else:
        file_icon = os.path.join(script_folder, "icons", ptypes[plugin_type][2])
    shutil.copyfile(file_icon, file_new_icon)

    # 5. tools
    shutil.copyfile(file_tools, file_new_tools)

    # 6 custom tool
    if plugin_custom_file:
        shutil.copyfile(plugin_custom_file, file_new_custom_local)

    # 7. making a zip
    out_file = os.path.join(
        os.path.dirname(folder_out_sub), "{}.zip".format(plugin_name)
    )

    zf = zipfile.ZipFile(out_file, "w")
    for filename in os.listdir(folder_out_sub):
        full_file_path = os.path.join(folder_out_sub, filename)
        fl = os.path.basename(os.path.dirname(full_file_path))
        new_path = os.path.join(fl, filename)
        zf.write(full_file_path, arcname=new_path)
    zf.close()
    return out_file


def remove_docked_widgets():
    for ch in iface.mainWindow().children():
        if "om_mod" in ch.objectName():
            ch.close()
            ch = None


class easyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("easyPlugin by Pavel Pereverzev")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(700, 500, 400, 100)

        # attrs
        self.save_path = None
        self.icon_path = None
        self.plugin_name = None
        self.plugin_desc = None
        self.plugin_about = None
        self.plugin_author = None
        self.plugin_mail = None
        self.class_file = None
        self.class_name = None

        # layout
        groupbox_about = QGroupBox("Main parameters")
        groupbox_misc = QGroupBox("Misc.")
        vbox = QVBoxLayout(self)
        grid_about = QGridLayout()
        grid_about.setSpacing(10)
        grid_misc = QGridLayout()
        grid_misc.setSpacing(10)

        self.l_pname = QLabel("Plugin title")
        self.line_pname = QLineEdit(self)
        # self.line_pname.setValidator(validator)

        self.l_type = QLabel("Plugin type")
        self.plugin_type = QComboBox()
        self.plugin_type.addItems(["Action", "Widget", "Map tool", "Custom"])

        self.l_custom = QLabel("Custom file")
        self.line_custom = QLineEdit()
        self.line_custom.setReadOnly(True)
        self.btn_custom = QPushButton(self)
        self.btn_custom.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.line_custom.setDisabled(True)
        self.btn_custom.setDisabled(True)

        self.l_desc = QLabel("Plugin\ndescription")
        self.line_desc = QLineEdit(self)

        # self.l_about = QLabel('About')
        # self.line_about = QLineEdit(self)

        self.l_author = QLabel("Author")
        self.line_author = QLineEdit(self)

        self.l_mail = QLabel("E-mail")
        self.line_mail = QLineEdit(self)

        self.l_site = QLabel("Site/GitHub")
        self.line_site = QLineEdit(self)

        self.l_folder = QLabel("Out folder")
        self.line_folder = QLineEdit(self)
        self.line_folder.setReadOnly(True)
        self.btn_folder = QPushButton(self)
        self.btn_folder.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.btn_folder.setMaximumWidth(30)

        self.l_icon = QLabel("Icon")
        self.line_icon = QLineEdit(self)
        self.line_icon.setReadOnly(True)
        self.btn_icon = QPushButton(self)
        self.btn_icon.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.btn_icon.setMaximumWidth(30)

        self.btn_generate = QPushButton("Generate plugin")
        self.btn_generate.setMinimumHeight(32)

        # gui setup
        grid_about.addWidget(self.l_pname, 0, 1, 1, 1)
        grid_about.addWidget(self.line_pname, 0, 2, 1, 4)

        grid_about.addWidget(self.l_type, 1, 1, 1, 1)
        grid_about.addWidget(self.plugin_type, 1, 2, 1, 4)

        grid_about.addWidget(self.l_custom, 2, 1, 1, 1)
        grid_about.addWidget(self.line_custom, 2, 2, 1, 3)
        grid_about.addWidget(self.btn_custom, 2, 5, 1, 1)

        grid_about.addWidget(self.l_desc, 3, 1, 1, 1)
        grid_about.addWidget(self.line_desc, 3, 2, 1, 4)

        grid_about.addWidget(self.l_author, 4, 1, 1, 1)
        grid_about.addWidget(self.line_author, 4, 2, 1, 4)

        grid_about.addWidget(self.l_mail, 5, 1, 1, 1)
        grid_about.addWidget(self.line_mail, 5, 2, 1, 4)

        grid_about.addWidget(self.l_site, 6, 1, 1, 1)
        grid_about.addWidget(self.line_site, 6, 2, 1, 4)

        grid_about.addWidget(self.l_folder, 7, 1, 1, 1)
        grid_about.addWidget(self.line_folder, 7, 2, 1, 3)
        grid_about.addWidget(self.btn_folder, 7, 5, 1, 1)

        grid_misc.addWidget(self.l_icon, 0, 1, 1, 1)
        grid_misc.addWidget(self.line_icon, 0, 2, 1, 3)
        grid_misc.addWidget(self.btn_icon, 0, 5, 1, 1)
        grid_about.setColumnStretch(2, 3)
        grid_misc.setColumnStretch(2, 3)

        groupbox_about.setLayout(grid_about)
        groupbox_misc.setLayout(grid_misc)

        vbox.addWidget(groupbox_about)
        vbox.addWidget(groupbox_misc)
        vbox.addWidget(self.btn_generate)
        self.setLayout(vbox)

        self.plugin_type.currentTextChanged.connect(self.check_plugin_type)
        self.btn_custom.clicked.connect(self.select_custom_file)
        self.btn_folder.clicked.connect(self.select_folder)
        self.btn_generate.clicked.connect(self.generate_plugin)
        self.line_pname.textChanged.connect(self.check_text)
        self.btn_icon.clicked.connect(self.select_icon)

        self.show()

    def check_plugin_type(self):
        ptype = self.plugin_type.currentText()
        if ptype == "Custom":
            self.line_custom.setDisabled(False)
            self.btn_custom.setDisabled(False)
        else:
            self.line_custom.setDisabled(True)
            self.btn_custom.setDisabled(True)
        return

    def select_custom_file(self):
        # select icon for a plugin
        result_file = QFileDialog.getOpenFileName(
            self, "Select python script file", None, "Python files (*.py)"
        )[0]
        if result_file:
            self.line_custom.setText(result_file)

    def select_icon(self):
        # select icon for a plugin
        result_file = QFileDialog.getOpenFileName(
            self, "Select icon picture", None, "Images (*.png)"
        )[0]
        if result_file:
            self.line_icon.setText(result_file)
            self.icon_path = result_file

    def check_text(self):
        # validate input plugin name
        global_pos = self.line_pname.mapToGlobal(self.line_pname.rect().topRight())
        curr_v = self.line_pname.text()
        v = validator.validate(curr_v, 0)[0]
        if v != QValidator.Acceptable:
            QToolTip.showText(
                global_pos,
                "Only english characters\nand _ symbol are allowed",
                self.line_pname,
            )
            self.line_pname.setStyleSheet("QLineEdit {background: #ffc8c8;}")
            pass
        else:
            self.line_pname.setStyleSheet("")
            pass

    def warning_message(self, err_text):
        # custom warning message
        msg = QMessageBox()
        msg.warning(self, "Warning", err_text)
        return

    def question_message(self, question_text):
        final_question = QMessageBox(self)
        answer = final_question.question(
            self, "easyPlugin", question_text, final_question.Yes | final_question.No
        )
        return answer

    def select_folder(self):
        # path to save plugin
        result = QFileDialog.getExistingDirectory(None, "Select folder to save plugin")
        self.save_path = result
        self.line_folder.setText(self.save_path)
        return

    def generate_plugin(self):
        # get all inputs and generate pl
        self.plugin_name = self.line_pname.text()
        self.class_name = self.plugin_name.replace(" ", "_")
        self.ptype = self.plugin_type.currentText()
        self.custom_file = self.line_custom.text()
        self.plugin_desc = self.line_desc.text()
        # self.plugin_about = self.line_about.text()
        self.plugin_author = self.line_author.text()
        self.plugin_mail = self.line_mail.text()
        self.plugin_site = self.line_site.text()
        v = validator.validate(self.line_pname.text(), 0)[0] == QValidator.Acceptable
        if all([v, self.save_path]):
            plugin_file = prepare_data(
                self.save_path,
                self.plugin_name,
                self.class_name,
                self.ptype,
                self.custom_file,
                self.plugin_desc,
                self.plugin_author,
                self.plugin_mail,
                self.plugin_site,
                self.icon_path,
            )

            user_answer = self.question_message(
                "Plugin {} is good to go.\nInstall it now?".format(self.plugin_name)
            )
            if user_answer == QMessageBox.Yes:
                pyplugin_installer.instance().installFromZipFile(plugin_file)
                self.warning_message("Plugin installed!")
            else:
                pass
        else:
            self.warning_message("Plugin title and Out folder should be specified")


class easyPlugin(object):
    # main plugin class
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "easyPlugin_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("easyPlugin")

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    def initGui(self):
        # Create the menu entries and toolbar icons inside the QGIS GUI
        icon_path = QIcon(os.path.join(self.plugin_dir, "icon.png"))
        icon_path_scripter = QIcon(os.path.join(self.plugin_dir, "icon_scripter.png"))
        self.icon_action = self.add_action(
            icon_path,
            text=self.tr("easyPlugin"),
            callback=self.run,
            checkable=False,
            parent=self.iface.mainWindow(),
        )
        self.icon_action_scripter = self.add_action(
            icon_path_scripter,
            text=self.tr("easyScripter"),
            callback=self.runScripter,
            checkable=True,
            parent=self.iface.mainWindow(),
        )
        self.scripterIsActive = False
        self.dockwidget = None

        # will be set False in run()
        self.first_start = True

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        checkable=False,
        add_to_menu=False,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        action.setCheckable(checkable)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def unload(self):
        # Removes the plugin menu item and icon from QGIS GUI
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

    def tr(self, text):
        return QCoreApplication.translate("easyPlugin", text)

    # MAIN ACTION FUNCTION IS HERE
    def run(self):
        # run method that performs all the real work
        self.app = easyWidget()

    def runScripter(self):
        if not self.scripterIsActive:
            self.scripterIsActive = True

            if self.dockwidget == None:
                self.dockwidget = Scripter(None)

            self.dockwidget.closingPlugin.connect(self.onClosePlugin)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
        else:
            self.dockwidget.close()

    def onClosePlugin(self):
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)
        self.dockwidget = None
        self.scripterIsActive = False
        self.icon_action_scripter.setChecked(False)
