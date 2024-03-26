[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/Kylsha/easyPlugin/blob/main/README.md) 
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

Первые четыре функции — это запуск действия в соответствии с типом плагина, а последняя (`run()`) указывает, какое действие нужно выбрать.

* **simple_action** выводит уведомление в голубой строке над зоной карты QGIS (как в примере выше).
* **simple_gui** запускает pyqt-виджет из файла `template_tools.py`, который расположен в той же папке, что и `test_plugin.py`. Виджет `SimpleGui()`, который запускается этой функцией, расположен в `template_tools.py`. Его можно изменять и заменять сохраненный файл в zip-архиве плагина.
* **simple_map_tool** запускает картографический инструмент (считывание положений курсора и нажатий на карте), который также можно найти в `template_tools.py`. Если выбран этот тип плагина, его кнопка принимает вид переключателя, то есть по аналогии с другими картографическими инструментами. Это определено в функции `initGui()` в которой задается атрибут `self.icon_action`.
* **custom_tool** аналог запуска скрипта из редактора консоли Python в QGIS. Нажатие кнопки плагина всего лишь запускает скрипт, который был указан в easyPlugin. Как было указано ранее, это не очень хорошгий способ, продвинутые пользователи могут переписать часть кода в этой функции с корректной подгрузкой объектов из другого файла.
* **run** запускает одну из функций выше.

Если требуется что-то изменить в плагине, этот файл может быть отредактирован в соответствии с функцией, указанной в `run()`. В примере приведена функция `simple_action()`, которая создает уведомление в голубой строке QGIS. Допустим, необходимо заменить ее на вывод всех векторных слоев текущего проекта и количества объектов в них в консоли Python.

Изменения в коде:
```
    # custom actions, feel free to edit them
    def simple_action(self):
        # run a simple action like in Python console of QGIS
        all_layers_count = [[l.name(), l.featureCount()] for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer]
        for layer_name, layer_count in all_layers_count:
            print('{} \t {}'.format(layer_name, layer_count))
```

После изменений и сохранения файла `test_plugin.py` он может быть загружен в zip-архив плагина, после чего последний должен быть переустановлен, чтобы можно было увидеть изменения. 

Другой пример — сделать то же самое, но с выводом данных по слоям в простой виджет-уведомление.
```
    # custom actions, feel free to edit them
    def simple_action(self):
        # run a simple action like in Python console of QGIS
        all_layers_count = [[l.name(), l.featureCount()] for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer]
        message = '\n'.join(['{}: {}'.format(layer_name, layer_count) for layer_name, layer_count in all_layers_count])
        QMessageBox.information(None, "Notification", message) 
```

После этого при нажатии кнопки будет полявляться виджет с данными по слоям.

Если пользователь выберет тип **Widget** или **Map tool** , в функцию `run()` добавится вызов функции `simple_gui()` или `simple_map_tool()` соответственно. Обе функции отсылаются к файлу `template_tools.py`, который также импортируется из Python-скрипта (т.е., `test_plugin.py`). Если необходимо что-то заменить в функционале шаблонных инструментов, необходимо редактировать файл `template_tools.py`.

Последний тип плагина — **Custom**, который запускает файл скрипта Python. Этот вариант применим для простых плагинов, которые не используют несколько файлов-скриптов и импортов данных из них.

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
