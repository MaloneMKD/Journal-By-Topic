"""
 *(C)Copyright 2023 Malone Napier-Jameson
 *
 * This file is part of Journal By Topic.
 * Journal By Topic is free software: you can redistribute it and/or modify it under the terms of
 * the GNU Lesser General Public License as published by the Free Software Foundation,
 * either version 3 of the License, or (at your option) any later version.
 * Turing Machine Simulator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.

 * You should have received a copy of the GNU Lesser General Public License along with Journal By Topic.
 * There is also a copy available inside the application.
 * If not, see <https://www.gnu.org/licenses/>.
"""
# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import QObject, Signal


class ToggleButton(QObject, QGraphicsPixmapItem):

    # Signals
    clicked = Signal()

    def __init__(self, picA, picB, parentObject=None, parentItem=None):
        """This is a QGraphicsPixmap button that can be toggled on and off"""

        # Calling super class constructors
        QObject.__init__(self, parentObject)
        QGraphicsPixmapItem.__init__(self, parentItem)

        # Variables
        self.toggled= False
        self.toggled_off_pic = picA
        self.toggled_on_pic = picB
        self.setPixmap(picA)


    # Method to manually toggle the button on
    def setOn(self):
        self.toggled = True
        self.setPixmap(self.toggled_on_pic)


    # Method to manually toggle the button off
    def setOff(self):
        self.toggled = False
        self.setPixmap(self.toggled_off_pic)


    def mousePressEvent(self, event):
        pass


    def mouseReleaseEvent(self, event):
        if self.toggled == True:
            self.setOff()
        else:
            self.setOn()

        self.clicked.emit()





