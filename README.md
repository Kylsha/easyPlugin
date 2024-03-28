[![en](https://img.shields.io/badge/lang-ru-red.svg)](https://github.com/Kylsha/easyPlugin/blob/main/README.ru.md) 
# easyPlugin
QGIS plugin that allows to create plugins.

The main goal of this plugin is to make a fast and easy plugin template. With all respect to [Plugin Builder](https://github.com/g-sherman/Qgis-Plugin-Builder) module, easyPlugin is turnkey solution and makes a plugin ready for installation, testing and editing.
Plugin contains two tools: easyPlugin itself and Scripter - a tool for testing raw Python plugin code and other scripts. 

## easyPlugin tool
![Table loook](https://pereverzev.info/easyPlugin/img/img_ep.png)

### Quickstart guide
easyPlugin is a single-windowed widget that allows user to create a template of a plugin with minimum steps. The result is a folder with plugin contents and zip-file itself.  

Mandatory user inputs are: **Plugin title**, **Plugin type** and **Out folder**. Another information (author, mail tracker etc.) is not necessary but recommended to be written. 

**1. Plugin title** is the name of a plugin. It should be written with english characters only and no numbers or punctuation signs (only underscore sign allowed). This name will be used as a future name of a plugin and in some Python classes names.

**2. Plugin type** is a sample type of a plugin. It is not some classification of plugin types, just a setup for popular scenarios of plugin use.
* **Action** type will make plugin do some action just by pressing a plugin icon.
* **Widget** type is a simple widget template which can be either modified or rewritten completely. 
* **Map tool** is a simple mapping tool which makes plugin button checkable. It makes a pointer tool which puts point on map by pressing cursor on canvas. Can be deactivated by pressing plugin button one more time or selecting another map tool in QGIS.
* **Custom** type means user can take some script and make it launching from plugin button. When this type is selected, a custom Python file has to be selected as well. Note that this is a kind of dirty solution. Plugin will just execute a file, not importing user's script modules and other parts that can be reached from main plugin file. The better solution would be to edit plugin's main Python file and import script in a right way.

**3. Out folder** is a path to a folder which will be used as place where plugin data will be stored as well as zip-file.

Once **Plugin title**, **Plugin type** and **Out folder** forms are completed, user can generate plugin by clicking the appropriate button. Then there will be a question whether to install plugin or not.

Let's say a **Plugin title** is `test_plugin`, **Plugin type** is `Action` and **Out folder** is `C:\GIS\plugin_folder`. If user installed plugin and test it by pressing a plugin button, a blue notification bar will be appeared in current QGIS project. It means that everything is okay and plugin works.

### Editing plugin contents

There will be a file structure like this:

```
├── test_plugin
│   ├── __init__.py
│   ├── icon.png
│   ├── metadata.txt
│   ├── template_tools.py
│   └── test_plugin.py
└── test_plugin.zip
```

All plugin data will appear in the selected folder. According to the type of plugin some parts of code will be different for each option while the mandatory functions remain the same.
The main Python file will be named same like a plugin title written by user. 

As in example, there would be a script file called `test_plugin.py`. This file can be edited and finally replaced in zip-file in order to change a plugin. This file contains five functions in the end of it:

```
    # custom actions, feel free to edit them
    def simple_action(self):
        # run a simple action like in Python console of QGIS
        self.iface.messageBar().pushMessage("Simple", "Action", level=Qgis.Info)

    def simple_gui(self):
        # run a widget with some actions
        self.app = SimpleGui()

    def simple_map_tool(self):
        # run a map tool, also making an action button checkable
        if self.icon_action.isChecked():
            self.rband_tool_anchor = PointTool(self.icon_action)        
            iface.mapCanvas().setMapTool(self.rband_tool_anchor)
        else:
            self.rband_tool_anchor.deactivate()
            iface.mapCanvas().unsetMapTool(self.rband_tool_anchor)

    def custom_tool(self):
        try:
            pass
        except Exception as e:
            print(e)
            self.warning_message("Error in script\nSee Python console for details")

    def run(self):
        # run method that performs all the real work
        self.simple_action()
```

First four of them are "launchers" of action, widget, map or custom tool (reference to a **Plugin type** option box) and the last one (`run()`) is a selector of launcher function.
* **simple_action** will print a notification in a blue bar of QGIS (like in the example above).
* **simple_gui** runs a pyqt widget imported from file `template_tools.py` which is in the same folder as `test_plugin.py`. `SimpleGui()` widget can be found in `template_tools.py` and also modified and be replaced in zip-file of a plugin.
* **simple_map_tool** runs a map tool which also can be found in `template_tools.py`. Also if this type of plugin is selected, a plugin button becomes checkable. This is mentioned in `initGui()` function where a `self.icon_action` is defined.
* **custom_tool** is the same thing like running a script from Python editor console. It means that pressing a button will just run a file just as if it was run in Python editor of QGIS. Actually this is not a good way to go, but experienced users can rewrite a code and import their custom objects the right way.
* **run** runs one of the function above.

If there is a need to change something in plugin, this file can be edited according to function mentioned in `run()` method. In the example there is a `simple_action()` function which will make a notification in a blue QGIS bar. Let's say we want to change it and instead of notification make a print of all vector layers with number of their features in current project. 

Change in a code:
```
    # custom actions, feel free to edit them
    def simple_action(self):
        # run a simple action like in Python console of QGIS
        all_layers_count = [[l.name(), l.featureCount()] for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer]
        for layer_name, layer_count in all_layers_count:
            print('{} \t {}'.format(layer_name, layer_count))
```

That's it, code is changed and `test_plugin.py` can be put in a zip-file. Then plugin should be re-installed in order to see changes.

Another example - to do the same thing but show it in a notification window widget.
```
    # custom actions, feel free to edit them
    def simple_action(self):
        # run a simple action like in Python console of QGIS
        all_layers_count = [[l.name(), l.featureCount()] for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer]
        message = '\n'.join(['{}: {}'.format(layer_name, layer_count) for layer_name, layer_count in all_layers_count])
        QMessageBox.information(None, "Notification", message) 
```

For now a notification widget with all layers' data will appear by pressing a plugin button.

If user selects **Widget** or **Map tool** type, `run()` method will have either `simple_gui()` or `simple_map_tool()` function. Both of them reference to a `template_tools.py` file which is also imported in a main Python script (i.e., `test_plugin.py`). So if something has to be changed in provided widget sample or a map tool, user should edit the `template_tools.py` file.

The last widget type is a **Custom** and like mentioned above it just runs a Python file. This solution would work for not complex projects that use multiple imports from other files or any joins with main Python script.

Video guide provided below:

https://github.com/Kylsha/easyPlugin/assets/25682040/fc04cf6a-39c8-418e-8e39-8fef1cd613de


## Scripter tool
![Table loook](https://pereverzev.info/easyPlugin/img/img_es.png)

This tool is made for testing Python script files. User should specify a direct path to directory with Python files. Then window will show a list of Python files while you user is able to edit them in some external code editor. So when user double-click a script in Scripter, the most up-to-date version of selected script will be launched. It also helps in a team work, when you have a shared folder between users, they don't need to constantly update script/plugin, they will have the latest version of tool made by someone.

>[!NOTE]
> Scripter tool was greeted by colleagues by its simplicity. From some moment I prefer it more than plugins with repository that should be updated manually sometimes. It is more convenient in case of issue fixes: colleagues have a same local network path to scripts and tell that some script works incorrectly. I fix the script and tell that it is ready to go. Another users don't have to have update something (plugin via repository or zip-file), they just re-run script and that's it.

Scripts which are run from Scripter should have all needed libraries imported in order to work. Otherwise Scripter will tell that something is wrong with selected script and an error will be printed in Python console of QGIS. So, despite the fact that some libraries are imported in QGIS from startup, they should be re-imported in local script file. 

### Quickstart

For example there is a script which can be run from Python console:

```
from qgis.utils import iface
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(250, 100)
        self.setWindowTitle("Test widget")
        layout = QVBoxLayout(self)
        button = QPushButton("Check active layer")
        layout.addWidget(button)
        button.clicked.connect(self.get_current_layer)
        self.show()

    def get_current_layer(self):
        active_layer = iface.activeLayer()
        if active_layer:
            print(active_layer.name())
        else:
            print('no layers in project')
app = TestWidget()
```
>[!NOTE]
> Here `iface` and `PyQt5` elements are imported in order to make script run from Scripter.

This code snippet can be saved as a Python script file (for example, `my_widget.py`) and put in a folder selected as a script path in Scripter. In order to update contents of script list in Scripter widget, a blue refresh button should be pressed. Finally a double click on script will execute it. Same thing can be achieved in by selecting script in a list and pressing a ▶︎ button.

The right part of Scripter window is used to show a description of selected plugins. In order to do that, a file `descriptions.json` should be created in a folder which is selected as a script path. A content of this file should look like that:
```
{
    "test": "A sample Python code snippet.",
    "my_widget": "PyQt5 widget to show layers info"
}
```
where keys are filenames without extensions and values are script file descriptions.

Due to imports of all needed modules (like PyQt widgets and other) scripts can be used in plugin development.

Video guide provided below:

https://github.com/Kylsha/easyPlugin/assets/25682040/67390440-8ca9-4c46-9284-0677c74a3be9

