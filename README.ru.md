[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/Kylsha/easyPlugin/blob/main/README.md) 
# easyPlugin
Инструмент для создания плагинов в QGIS.

Основная функция данного плагина - создание шаблонов плагинов под разные задачи. Несмотря на наличие отличного инструмента PluginBuilder, данное решение позволяет создать плагин практически «под ключ». Конечный результат - сам плагин в виде zip-архива и файлы, которые его составляют. Модуль состоит из двух инструментов - непосредственно easyPlugin и Scripter, инструмент для тестирования скриптов на Python.

## Инструмент easyPlugin
![Table loook](https://pereverzev.info/easyPlugin/img/img_ep.png)

### Инструкция
easyPlugin - это виджет, позволяющий пользователю создавать шаблоны плагинов за пару действий.
При открытии инструмента пользователю необходимо заполнить данные, которые представлены в виджете. 

Обязательные к заполнению поля: **Plugin title**, **Plugin type** и **Out folder**. Вся остальная информация (автор, почта, трекер и т.д.) лишь рекомендуема к заполнению.

**1. Plugin title** — это название будущего плагина. Оно должно быть написано только латинскими символами без чисел и знаков препинания за исключением нижнего подчеркивания. Название будет в дальнейшем использоваться в других сопутствующих файлах плагина и классах Python.
**2. Plugin type** — это тип шаблона плагина, который будет взят за основу при создании нового плагина. Типы не представляют собой некую классификацию, это всего лишь образцы популярных видов плагинов, используемых в работе в QGIS.
* **Action** — тип плагина, который выполняет какое-то простое действие в Python по нажатию кнопки будущего плагина 
* **Widget** — тип плагина в виде виджета-отдельного окна с набором функций
* **Map tool** — простейший картографический инструмент, который позволяет добавлять точки на карте по клику. При этом сама кнопка плагина принимает вид checkable, то есть, работает как переключатель: пока инструмент активен, кнопка имеет «нажатый» вид. Как только пользователь выбирает другой инструмент взаимодействия с картой или нажимает по кнопке плагина еще раз, вид кнопки возвращается в исходное положение.
* **Custom** — данный тип подразумевает возможность пользователя внедрить свой скрипт в плагин и запустить его по нажатию кнопки. При выборе данного типа плагина пользователь также должен указать ссылку на файл скрипта Python, который требуется запускать. Стоит отметить, что несмотря на работоспособность данного метода он является не самым лучшим способом для инициализации данных из других файлов. По сути данный метод просто запускает файл скрипта Python по аналогии с запуском его из консоли в QGIS. Лучшим решением здесь был бы импорт скрипта и далее ручная правка функции, работающей с данными из стороннего файла.
**3. Out folder** — это путь, в котором появится плагин и его файлы.

Как только **Plugin title**, **Plugin type** и **Out folder** заполнены, пользователь может сгенерировать плагин соответствующей кнопкой. После создания плагина инструмент также предложит его установить.

Предположим, что название плагина — `test_plugin`, тип — `Action` и выходной путь — `C:\GIS\plugin_folder`. Если пользователь установит данный плагин и нажмет его кнопку, то в QGIS появится голубая строка уведомления с текстом. Это означает, что все хорошо, плагин работает.

### Редактирование содержимого плагина

В выходной папке будет создана следующая структура:

```
├── test_plugin
│   ├── __init__.py
│   ├── icon.png
│   ├── metadata.txt
│   ├── template_tools.py
│   └── test_plugin.py
└── test_plugin.zip
```

В соответствии с типом плагина некоторые части кода скрипта будут отличаться, в то время как основные системные функции останутся без изменений. Основной файл скрипта будет наименован так же как и значение в поле Plugin type.

Как в примере выше, будет создан файл скрипта test_plugin.py. Данный скрипт можно редактировать и по итогу заменять в zip-архиве плагина для изменения его работы. В файле в конце скрипта расположено пять функций.

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

Первые четыре функции — это запуск действия в соответствии с типом плагина, а последняя (run) указывает, какое действие нужно выбрать.

* **simple_action** will print a notification in a blue bar of QGIS (like in the example above).
* **simple_gui** runs a pyqt widget imported from file `template_tools.py` which is in the same folder as `test_plugin.py`. `SimpleGui()` widget can be found in `template_tools.py` and also modified and be replaced in zip-file of a plugin.
* **simple_map_tool** runs a map tool which also can be found in `template_tools.py`. Also if this type of plugin is selected, a plugin button becomes checkable. This is mentioned in `initGui()` function where a `self.icon_action` is defined.
* **custom_tool** is the same thing like running a script from Python editor console. It means that pressing a button will just run a file just as if it was run in Python editor of QGIS. Actually this is not a good way to go, but experienced users can rewrite a code and import their custom objects the right way.
* **run** runs one of the function above.

If there is a need to change something in plugin, this file can be edited according to function menntioned in `run()` method. In the example there is a `simple_action()` function which will make a notication in a blue QGIS bar. Let's say we want to change it and instead of notification make a print of all vector layers with number of their features in current project. 

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

## Scripter tool
![Table loook](https://pereverzev.info/easyPlugin/img/img_es.png)

This tool is made for testing Python script files. User should specify a direct path to directory with Python files. Then window will show a list of Python files while you user is able to edit them in some external code editor. So when user double-click a script in Scripter, the most up-to-date version of selected script will be launched. It also helps in a team work, when you have a shared folder between users, they don't need to constantly update script/plugin, they will have the latest version of tool made by someone.

>[!NOTE]
> Scripter tool was greeted by collegaues by its simplicity. From some moment I prefer it more than plugins with repository that should be updated manually sometimes. It is more convenient in case of issue fixes: collegaues have a same local network path to scripts and tell that some script works incorrectly. I fix the script and tell that it is ready to go. Another users don't have to have update something (plugin via repository or zip-file), they just re-run script and that's it.

Scripts which are run from Scripter should have all needed libraries imported in order to work. Otherwise Scripter will tell that something is wrong with selected script and an error will be printed in Python console of QGIS. So, despite the fact that some libraries are imported in QGIS from startup, they should be re-imported in local script file. 

Example:

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
Here `iface` and `PyQt5` elements are imported. This code snippet can be saved as a Python script file and put in a folder selected as a script path in Scripter. In order to update contents of script list in Scripter widget, a blue refresh button should be pressed. Finally a double click on script will execute it. Same thing can be achieved in by selecting script in a list and pressing a ▶︎ button.

The right part of Scripter window is used to show a description of selected plugins. In order to do that, a file `descriptions.json` should be created in a folder which is selected as a script path. A content of this file should look like that:
```
{
    "test": "A sample Python code snippet.",
    "my_widget": "PyQt5 widget to show layers info"
}
```
where keys are filenames without extensions and values are script file descriptions.
