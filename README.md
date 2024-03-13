# easyPlugin
QGIS plugin that allows to create plugins.

~ draft guide ~

The main goal of this plugin is to make a fast and easy plugin template. With all respect to [Plugin Builder](https://github.com/g-sherman/Qgis-Plugin-Builder) module, easyPlugin is turnkey solution and makes a plugin ready for installation, testing and editing.
Plugin contains two tools: easyPlugin itself and Scripter - a tool for testing raw python plugin code and other scripts. 

## easyPlugin tool
![Table loook](https://pereverzev.info/easyPlugin/img/img_ep.png)

easyPlugin is a single-windowed widget where user should type at least **Plugin name** and point the **Out folder**. Another information is not mandatory but may be mentioned. Also user can select a plugin type. There are four of them.
* **Action** type will make plugin do some action just by pressing a plugin icon.
* **Widget** type is a simple widget template which can be either modified or rewritten completely. 
* **Map tool** is a simple mapping tool which makes plugin button checkable. It makes a pointer tool which puts point on map by pressing cursor on canvas. Can be deactivated by pressing plugin button one more time or selecting another map tool in QGIS.
* **Custom** type means user can take some script and make it launching from plugin button. Note that this is a kind of dirty solution. Plugin will just execute a file, not importing user's script modules and other parts that can be reached from main plugin file. The better solution would be to edit plugin's main python file and import script in a right way.

Once **Plugin name** and **Out folder** fields are filled, user can generate plugin by clicking the appropriate button. Then there will be a question whether to install plugin or not.

Let's say a plugin is named like **test_plugin**, type is **Action** and Out folder is **_C:\GIS\plugin_folder_**.

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

All plugin data will appear in the selected folder. All data related to plugin and zip-file itself can be found there. According to the type of plugin some parts of code will be different for each option while the mandatory functions remain the same.
The main python file will be named same like a plugin name written by user. 

As in example, there would be a script file names **_test_plugin.py_**. This file can be edited and finally replaced in zip-file in order to change a plugin. This file contains five funcitons in the end of it:

```
    # custom actions, feel free to edit them
    def simple_action(self):
        # run a simple action like in python console of QGIS
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

First four of them are "launchers" of action, widget, map or custom tool and the last one (run) is a selector of launcher function.
* **simple_action** will print a notification in a blue bar of QGIS
* **simple_gui** runs a pyqt widget imported from file template_tools.py which is in the same folder as test_plugin.py. SimpleGui widget can be found in template_tools.py and also modified and be replaced in zip-file of a plugin.
* **simple_map_tool** runs a map tool which also can be found in template_tools.py. Also if this type of plugin is selected, a plugin button becomes checkable. This is mentioned in initGui function where a self.icon_action is defined.
* **custom_tool** is the same thing like running a script from python editor console. It means that pressing a button will just run a file just like if it was run in python editor of QGIS. Actually this is not a good way to go, but experienced users can rewrite a code and import their custom objects the right way.
* **run** runs one of the function above

If there is a need to change something in plugin, this file can be edited according to function typed in ```run()``` method. In the example there is a ```simple_action()``` launching which will make a notication in a blue QGIS bar. Let's say we want to change it and instead of notification make a print of all vector layers with number of their features in current project. 

Change in a code:
```
    # custom actions, feel free to edit them
    def simple_action(self):
        # run a simple action like in python console of QGIS
        all_layers_count = [[l.name(), l.featureCount()] for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer]
        for layer_name, layer_count in all_layers_count:
            print('{} \t {}'.format(layer_name, layer_count))
```

That's it, code is changed and **_test_plugin.py_** can be put in a zip-file. Then plugin should be re-installed in order to see changes.

Another example - to show a simple notification widget window with all that layers and their feature numbers.
```
    # custom actions, feel free to edit them
    def simple_action(self):
        # run a simple action like in python console of QGIS
        all_layers_count = [[l.name(), l.featureCount()] for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer]
        message = '\n'.join(['{} \t {}'.format(layer_name, layer_count) for layer_name, layer_count in all_layers_count])
```


## Scripter tool
![Table loook](https://pereverzev.info/easyPlugin/img/img_es.png)

This tool is made for testing python scripts which eventually can be launched as a plugin. But the main purpose of Scripter is launching python scripts from tiny window. User should specify a direct path to directory with python files. Then window will show a table view of python files while you user is able to edit them in some external code editor. So when user double-click a script in Scripter, the most up-to-date version of selected script will be launched. It also helps in a team work, when you have a shared folder between users, they don't need to constantly update script/plugin, they will have the latest version of tool made by someone.
