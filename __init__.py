# -*- coding: utf-8 -*-
"""
/***************************************************************************
easyPlugin 
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
 This script initializes the plugin, making it known to QGIS.
"""
from __future__ import absolute_import

def classFactory(iface):
    # load easyPlugin class from file easyPlugin -- load classname (plugin name)
    from .easyPlugin import easyPlugin # -- from filename import classname
    return easyPlugin(iface) # -- import classname 
