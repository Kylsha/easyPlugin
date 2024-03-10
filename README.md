# easyPlugin
QGIS plugin that allows to create plugins.

~ draft guide ~

The main goal of this plugin is to make a fast and easy plugin template. With all respect to [Plugin Builder](https://github.com/g-sherman/Qgis-Plugin-Builder) module, easyPlugin is turnkey solution and makes a plugin ready for installation, testing and editing.
Plugin contains two tools: easyPlugin itself and Scripter - a tool for testing raw python plugin code and other scripts. 

## easyPlugin tool
easyPlugin has just one window and user should type at least plugin name and point a saving folder. Another information is not arbitrary but may be mentioned. Also user can check a plugin type. There are four of them.
* Action type will make plugin do some action just by pressing a plugin icon.
* Widget type is a simple widget template which can be either modified or rewritten completely. 
* Map tool is a simple mapping tool which makes plugin button checkable. It makes a pointer tool which puts point on map by pressing cursor on canvas. Can be deactivated by pressing plugin button one more time or selecting another map tool in QGIS.
* Custom type means user can take some script and make it launching from plugin button. Note that this is a kind of dirty solution. Plugin will just execute a file, not importing user's script modules and other parts that can be reached from main plugin file. The better solution would be to edit plugin's main python file and import script in a right way.

## Scripter tool
This tool is made for testing python scripts which eventually can be launched as a plugin. But the main purpose of Scripter is launching python scripts from tiny window. User should specify a direct path to directory with python files. Then window will show a table view of python files while you user is able to edit them in some external code editor. So when user double-click a script in Scripter, the most up-to-date version of selected script will be launched. It also helps in a team work, when you have a shared folder between users, they don't need to constantly update script/plugin, they will have the latest version of tool made by someone.
