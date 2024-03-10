from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * # only used widgets can be listed here

from qgis.core import *
from qgis._gui import * 
from qgis.utils import iface

# variables
screen = QApplication.primaryScreen()
size = screen.size()
w, h = size.width(), size.height() # used in placing widget
txt_selection = "Selected layer: {}\nSelected field: {}\nSelected values: {}"
txt_no_selection = "No selection in layer {}"

class PointTool(QgsMapToolEmitPoint):
    # point map tool
    # used as an example for easyPlugin
    def __init__(self, icon_action):
        self.canvas = iface.mapCanvas()
        self.icon_action = icon_action
        # hover circle 
        self.rubberBandPointRound = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rubberBandPointRound.setColor(QColor(55,50,100,50))
        self.rubberBandPointRound.setStrokeColor(QColor('red'))
        self.rubberBandPointRound.setWidth(35)
        self.rubberBandPointRound.reset()
    
        # click point
        self.rubberBandPoint = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rubberBandPoint.setColor(QColor(150,150,200,255))
        self.rubberBandPoint.setWidth(15)
        self.rubberBandPoint.reset()
        self.anchor_point = None
        self.anchor_point_geom = None
        
        # initialize tool
        QgsMapToolEmitPoint.__init__(self, self.canvas)    
        return

    def canvasMoveEvent(self, e):
        # listening to mouse move
        self.anchor_point = self.toMapCoordinates(e.pos())
        self.anchor_point_geom = QgsGeometry().fromPointXY(self.anchor_point)
        self.rubberBandPointRound.reset()
        self.rubberBandPointRound.setToGeometry(self.anchor_point_geom)
        return

    def canvasPressEvent(self, e):
        # listening to mouse click
        self.rubberBandPoint.reset()
        self.rubberBandPoint.setToGeometry(self.anchor_point_geom)
        return

    def deactivate(self):
        # deactivating tool
        self.rubberBandPoint.reset()
        self.rubberBandPointRound.reset()
        QgsMapTool.deactivate(self)
        self.deactivated.emit()
        self.icon_action.setChecked(False)
        return

class SimpleGui(QWidget):
    # simple gui widget which check selected values and brings it into
    # notification
    # used as an example for easyPlugin
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(int(w / 2 - 200), int(h / 2) - 50, 400, 100)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setWindowTitle("Simple GUI")

        # variables
        self.current_layer = None
        self.fields_data = []
        self.values_data = []
        all_layers = list(
            list(
                filter(
                    lambda x: x.type() == QgsVectorLayer.VectorLayer
                    and x.featureCount()
                    and x.isValid(),
                    QgsProject.instance().mapLayers().values(),
                )
            )
        )
        self.layers_dict = {l.name(): l for l in all_layers}

        # widgets
        self.combo_layers = QComboBox()
        self.combo_fields = QComboBox()
        self.check_value = QPushButton("Check value")
        self.combo_layers.addItems(list(self.layers_dict.keys()))

        # gui setup
        self.setLayout(self.grid)
        self.grid.addWidget(self.combo_layers, 1, 1, 1, 2)
        self.grid.addWidget(self.combo_fields, 1, 3, 1, 3)
        self.grid.addWidget(self.check_value, 2, 1, 1, 5)

        # actions
        self.combo_layers.currentIndexChanged.connect(self.update_fields)
        self.check_value.clicked.connect(self.check_selected_values)
        self.update_fields()
        self.show()

    def update_fields(self):
        # get current layer and fields
        if self.layers_dict:
            selected_text = self.combo_layers.currentText()
            self.current_layer = self.layers_dict[selected_text]
            self.combo_fields.clear()
            self.combo_fields.addItems(self.current_layer.fields().names())

    def check_selected_values(self):
        # get selected features and its values from selected fields
        if self.current_layer:
            selection = list(self.current_layer.getSelectedFeatures())
            if selection:
                current_field = self.combo_fields.currentText()
                unique_values = sorted(set([f[current_field] for f in selection]))
                message_text = txt_selection.format(
                    self.current_layer.name(),
                    current_field,
                    ", ".join([str(w) for w in unique_values]),
                )
                self.warning_message(message_text)
            else:
                self.warning_message(txt_no_selection.format(self.current_layer.name()))
        else:
            self.warning_message("No vector layers in current project")

    def warning_message(self, text):
        mbox = QMessageBox()
        mbox.warning(self, "Notification", text)
